import streamlit as st
import pandas as pd
import os

from utils.logger import load_history, clear_history

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Detection History",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Detection History")

st.write("View all previous object detection records.")

st.markdown("---")

# -----------------------------------
# Load History
# -----------------------------------

history = load_history()

if history.empty:

    st.info("No detection history available.")

else:

    st.success(f"Total Records : {len(history)}")

    st.dataframe(
        history,
        use_container_width=True
    )

    st.markdown("---")

    # -----------------------------------
    # Download CSV
    # -----------------------------------

    csv = history.to_csv(index=False)

    st.download_button(
        label="📥 Download Detection History",
        data=csv,
        file_name="DetectionHistory.csv",
        mime="text/csv"
    )

    # -----------------------------------
    # Clear History
    # -----------------------------------

    if st.button("🗑 Clear History"):

        clear_history()

        st.success("History Cleared Successfully!")

        st.rerun()