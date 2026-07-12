import streamlit as st
from PIL import Image
from crowdbot.services.pipeline_queue import current_item, get_queue, get_index


def render_pipeline_view():

    queue = get_queue()
    idx = get_index()

    st.write(f"Progress: {idx} / {len(queue)}")

    current = current_item()

    if current:
        st.write("Current image:")
        img = Image.open(current)

        st.image(img, width=250, caption=current)

    if idx != 0 and idx == len(queue):
        st.info("Pipeline finished")
