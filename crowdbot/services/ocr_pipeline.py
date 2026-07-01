import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.layers import StringLookup
from keras import ops
import streamlit as st
import time
import cv2

from services.ocr_preprocessing import crop_rotated, preprocess_for_ocr
from config.settings import (
    SHOW_IMAGE_DEFAULT,
    SHOW_LOGS_DEFAULT,
    AUTO_ADVANCE_DEFAULT,
    OCR_LOG_PREFIX,
    IMAGE_PREVIEW_WIDTH,
    OCR_CLASSES,
)

print(
    SHOW_IMAGE_DEFAULT,
    SHOW_LOGS_DEFAULT,
    AUTO_ADVANCE_DEFAULT,
    OCR_LOG_PREFIX,
    IMAGE_PREVIEW_WIDTH,
    OCR_CLASSES,
)


@keras.utils.register_keras_serializable()
class CTCLayer(keras.layers.Layer):
    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.loss_fn = keras.backend.ctc_batch_cost

    def call(self, y_true, y_pred):
        batch_len = ops.cast(ops.shape(y_true)[0], dtype="int64")
        input_length = ops.cast(ops.shape(y_pred)[1], dtype="int64")
        label_length = ops.cast(ops.shape(y_true)[1], dtype="int64")
        input_length = input_length * ops.ones(shape=(batch_len, 1), dtype="int64")
        label_length = label_length * ops.ones(shape=(batch_len, 1), dtype="int64")
        self.add_loss(self.loss_fn(y_true, y_pred, input_length, label_length))
        return y_pred

    def get_config(self):
        return super().get_config()


def load_vocab(vocab_path: str):
    import json

    with open(vocab_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    characters = data["characters"]
    vocab_size = len(characters)
    padding_token = vocab_size + 1

    char_to_num = StringLookup(vocabulary=characters, mask_token=None)
    num_to_char = StringLookup(
        vocabulary=char_to_num.get_vocabulary(),
        mask_token=None,
        invert=True,
    )
    return num_to_char, padding_token


def decode_predictions(preds: np.ndarray, num_to_char) -> list[str]:
    input_len = np.ones(preds.shape[0]) * preds.shape[1]
    results = keras.backend.ctc_decode(preds, input_length=input_len, greedy=True)[0][0]
    out = []
    for res in results:
        res = tf.gather(res, tf.where(tf.not_equal(res, -1)))
        text = tf.strings.reduce_join(num_to_char(res)).numpy().decode("utf-8")
        out.append(text)
    return out


class OCRPipeline:

    def __init__(self, model_path: str, vocab_path: str = "../config/vocab.json"):
        self.num_to_char, _ = load_vocab(vocab_path)

        raw_model = keras.models.load_model(
            model_path,
            custom_objects={"CTCLayer": CTCLayer},
        )

        # Extrai o sub-modelo de inferência (sem a CTC loss)
        self.model = keras.models.Model(
            inputs=raw_model.input[0],
            outputs=raw_model.get_layer(name="logits").output,
        )

    def run_on_crop(self, crop: np.ndarray) -> str:
        """Corre OCR numa única crop (np.ndarray BGR ou cinza)."""
        tensor = preprocess_for_ocr(crop)
        pred = self.model.predict(tensor, verbose=0)
        texts = decode_predictions(pred, self.num_to_char)
        return texts[0] if texts else ""

    def run(
        self,
        image_path: str,
        detections: list[dict],
        *,
        show_image: bool = SHOW_IMAGE_DEFAULT,
        show_logs: bool = SHOW_LOGS_DEFAULT,
        auto_advance: bool = AUTO_ADVANCE_DEFAULT,
    ) -> dict:

        start = time.time()
        img = cv2.imread(image_path)

        if img is None:
            raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

        results = []

        for det in detections:
            if det["class_name"] not in OCR_CLASSES:
                continue
            polygon = det["polygon"]
            if isinstance(polygon[0][0], list):
                polygon = polygon[0]

            crop = crop_rotated(img, polygon)
            if crop is None or crop.size == 0:
                continue

            text = self.run_on_crop(crop)

            results.append(
                {
                    "class_id": det["class_id"],
                    "class_name": det["class_name"],
                    "confidence": det["confidence"],
                    "polygon": det["polygon"],
                    "text": text,
                }
            )

            if show_logs:
                st.write(f"{OCR_LOG_PREFIX} [{det['class_name']}] → '{text}'")

            if show_image:
                import cv2 as _cv2

                crop_rgb = _cv2.cvtColor(crop, _cv2.COLOR_BGR2RGB)
                st.image(
                    crop_rgb,
                    caption=f"{det['class_name']}: {text}",
                    width=IMAGE_PREVIEW_WIDTH,
                )

        elapsed = time.time() - start

        if show_logs:
            st.write(f"{OCR_LOG_PREFIX} OCR: {len(results)} palavras em {elapsed:.2f}s")

        output = {
            "image": image_path,
            "ocr_results": results,
        }

        if auto_advance:
            st.session_state.pipeline_index += 1
            st.rerun()

        return output
