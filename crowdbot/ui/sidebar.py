import streamlit as st
from ui.components.model_manager import render_model_manager


def render_sidebar():
    with st.sidebar:
        obb_model = render_model_manager("obb")
        confidence = st.slider("Confidence", 0.0, 1.0, 0.25)
        iou = st.slider("IoU", 0.0, 1.0, 0.45)

        st.divider()

        ocr_model = render_model_manager("ocr")

        run = st.button("Run Pipeline")

    return {
        "obb_model": obb_model,
        "ocr_model": ocr_model,
        "confidence": confidence,
        "iou": iou,
        "run": run,
    }
