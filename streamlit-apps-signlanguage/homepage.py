import streamlit as st
import cv2
from ultralytics import YOLO
import numpy as np

# Load model YOLOv8
model_path = 'YoloV8/ultralytics/runs/detect/train/weights/best.pt'  # Ganti dengan path ke model Anda
model = YOLO(model_path)

def get_color(class_id):
    np.random.seed(int(class_id))
    return tuple(np.random.randint(100, 255, size=3).tolist())

def detect_objects(frame):
    results = model(frame)
    overlay = frame.copy()
    alpha = 0.6

    for result in results:
        boxes = result.boxes
        for box in boxes:
            xmin, ymin, xmax, ymax = box.xyxy[0].cpu().numpy()
            confidence = box.conf[0].cpu().numpy()
            class_id = box.cls[0].cpu().numpy()
            label = f"{model.names[int(class_id)]} {confidence:.2f}"
            color = get_color(class_id)

            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
            (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
            text_x, text_y = int(xmin), int(ymin) - 10
            cv2.rectangle(overlay, (text_x, text_y - text_height - 5), (text_x + text_width, text_y + 5), color, -1)
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
            cv2.putText(frame, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    return frame

def homepage():
    st.markdown("<h1 style='text-align: center; color: white;'>Deteksi Bahasa Isyarat BISINDO</h1>", unsafe_allow_html=True)
    cap = cv2.VideoCapture(1)
    stframe = st.empty()
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Gagal membaca frame dari webcam.")
            break
        detected_frame = detect_objects(frame)
        detected_frame = cv2.cvtColor(detected_frame, cv2.COLOR_BGR2RGB)
        stframe.image(detected_frame, channels="RGB", use_container_width=True)
    cap.release()
