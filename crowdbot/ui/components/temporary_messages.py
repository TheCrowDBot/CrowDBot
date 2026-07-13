import time
import streamlit as st


def show_temp_success(message: str, key: str, ttl: int):
    now = time.time()

    if "messages" not in st.session_state:
        st.session_state.messages = {}

    st.session_state.messages[key] = {"text": message, "time": now, "ttl": ttl}


def render_messages():

    now = time.time()

    if "messages" not in st.session_state:
        return

    for key in list(st.session_state.messages.keys()):

        msg = st.session_state.messages[key]

        if now - msg["time"] < msg["ttl"]:
            st.success(msg["text"])
        else:
            del st.session_state.messages[key]
