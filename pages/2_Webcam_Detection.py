import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av

from utils.detector import detect_frame

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Webcam Detection",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 Real-Time Webcam Object Detection")

st.write(
    """
    Click **START** below to begin real-time object detection using your webcam.
    """
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Detection Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.10,
    1.00,
    0.25,
    0.05
)

model_choice = st.sidebar.selectbox(
    "Select YOLO Model",
    [
        "yolov8n.pt",
        "yolov8s.pt",
        "yolov8m.pt"
    ]
)

# -----------------------------
# Video Processor
# -----------------------------
class VideoProcessor(VideoProcessorBase):

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        detected = detect_frame(
            img,
            confidence,
            model_choice
        )

        return av.VideoFrame.from_ndarray(
            detected,
            format="bgr24"
        )

# -----------------------------
# Webcam Stream
# -----------------------------
webrtc_streamer(
    key="object-detection",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={
        "video": {
            "width": {"ideal": 1280},
            "height": {"ideal": 720},
            "frameRate": {"ideal": 30}
        },
        "audio": False
    }
)

st.markdown("---")

st.info(
    """
    💡 Tips

    • Allow camera permission when prompted.

    • Higher confidence values reduce false detections.

    • YOLOv8n is the fastest model.

    • YOLOv8m provides better accuracy but is slower.
    """
)