import cv2
import numpy as np
import tensorflow as tf

TARGET_W = 200
TARGET_H = 50


def order_points(pts: np.ndarray) -> np.ndarray:
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def crop_rotated(img: np.ndarray, box: list) -> np.ndarray | None:
    # Recorta uma região OBB da imagem e endireita-a

    pts = np.array(box, dtype=np.float32)
    rect = cv2.minAreaRect(pts)
    box_pts = order_points(cv2.boxPoints(rect))
    tl, tr, br, bl = box_pts

    width = int(max(np.linalg.norm(tr - tl), np.linalg.norm(br - bl)))
    height = int(max(np.linalg.norm(bl - tl), np.linalg.norm(br - tr)))

    if width == 0 or height == 0:
        return None

    if height > width:
        width, height = height, width
        dst = np.array(
            [[0, height - 1], [0, 0], [width - 1, 0], [width - 1, height - 1]],
            dtype="float32",
        )
    else:
        dst = np.array(
            [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
            dtype="float32",
        )

    M = cv2.getPerspectiveTransform(box_pts, dst)
    crop = cv2.warpPerspective(
        img,
        M,
        (width, height),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )

    # Upscale se a crop for muito pequena
    if crop.shape[0] < 30:
        scale = 30 / crop.shape[0]
        crop = cv2.resize(crop, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    return crop


def preprocess_for_ocr(image: np.ndarray) -> tf.Tensor:
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image = cv2.resize(image, (TARGET_W, TARGET_H), interpolation=cv2.INTER_CUBIC)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 2))
    image = clahe.apply(image)

    image = cv2.GaussianBlur(image, (3, 3), 0)

    image = cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=15,
        C=10,
    )

    tensor = tf.cast(image, tf.float32) / 255.0
    tensor = tf.expand_dims(tf.expand_dims(tensor, -1), 0)
    return tensor
