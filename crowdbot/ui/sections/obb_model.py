import streamlit as st

from crowdbot.services.model_service import ModelService


def render_obb_config():

    st.subheader("OBB Detection Model")

    models = ModelService.list_models("obb")

    if not models:

        uploaded = st.file_uploader(
            "Upload OBB Model (.pt)", type=["pt"], key="obb_upload_empty"
        )

        if uploaded:
            ModelService.upload_model("obb", uploaded)
            st.rerun()

        return {"model_path": None}

    names = [m["name"] for m in models]

    selected = st.selectbox("Select model", names, key="obb")

    ModelService.set_selected("obb", selected)

    model_path = ModelService.get_active_path("obb")

    st.success(f"Using: {selected}")

    uploaded = st.file_uploader("Upload new model", type=["pt"], key="obb_upload")

    if uploaded:
        ModelService.upload_model("obb", uploaded)
        st.rerun()

    confidence = st.slider("Confidence", 0.0, 1.0, 0.25)
    iou = st.slider("IoU", 0.0, 1.0, 0.45)

    return {
        "model_path": model_path,
        "confidence": confidence,
        "iou": iou,
    }
