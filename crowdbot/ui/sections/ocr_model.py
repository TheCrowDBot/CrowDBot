import streamlit as st

from crowdbot.services.model_service import ModelService


def render_ocr_config():

    st.subheader("OCR Model")

    models = ModelService.list_models("ocr")

    if not models:

        uploaded_model = st.file_uploader(
            "Upload OCR Model (.keras)", type=["keras"], key="ocr_upload_empty"
        )
        uploaded_vocab = st.file_uploader(
            "Upload Vocab (.json)", type=["json"], key="ocr_vocab_empty"
        )

        if uploaded_model and uploaded_vocab:
            ModelService.upload_ocr_model(uploaded_model, uploaded_vocab)
            st.rerun()
        elif uploaded_model and not uploaded_vocab:
            st.warning("Faz também upload do vocab.json")

        return {"model_path": None, "vocab_path": None}

    names = [m["name"] for m in models]

    selected = st.selectbox("Select model", names, key="ocr")

    ModelService.set_selected("ocr", selected)

    model_path = ModelService.get_active_path("ocr")
    vocab_path = ModelService.get_active_vocab_path("ocr")

    st.success(f"Using: {selected}")

    if not vocab_path:
        st.warning("Este modelo não tem vocab associado.")

    uploaded_model = st.file_uploader(
        "Upload new model", type=["keras"], key="ocr_upload"
    )
    uploaded_vocab = st.file_uploader(
        "Upload new vocab", type=["json"], key="ocr_vocab"
    )

    if uploaded_model and uploaded_vocab:
        ModelService.upload_ocr_model(uploaded_model, uploaded_vocab)
        st.rerun()

    return {
        "model_path": model_path,
        "vocab_path": vocab_path,
    }
