from ultralytics import YOLO

# Dictionary to store loaded models
loaded_models = {}

def get_model(model_name):
    if model_name not in loaded_models:
        loaded_models[model_name] = YOLO(model_name)
    return loaded_models[model_name]


def detect_objects(image_path, confidence=0.25, model_name="yolov8n.pt"):

    model = get_model(model_name)

    try:
        results = model.predict(
        source=image_path,
        conf=confidence,
        save=False,
        verbose=False
        )
    except Exception as e:
        raise RuntimeError(f"Error during object detection: {e}")

    result = results[0]

    detected_image = result.plot()

    detected_objects = []

    for box in result.boxes:

        cls = int(box.cls[0])

        detected_objects.append({
            "Object": model.names[cls],
            "Confidence": round(float(box.conf[0]) * 100, 2)
        })

    return detected_image, detected_objects
def detect_frame(frame, confidence=0.25, model_name="yolov8n.pt"):

    model = get_model(model_name)

    results = model.predict(
        source=frame,
        conf=confidence,
        verbose=False
    )

    result = results[0]

    annotated_frame = result.plot()

    return annotated_frame
def detect_video_frame(frame, confidence=0.25, model_name="yolov8n.pt"):

    model = get_model(model_name)

    results = model.predict(
        source=frame,
        conf=confidence,
        verbose=False
    )

    result = results[0]

    return result.plot()