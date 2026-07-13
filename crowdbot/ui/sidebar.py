import streamlit as st
from crowdbot.ui.components.model_manager import render_model_manager


def render_sidebar():
    with st.sidebar:
        obb_config = render_model_manager("obb")
        st.slider(
            "Confidence",
            0.0,
            1.0,
            0.40,
            help="The model's certainty score; predictions below this threshold are ignored.",
            key="confidence",
        )
        st.slider(
            "IoU",
            0.0,
            1.0,
            0.45,
            help="Measures the overlap between a predicted bounding box and the ground truth.",
            key="iou",
        )

        st.divider()

        ocr_config = render_model_manager("ocr")

        st.checkbox(
            "Auto Run?",
            help="Automatically execute the next pipeline stage after each step.",
            key="auto_run",
        )

        with st.expander("Output Settings"):

            input_folder = st.session_state.get(
                "input_folder",
                None,
            )

            if input_folder:
                output_folder = f"{input_folder}/out"

                st.info(f"Outputs will be saved to:\n\n{output_folder}")

                st.session_state.output_folder = output_folder

            else:
                st.warning("Load an image folder first.")

            st.write("Save:")
            st.checkbox(
                "DrawIO diagram",
                value=True,
                key="save_drawio",
            )

            st.checkbox(
                "OBB detections",
                value=False,
                key="save_obb",
            )

            st.checkbox(
                "Matcher result",
                value=False,
                key="save_matcher",
            )

            st.checkbox(
                "OCR result",
                value=False,
                key="save_ocr",
            )

    return {
        "obb_model": obb_config["model_path"],
        "ocr_model": ocr_config["model_path"],
        "ocr_vocab": ocr_config.get("vocab_path"),
    }
