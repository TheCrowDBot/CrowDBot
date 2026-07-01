from ultralytics import YOLO
import streamlit as st
import time

from config.settings import (
    AUTO_ADVANCE_DEFAULT,
    SHOW_LOGS_DEFAULT,
    SHOW_IMAGE_DEFAULT,
    IMAGE_PREVIEW_WIDTH,
    INFERENCE_LOG_PREFIX,
)


class OBBPipeline:

    def __init__(self, model_path: str):
        self.model = YOLO(model_path, verbose=False)

    def infer(self, image_path: str):
        return self.model(image_path)[0]

    def parse_result(self, result):

        names = self.model.names

        return [
            {
                "class_id": int(box.cls),
                "class_name": names[int(box.cls)],
                "confidence": float(box.conf),
                "polygon": box.xyxyxyxy.tolist(),
            }
            for box in result.obb
        ]

    def visualize(self, result):
        return result.plot()

    def run(
        self,
        image_path: str,
        *,
        show_image: bool = SHOW_IMAGE_DEFAULT,
        show_logs: bool = SHOW_LOGS_DEFAULT,
        auto_advance: bool = AUTO_ADVANCE_DEFAULT,
    ):

        start = time.time()

        if show_logs:
            st.write(f"{INFERENCE_LOG_PREFIX} Processing {image_path}")

        result = self.infer(image_path)
        detections = self.parse_result(result)

        elapsed = time.time() - start

        if show_logs:
            st.write(
                f"{INFERENCE_LOG_PREFIX} "
                f"Detected {len(detections)} objects in {elapsed:.2f}s"
            )

        if show_image:
            annotated = self.visualize(result)
            st.image(
                annotated,
                caption=image_path,
                width=IMAGE_PREVIEW_WIDTH,
            )

        output = {
            "image": image_path,
            "detections": detections,
            "raw": result,
        }

        if auto_advance:
            if show_logs:
                st.write(f"{INFERENCE_LOG_PREFIX} Auto-advancing")

            st.session_state.pipeline_index += 1
            st.rerun()

        return output
