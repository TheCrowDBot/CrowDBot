from services.pipeline_queue import current_item, advance
import streamlit as st

from services.obb_pipeline import OBBPipeline
from config.settings import (
    SHOW_IMAGE_DEFAULT,
    SHOW_LOGS_DEFAULT,
    AUTO_ADVANCE_DEFAULT,
)


@st.cache_resource
def load_obb_pipeline(model_path: str):
    return OBBPipeline(model_path)


def run_obb_step(
    model_path: str,
    *,
    show_image: bool = SHOW_IMAGE_DEFAULT,
    show_logs: bool = SHOW_LOGS_DEFAULT,
    auto_advance: bool = AUTO_ADVANCE_DEFAULT,
):

    image = current_item()

    if image is None:
        return None

    pipeline = load_obb_pipeline(model_path)

    result = pipeline.run(
        image,
        show_image=show_image,
        show_logs=show_logs,
        auto_advance=False,
    )

    if auto_advance:
        advance()
        st.rerun()

    return result


def process_current_image(process_fn):
    image = current_item()

    if image is None:
        return None

    result = process_fn(image)

    return result


def next_step():
    advance()
