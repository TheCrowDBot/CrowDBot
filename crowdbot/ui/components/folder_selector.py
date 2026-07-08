import streamlit as st
from crowdbot.services.image_loader import load_images
from crowdbot.services.pipeline_queue import set_queue


def render_folder_selector():

    folder = st.text_input("Image folder")

    if not folder:
        return None

    images = load_images(folder)

    st.write(f"Images found: {len(images)}")

    if st.button("Load into pipeline"):

        set_queue(images)
        st.success("Pipeline loaded")

        st.rerun()

    return folder
