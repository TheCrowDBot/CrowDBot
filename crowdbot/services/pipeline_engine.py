from crowdbot.services.pipeline_queue import current_item, advance
import streamlit as st

from crowdbot.services.obb_pipeline import OBBPipeline
from crowdbot.services.ocr_pipeline import OCRPipeline
from crowdbot.services.matcher_pipeline import MatcherPipeline
from crowdbot.services.crawio_pipeline import CrawIOPipeline
from crowdbot.config.settings import (
    SHOW_IMAGE_DEFAULT,
    SHOW_LOGS_DEFAULT,
    AUTO_ADVANCE_DEFAULT,
)


@st.cache_resource
def load_matcher_pipeline():
    return MatcherPipeline()


@st.cache_resource
def load_crawio_pipeline():
    return CrawIOPipeline()


@st.cache_resource
def load_obb_pipeline(model_path: str):
    return OBBPipeline(model_path)


@st.cache_resource
def load_ocr_pipeline(model_path: str, vocab_path: str):
    return OCRPipeline(model_path, vocab_path)


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


def run_ocr_step(
    model_path: str,
    vocab_path: str,
    matcher_result,
    *,
    show_image: bool = SHOW_IMAGE_DEFAULT,
    show_logs: bool = SHOW_LOGS_DEFAULT,
    auto_advance: bool = AUTO_ADVANCE_DEFAULT,
):
    image = current_item()
    if image is None:
        return None

    pipeline = load_ocr_pipeline(model_path, vocab_path)
    result = pipeline.run(
        schema=matcher_result,
        image_path=image,
        show_image=show_image,
        show_logs=show_logs,
    )

    if auto_advance:
        advance()
        st.rerun()

    return result


def run_crawio_step(json: str):
    pipeline = load_crawio_pipeline()
    return pipeline.run(json=json)


def run_matcher_step(
    *,
    obb_result: dict,
    show_logs: bool = SHOW_LOGS_DEFAULT,
):
    pipeline = load_matcher_pipeline()

    return pipeline.run(
        image=obb_result["image"],
        detections=obb_result["detections"],
        show_logs=show_logs,
    )


def process_current_image(process_fn):
    image = current_item()

    if image is None:
        return None

    result = process_fn(image)

    return result


def next_step():
    advance()
