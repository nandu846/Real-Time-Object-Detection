import streamlit as st
from utils.detector import detect_objects
import pandas as pd
import cv2
import os
from collections import Counter
from utils.logger import save_detection
# ---------------------------------------
# Page Configuration
# ---------------------------------------
st.set_page_config(
    page_title="Image Detection",
    page_icon="📷",
    layout="wide"
)

st.title("📷 Image Object Detection")

st.write("Upload an image and detect objects using the YOLOv8 model.")

# ---------------------------------------
# Sidebar
# ---------------------------------------
st.sidebar.header("Detection Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=1.00,
    value=0.25,
    step=0.05
)

model_choice = st.sidebar.selectbox(
    "Select YOLO Model",
    [
        "yolov8n.pt",
        "yolov8s.pt",
        "yolov8m.pt"
    ]
)

# ---------------------------------------
# Upload Image
# ---------------------------------------
uploaded_file = st.file_uploader(
    "Choose an Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    image_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ---------------------------------------
    # Object Detection
    # ---------------------------------------
    detected_image, detected_objects = detect_objects(
        image_path,
        confidence,
        model_choice
    )
    save_detection(
    uploaded_file.name,
    detected_objects
    )

    detected_image = cv2.cvtColor(
        detected_image,
        cv2.COLOR_BGR2RGB
    )

    # ---------------------------------------
    # Display Images
    # ---------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(
            uploaded_file,
            use_container_width=True
        )

    with col2:
        st.subheader("Detected Image")
        st.image(
            detected_image,
            use_container_width=True
        )

    # ---------------------------------------
    # Save Output Image
    # ---------------------------------------
    output_path = os.path.join(
        "outputs",
        f"detected_{uploaded_file.name}"
    )

    cv2.imwrite(
        output_path,
        cv2.cvtColor(
            detected_image,
            cv2.COLOR_RGB2BGR
        )
    )

    st.markdown("---")

    # ---------------------------------------
    # Detection Results
    # ---------------------------------------
    df = pd.DataFrame(detected_objects)

    st.subheader("📋 Detection Results")

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True
        )

        # -----------------------------
        # Download CSV
        # -----------------------------
        csv = df.to_csv(index=False)

        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name="DetectedObjects.csv",
            mime="text/csv"
        )

        # -----------------------------
        # Download Image
        # -----------------------------
        with open(output_path, "rb") as file:

            st.download_button(
                label="📥 Download Detected Image",
                data=file,
                file_name=f"Detected_{uploaded_file.name}",
                mime="image/jpeg"
            )

        st.metric(
            label="Total Objects Detected",
            value=len(df)
        )

        st.markdown("---")

        # ---------------------------------------
        # Detection Summary
        # ---------------------------------------
        st.subheader("📊 Detection Summary")

        object_counts = Counter(df["Object"])

        summary_df = pd.DataFrame(
            object_counts.items(),
            columns=[
                "Object",
                "Count"
            ]
        )

        st.dataframe(
            summary_df,
            use_container_width=True
        )

        cols = st.columns(len(object_counts))

        for i, (obj, count) in enumerate(object_counts.items()):
            cols[i].metric(
                obj.capitalize(),
                count
            )

        st.markdown("---")

        # ---------------------------------------
        # Confidence Chart
        # ---------------------------------------
        st.subheader("📈 Average Confidence")

        chart_df = (
            df.groupby("Object")["Confidence"]
            .mean()
            .reset_index()
        )

        st.bar_chart(
            chart_df.set_index("Object")
        )

    else:

        st.warning("No objects detected.")