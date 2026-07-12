import streamlit as st

from crowdbot.ui.sidebar import render_sidebar
from crowdbot.ui.components.folder_selector import render_folder_selector
from crowdbot.ui.components.pipeline_view import render_pipeline_view
from crowdbot.services.pipeline_queue import current_item, advance
from crowdbot.services.pipeline_engine import run_pipeline
from pathlib import Path


def render_processing_page():

    sidebar = render_sidebar()

    render_folder_selector()
    render_pipeline_view()

    image = current_item()

    if not image:
        st.info("No images loaded")
        return

    if not sidebar["obb_model"]:
        st.warning("No OBB model selected")
        return

    # Store selected configuration
    st.session_state.obb_model = sidebar["obb_model"]
    st.session_state.ocr_model = sidebar.get("ocr_model")
    st.session_state.ocr_vocab = sidebar.get("ocr_vocab")
    # st.session_state.auto_run = sidebar["auto_run"]

    # Start a new pipeline run
    if st.button("Process"):

        base_folder = st.session_state.output_folder

        output_dir = None

        if base_folder:
            output_dir = Path(base_folder) / "out"
            output_dir.mkdir(
                parents=True,
                exist_ok=True,
            )
        st.session_state.queue_index = 0

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

        st.session_state.pipeline_running = True

        st.rerun()

    # Continue pipeline execution
    if st.session_state.get("pipeline_running", False):

        result = None

        if st.session_state.auto_run:
            result = run_pipeline()

        else:
            if st.button("Run next step"):
                result = run_pipeline()

        if result:
            st.session_state["pipeline_result"] = result

        # Pipeline finished
        if st.session_state.get("pipeline_finished", False):
            st.session_state.pipeline_running = False

            advance()

            next_image = current_item()

            if next_image:
                st.session_state.pipeline_context = {
                    "image_path": next_image,
                    "output_dir": output_dir,
                    "outputs": {
                        "obb": st.session_state.save_obb,
                        "matcher": st.session_state.save_matcher,
                        "ocr": st.session_state.save_ocr,
                        "drawio": st.session_state.save_drawio,
                    },
                }

                st.session_state.pipeline_running = True
                st.rerun()

            else:
                st.success("Pipeline completed!")
