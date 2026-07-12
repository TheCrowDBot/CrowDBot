from crowdbot.services.pipeline_runner import PipelineRunner
from crowdbot.services.pipeline_queue import current_item
import streamlit as st
from crowdbot.services.obb_pipeline import OBBPipeline
from crowdbot.services.ocr_pipeline import OCRPipeline
from crowdbot.services.matcher_pipeline import MatcherPipeline
from crowdbot.services.crawio_pipeline import CrawIOPipeline


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


def create_pipeline_runner(
    obb_model,
    ocr_model,
    vocab_path,
):

    return PipelineRunner(
        [
            load_obb_pipeline(obb_model),
            load_matcher_pipeline(),
            load_ocr_pipeline(
                ocr_model,
                vocab_path,
            ),
            load_crawio_pipeline(),
        ]
    )


def run_pipeline():

    image = current_item()

    if image is None:
        st.session_state.pipeline_running = False
        st.session_state.pipeline_finished = True
        return None

    if not st.session_state.get("pipeline_context"):

        st.session_state.pipeline_context = {
            "image_path": image,
            "output_dir": st.session_state.output_folder,
            "outputs": {
                "obb": st.session_state.save_obb,
                "matcher": st.session_state.save_matcher,
                "ocr": st.session_state.save_ocr,
                "drawio": st.session_state.save_drawio,
            },
        }

        st.session_state.pipeline_step = 0

    runner = create_pipeline_runner(
        obb_model=st.session_state.obb_model,
        ocr_model=st.session_state.ocr_model,
        vocab_path=st.session_state.ocr_vocab,
    )

    return runner.run(st.session_state.pipeline_context)
