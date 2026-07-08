import cv2
import numpy as np
import torch
from PIL import Image


TARGET_W = 256
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

    if crop.shape[0] < 30:
        scale = 30 / crop.shape[0]
        crop = cv2.resize(crop, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    return crop


def normalize_image(img: Image.Image) -> Image.Image:
    img = img.convert("L")
    w, h = img.size
    scale = min(TARGET_W / w, TARGET_H / h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    img = img.resize((nw, nh), Image.BILINEAR)
    canvas = Image.new("L", (TARGET_W, TARGET_H), 255)
    canvas.paste(img, ((TARGET_W - nw) // 2, (TARGET_H - nh) // 2))
    return canvas


def preprocess_for_ocr(image: np.ndarray) -> torch.Tensor:
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    pil_img = Image.fromarray(image)
    pil_img = normalize_image(pil_img)

    arr = np.array(pil_img, dtype=np.float32) / 255.0
    tensor = torch.from_numpy(arr).unsqueeze(0).unsqueeze(0)  # (1, 1, H, W)
    return tensor