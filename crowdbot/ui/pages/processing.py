import streamlit as st
from ui.sidebar import render_sidebar
from ui.components.folder_selector import render_folder_selector
from ui.components.pipeline_view import render_pipeline_view
from services.pipeline_queue import current_item, advance
from services.pipeline_engine import run_obb_step


def render_processing_page():

    render_sidebar()

    render_folder_selector()
    render_pipeline_view()

    image = current_item()
    model_path = st.session_state.get("obb_active_path")

    if not image:
        st.info("No images loaded")
        return

    if not model_path:
        st.warning("No model selected")
        return

    if st.button("Process"):
        result = run_obb_step(
            model_path=model_path,
            show_image=True,
            show_logs=True,
            auto_advance=False,
        )

        st.session_state["last_result"] = result

        
        # advance()
        # st.rerun()
