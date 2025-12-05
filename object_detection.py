# object_detection.py
import cv2
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("models/yolov8n.pt")

def run_object_detection(callback=None):
    """
    Starts real-time object detection from webcam.
    `callback` can be a function to store logs, trigger SOPs, etc.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Unable to access camera")
        return

    print("📡 Object detection started. Press 'q' to stop.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break

        # Run YOLO detection
        results = model(frame)
        annotated = results[0].plot()

        # OPTIONAL callback on detection
        if callback and len(results[0].boxes) > 0:
            detected_labels = [model.names[int(box.cls)] for box in results[0].boxes]
            callback(detected_labels)

        cv2.imshow("AI Object Detector", annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
