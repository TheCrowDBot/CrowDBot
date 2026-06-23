from pathlib import Path
import streamlit as st

st.title("Images")

images_file = st.file_uploader(
    "Select image(s) file(s)", type=["jpg", "jpeg", "png", "tiff", "bmp"], accept_multiple_files=True
)

if images_file:
    images_dir = Path("./images")
    images_dir.mkdir(parents=True, exist_ok=True)

    saved_paths = []

    for image_file in images_file:
        st.image(image_file, caption=image_file.name)
        
        save_path = images_dir / image_file.name

        with open(save_path, "wb") as f:
            f.write(image_file.getbuffer())

        saved_paths.append(str(save_path))

    st.session_state.image_paths = saved_paths

    st.success(f"Saved {len(saved_paths)} image(s)")

    for path in saved_paths:
        st.write(path)
