import streamlit as st
from crowdbot.ui.sidebar import render_sidebar
from crowdbot.ui.components.folder_selector import render_folder_selector
from crowdbot.ui.components.pipeline_view import render_pipeline_view
from crowdbot.services.pipeline_queue import current_item
from crowdbot.services.pipeline_engine import (
    run_obb_step,
    run_ocr_step,
    run_matcher_step,
    run_crawio_step,
)


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

    if st.button("Process"):
        obb_result = run_obb_step(
            model_path=sidebar["obb_model"],
        )

        st.session_state["last_obb_result"] = obb_result

        if obb_result and sidebar.get("ocr_model") and sidebar.get("ocr_vocab"):

            # Matcher result is the json to feed crawio
            matcher_result = run_matcher_step(
                obb_result=obb_result,
            )
            ocr_result = run_ocr_step(
                model_path=sidebar["ocr_model"],
                vocab_path=sidebar["ocr_vocab"],
                matcher_result=matcher_result,
            )
            st.session_state["last_ocr_result"] = ocr_result

            generated = run_crawio_step(json=matcher_result)
            st.write(generated)
        elif obb_result and sidebar.get("ocr_model") and not sidebar.get("ocr_vocab"):
            st.warning("OCR model selected but vocab.json is missing.")
