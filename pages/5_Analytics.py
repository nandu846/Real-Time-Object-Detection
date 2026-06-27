import streamlit as st
import pandas as pd
from collections import Counter
from utils.logger import load_history

# ------------------------------------
# Page Configuration
# ------------------------------------

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analytics Dashboard")

st.write("Analytics based on all previous detections.")

st.markdown("---")

# ------------------------------------
# Load History
# ------------------------------------

history = load_history()

if history.empty:

    st.warning("No detection history found.")

    st.stop()

# ------------------------------------
# Calculate Statistics
# ------------------------------------

total_images = len(history)

total_objects = history["Total Objects"].sum()

average_confidence = round(
    history["Average Confidence"].mean(),
    2
)

# Count every detected object
all_objects = []

for objects in history["Objects"]:

    if objects == "No Objects":
        continue

    obj_list = [obj.strip() for obj in objects.split(",")]

    all_objects.extend(obj_list)

object_counter = Counter(all_objects)

if object_counter:
    most_detected = object_counter.most_common(1)[0][0]
else:
    most_detected = "None"

# ------------------------------------
# Dashboard Metrics
# ------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📸 Images Processed",
    total_images
)

col2.metric(
    "📦 Total Objects",
    total_objects
)

col3.metric(
    "🏆 Most Detected",
    most_detected
)

col4.metric(
    "🎯 Avg Confidence",
    f"{average_confidence}%"
)

st.markdown("---")

# ------------------------------------
# Object Count Table
# ------------------------------------

st.subheader("📋 Object Frequency")

object_df = pd.DataFrame(
    object_counter.items(),
    columns=[
        "Object",
        "Count"
    ]
)

if not object_df.empty:

    st.dataframe(
        object_df,
        use_container_width=True
    )

else:

    st.info("No objects detected yet.")

st.markdown("---")

# ------------------------------------
# Bar Chart
# ------------------------------------

st.subheader("📊 Object Distribution")

if not object_df.empty:

    st.bar_chart(
        object_df.set_index("Object")
    )

st.markdown("---")

# ------------------------------------
# Confidence Trend
# ------------------------------------

st.subheader("📈 Average Confidence Per Image")

confidence_df = history[
    [
        "Image Name",
        "Average Confidence"
    ]
]

st.line_chart(
    confidence_df.set_index("Image Name")
)

st.markdown("---")

# ------------------------------------
# Download Analytics
# ------------------------------------

csv = history.to_csv(index=False)

st.download_button(
    label="📥 Download Analytics CSV",
    data=csv,
    file_name="Analytics.csv",
    mime="text/csv"
)