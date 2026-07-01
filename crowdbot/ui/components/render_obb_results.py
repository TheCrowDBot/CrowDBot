import streamlit as st


def render_obb_results(result):
    """Display OBB detection results in a clean layout."""
    if not result:
        st.info("No results to display yet.")
        return

    st.subheader("OBB Detection Results")

    col1, col2 = st.columns([3, 2])

    with col1:
        if result.get("annotated_image") is not None:
            st.image(
                result["annotated_image"],
                caption="Detection Output",
                use_column_width=True,
            )
        else:
            st.image(
                result.get("image"), caption="Original Image", use_column_width=True
            )

    with col2:
        st.metric("Detections", len(result.get("detections", [])))
        st.metric("Processing Time", f"{result.get('processing_time', 0):.2f}s")

        image_name = result.get("image", "Unknown")
        st.write(
            f"**Image:** {image_name.split('/')[-1] if '/' in image_name else image_name}"
        )

    # Detailed detections
    detections = result.get("detections", [])
    if detections:
        st.subheader("Detected Objects")

        data = []
        for i, det in enumerate(detections):
            data.append(
                {
                    "ID": i + 1,
                    "Class": det["class_name"],
                    "Confidence": f"{det['confidence']:.4f}",
                    "Points": len(det["polygon"]),
                }
            )

        st.dataframe(data, use_container_width=True, hide_index=True)
