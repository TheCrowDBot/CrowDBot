from pathlib import Path
import streamlit as st

st.title("Saved images")

images_dir = Path("./images")
images = list(images_dir.glob("*"))

if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = None


def delete_image(image_path):
    image_path.unlink()
    st.success(f"Deleted {image_path.name}")
    st.session_state.confirm_delete = None
    st.rerun()


if not images:
    st.info("No images found.")
else:
    for i in range(0, len(images), 3):
        cols = st.columns(3)

        for col, image_path in zip(cols, images[i:i+3]):
            with col:
                st.image(str(image_path), caption=image_path.name)

                if st.session_state.confirm_delete == str(image_path):
                    st.warning("Are you sure you want to delete this image?")

                    c1, c2 = st.columns(2)

                    with c1:
                        if st.button("Yes", key=f"yes_{image_path}"):
                            delete_image(image_path)

                    with c2:
                        if st.button("No", key=f"no_{image_path}"):
                            st.session_state.confirm_delete = None
                            st.rerun()

                else:
                    if st.button("🗑️ Delete", key=f"del_{image_path}"):
                        st.session_state.confirm_delete = str(image_path)
                        st.rerun()