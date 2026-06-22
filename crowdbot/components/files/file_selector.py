import streamlit as st


def render_file_selector():
    # mode = st.radio("Input type", ["Single file", "Multiple files", "Folder"])

    # if mode == "Single file":
    #     file = st.file_uploader("Choose a file")
    #     return [file] if file else []

    return st.file_uploader("Choose files", accept_multiple_files=True)
