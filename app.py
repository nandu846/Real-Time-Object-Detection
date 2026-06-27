import streamlit as st
from PIL import Image
import os

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Real-Time Object Detection",
    page_icon="🔍",
    layout="wide"
)

# -----------------------------
# Logo
# -----------------------------

logo_path = "assets/logo.png"

if os.path.exists(logo_path):
    logo = Image.open(logo_path)

    col1, col2 = st.columns([1, 5])

    with col1:
        st.image(logo, width=120)

    with col2:
        st.title("Real-Time Object Detection System")
        st.write(
            "Detect objects in images, webcam streams, and videos using YOLOv8."
        )
else:
    st.title("🔍 Real-Time Object Detection System")

st.markdown("---")

# -----------------------------
# Welcome
# -----------------------------

st.header("👋 Welcome")

st.write("""
This application uses **YOLOv8** and **Streamlit** to detect objects in:

- 📷 Images
- 🎥 Webcam
- 🎬 Videos

Use the navigation menu on the left to access each feature.
""")

st.markdown("---")

# -----------------------------
# Features
# -----------------------------

st.header("🚀 Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
### 📷 Image Detection

Upload an image and detect multiple objects with confidence scores.
""")

with col2:
    st.info("""
### 🎥 Webcam Detection

Perform live object detection using your webcam.
""")

with col3:
    st.info("""
### 🎬 Video Detection

Upload a video and detect objects frame by frame.
""")

col4, col5, col6 = st.columns(3)

with col4:
    st.success("""
### 📜 Detection History

View all previous detections.
""")

with col5:
    st.success("""
### 📊 Analytics

Analyze object detection statistics with charts.
""")

with col6:
    st.success("""
### 📥 Export

Download CSV files, images, and processed videos.
""")

st.markdown("---")

# -----------------------------
# Technologies
# -----------------------------

st.header("🛠 Technologies Used")

tech1, tech2, tech3, tech4 = st.columns(4)

tech1.metric("Python", "✔️")
tech2.metric("Streamlit", "✔️")
tech3.metric("OpenCV", "✔️")
tech4.metric("YOLOv8", "✔️")

st.markdown("---")

# -----------------------------
# Quick Start
# -----------------------------

st.header("📖 How to Use")

st.markdown("""
1. Select a page from the left sidebar.
2. Upload an image or video, or open the webcam.
3. Choose the YOLO model.
4. Adjust the confidence threshold.
5. View and download the results.
""")

st.markdown("---")

# -----------------------------
# Footer
# -----------------------------

st.caption("Developed by Nandusri Thummanapally | Powered by Streamlit + YOLOv8")