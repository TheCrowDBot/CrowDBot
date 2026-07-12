import streamlit as st
from crowdbot.services.image_loader import load_images
from crowdbot.services.pipeline_queue import set_queue


def render_folder_selector():

    folder = st.text_input(
        "Image folder",
        help="Provide either a single image path or a directory containing images",
    )

    if not folder:
        return None
        
    st.session_state.input_folder = folder

    images = load_images(folder)

    if not images:
        st.warning("No valid images found")
        return None
    else:
        st.write(f"Found {len(images)} Images")

    if st.button("Load into pipeline"):

        set_queue(images)
        st.info("Starting pipeline...")
        st.rerun()

    return folder
