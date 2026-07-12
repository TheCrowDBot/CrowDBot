from ultralytics import YOLO
import streamlit as st
import time
from pathlib import Path
from crowdbot.config.settings import (
    AUTO_ADVANCE_DEFAULT,
    SHOW_LOGS_DEFAULT,
    SHOW_IMAGE_DEFAULT,
    IMAGE_PREVIEW_WIDTH,
    INFERENCE_LOG_PREFIX,
)
from crowdbot.services.json_utils import save_json
from crowdbot.services.path_utils import get_output_folder


class OBBPipeline:
    name = "obb"

    def __init__(self, model_path: str):
        self.model = YOLO(model_path, verbose=False)

    def infer(
        self,
        image_path: str,
    ):
        return self.model(
            image_path,
            conf=st.session_state.confidence,
            iou=st.session_state.iou,
        )[0]

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

    def _save_result(
        self,
        result: dict,
        image_path: str,
        output_dir: str,
    ):
        image_name = Path(image_path).stem

        output_folder, image_name = get_output_folder(
            image_path,
            output_dir,
        )

        output_file = output_folder / f"{image_name}_obb.json"

        # Remove raw YOLO result before serializing
        save_data = {
            "image": result["image"],
            "detections": result["detections"],
        }

        save_json(data=save_data, path=output_file)

        return output_file

    def run(
        self,
        image_path: str,
        *,
        show_image: bool = SHOW_IMAGE_DEFAULT,
        show_logs: bool = SHOW_LOGS_DEFAULT,
        auto_advance: bool = AUTO_ADVANCE_DEFAULT,
        output_dir=None,
        outputs=None,
        **kwargs,
    ):

        start = time.time()

        if show_logs:
            st.write(f"{INFERENCE_LOG_PREFIX} Processing {image_path}")
            st.write(
                f"{INFERENCE_LOG_PREFIX} Using conf: {st.session_state.confidence}, using iou: {st.session_state.iou}"
            )
        try:
            result = self.infer(image_path)
            detections = self.parse_result(result)
        except Exception:
            st.error("Something went wrong")

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

        if output_dir and outputs and outputs.get("obb", False):
            self._save_result(
                result=output,
                image_path=image_path,
                output_dir=output_dir,
            )

        return output
