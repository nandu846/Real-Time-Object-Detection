import streamlit as st
import cv2
import tempfile
import os
import time

from utils.detector import detect_video_frame

# ----------------------------------------
# Page Configuration
# ----------------------------------------

st.set_page_config(
    page_title="Video Detection",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Video Object Detection")

st.write(
    "Upload a video and detect objects frame by frame using YOLO."
)

# ----------------------------------------
# Sidebar
# ----------------------------------------

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

# ----------------------------------------
# Upload Video
# ----------------------------------------

video = st.file_uploader(
    "Upload a Video",
    type=["mp4", "avi", "mov"]
)

if video is not None:

    st.subheader("📹 Original Video")
    st.video(video)

    # ----------------------------------------
    # Save Uploaded Video Temporarily
    # ----------------------------------------

    temp_video = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    )

    temp_video.write(video.read())
    temp_video.close()

    cap = cv2.VideoCapture(temp_video.name)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        fps = 30

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # ----------------------------------------
    # Video Information
    # ----------------------------------------

    st.markdown("## 📋 Video Information")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Width", width)
    c2.metric("Height", height)
    c3.metric("FPS", round(fps))
    c4.metric("Frames", total_frames)

    st.markdown("---")

    # ----------------------------------------
    # Output Folder
    # ----------------------------------------

    os.makedirs("outputs", exist_ok=True)

    output_path = os.path.join(
        "outputs",
        "DetectedVideo.mp4"
    )

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    progress = st.progress(0)

    status = st.empty()

    start_time = time.time()

    frame_number = 0

    # ----------------------------------------
    # Video Processing
    # ----------------------------------------

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        detected_frame = detect_video_frame(
            frame,
            confidence,
            model_choice
        )

        writer.write(detected_frame)

        frame_number += 1

        progress.progress(
            min(frame_number / total_frames, 1.0)
        )

        status.info(
            f"Processing Frame {frame_number} of {total_frames}"
        )

    cap.release()
    writer.release()

    processing_time = round(
        time.time() - start_time,
        2
    )

    if os.path.exists(temp_video.name):
        os.remove(temp_video.name)

    status.empty()

    progress.progress(1.0)

    st.success(
        f"✅ Video processed successfully in {processing_time} seconds."
    )

    st.markdown("---")

    st.subheader("🎥 Processed Video")

    st.video(output_path)

    with open(output_path, "rb") as file:

        st.download_button(
            label="📥 Download Processed Video",
            data=file,
            file_name="DetectedVideo.mp4",
            mime="video/mp4"
        )

    st.markdown("---")

    st.info(
        """
        **Tips**

        • Use **YOLOv8m** for better accuracy.

        • Use **YOLOv8n** for faster processing.

        • Lower the confidence threshold if some objects are not detected.

        • Large videos may take longer depending on your computer.
        """
    )