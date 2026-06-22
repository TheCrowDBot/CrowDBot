import streamlit as st
from components.files.file_selector import render_file_selector


# render_header()

# files = render_file_selector()

# if files:
#     st.write(f"{len(files)} files selected")

st.title("CrowDBot")

if "model_path" not in st.session_state:
    st.session_state.model_path = ""

st.write("Current model path:")
st.code(st.session_state.model_path)
