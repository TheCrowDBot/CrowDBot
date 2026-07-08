import crowmatcher
from dataclasses import asdict
from PIL import Image
import numpy as np
import streamlit as st


class MatcherPipeline:
    def run(
        self,
        image,
        detections,
        *,
        show_logs: bool = False,
    ):
        image_array = np.array(Image.open(image))
        result = crowmatcher.process(
            image=image_array,
            detections=detections,
        )

        return asdict(result)
