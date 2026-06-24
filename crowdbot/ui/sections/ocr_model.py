import streamlit as st


def render_ocr_config():

    st.subheader("OCR Model")

    model_path = st.text_input(
        "OCR Model Path", "models/ocr", key="local_ocr_model_path_input"
    )

    model_url = st.text_input("Download URL", key="external_ocr_model_path_input")

    return {
        "model_path": model_path,
        "model_url": model_url,
    }
