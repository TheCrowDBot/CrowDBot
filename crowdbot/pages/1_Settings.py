from pathlib import Path
import streamlit as st

st.title("Settings")

model_file = st.file_uploader(
    "Select model file", type=["gguf", "bin", "pt", "safetensors"]
)

if model_file:
    models_dir = Path("./models")
    models_dir.mkdir(parents=True, exist_ok=True)

    save_path = models_dir / model_file.name

    with open(save_path, "wb") as f:
        f.write(model_file.getbuffer())

    st.session_state.model_path = str(save_path)
    st.success(f"Saved model to: {save_path}")
