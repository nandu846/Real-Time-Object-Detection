import os
import pandas as pd
from datetime import datetime

# -----------------------------------
# Log File Path
# -----------------------------------
LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "detection_history.csv")


def initialize_log():
    """
    Create the log file with headers if it doesn't exist.
    """

    os.makedirs(LOG_FOLDER, exist_ok=True)

    if not os.path.exists(LOG_FILE):

        df = pd.DataFrame(columns=[
            "Date",
            "Time",
            "Image Name",
            "Objects",
            "Total Objects",
            "Average Confidence"
        ])

        df.to_csv(LOG_FILE, index=False)


def save_detection(image_name, detected_objects):
    """
    Save one detection record to CSV.
    """

    initialize_log()

    now = datetime.now()

    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%I:%M:%S %p")

    total_objects = len(detected_objects)

    if total_objects == 0:

        object_names = "No Objects"

        average_confidence = 0

    else:

        object_names = ", ".join(
            [obj["Object"] for obj in detected_objects]
        )

        average_confidence = round(
            sum(obj["Confidence"] for obj in detected_objects)
            / total_objects,
            2
        )

    new_data = pd.DataFrame([{
        "Date": date,
        "Time": time,
        "Image Name": image_name,
        "Objects": object_names,
        "Total Objects": total_objects,
        "Average Confidence": average_confidence
    }])

    history = pd.read_csv(LOG_FILE)

    history = pd.concat(
        [history, new_data],
        ignore_index=True
    )

    history.to_csv(
        LOG_FILE,
        index=False
    )


def load_history():
    """
    Return the detection history.
    """

    initialize_log()

    return pd.read_csv(LOG_FILE)


def clear_history():
    """
    Remove all detection history.
    """

    initialize_log()

    empty = pd.DataFrame(columns=[
        "Date",
        "Time",
        "Image Name",
        "Objects",
        "Total Objects",
        "Average Confidence"
    ])

    empty.to_csv(
        LOG_FILE,
        index=False
    )