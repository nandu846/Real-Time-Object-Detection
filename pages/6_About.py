import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ About This Project")

st.markdown("---")

st.header("📌 Project Title")

st.write("""
**Real-Time Object Detection System Using YOLOv8 and Streamlit**
""")

st.markdown("---")

st.header("📖 Project Description")

st.write("""
This project is an AI-powered object detection system that detects
multiple objects from images, webcam streams, and videos using the
YOLOv8 deep learning model.

The application provides a simple web interface built with Streamlit,
allowing users to upload media, perform detection, and analyze results.
""")

st.markdown("---")

st.header("🚀 Features")

st.markdown("""
- 📷 Image Object Detection
- 🎥 Real-Time Webcam Detection
- 🎬 Video Object Detection
- 📜 Detection History
- 📊 Analytics Dashboard
- 📄 CSV Export
- 🤖 Multiple YOLO Models
""")

st.markdown("---")

st.header("🛠 Technologies Used")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
- Python
- Streamlit
- OpenCV
- Pandas
""")

with col2:
    st.markdown("""
- Ultralytics YOLOv8
- NumPy
- Matplotlib
""")

st.markdown("---")

st.header("📚 Dataset")

st.write("""
The object detector uses pretrained YOLOv8 models trained on the
COCO Dataset, which contains 80 object classes.
""")

st.markdown("---")

st.header("👨‍💻 Developer")



st.markdown("---")

st.success("Thank you for using the Real-Time Object Detection System!")