import streamlit as st


def get_queue():
    if "pipeline_queue" not in st.session_state:
        st.session_state.pipeline_queue = []

    return st.session_state.pipeline_queue


def set_queue(items: list[str]):
    st.session_state.pipeline_queue = items
    st.session_state.queue_index = 0


def get_index():
    return st.session_state.get("queue_index", 0)


def advance():
    st.session_state.queue_index = get_index() + 1


def current_item():

    queue = get_queue()
    idx = get_index()

    if idx >= len(queue):
        return None

    return queue[idx]
