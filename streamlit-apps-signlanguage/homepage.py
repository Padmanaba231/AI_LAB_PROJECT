import streamlit as st
import cv2
import torch
import numpy as np
import time
import os

# --- Caching Model ---
@st.cache_resource(show_spinner=False)
def load_model(model_path):
    model = torch.load(model_path, map_location=torch.device('cpu'))  # Pakai CPU agar tidak ada masalah CUDA
    model.eval()  # Set model ke mode evaluasi
    return model

def get_color(class_id):
    np.random.seed(int(class_id))
    return tuple(np.random.randint(100, 255, size=3).tolist())

def detect_objects(frame, model):
    frame_resized = cv2.resize(frame, (640, 480))  # Resize untuk performa lebih baik
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    results = model(frame_rgb)
    detections = results.xyxy[0].cpu().numpy()

    for detection in detections:
        xmin, ymin, xmax, ymax, confidence, class_id = detection
        label = f"{model.names[int(class_id)]} {confidence:.2f}"
        color = get_color(class_id)

        cv2.rectangle(frame_resized, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
        cv2.putText(frame_resized, label, (int(xmin), int(ymin) - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    return frame_resized

def homepage():
    st.title("Deteksi Bahasa Isyarat BISINDO")
    model_path = os.path.join(os.getcwd(), "streamlit-apps-signlanguage/model_used/yolov5/best.pt")
    model = load_model(model_path)

    if "camera_active" not in st.session_state:
        st.session_state["camera_active"] = False

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎥 Mulai Kamera"):
            st.session_state["camera_active"] = True
    with col2:
        if st.button("🛑 Stop Kamera"):
            st.session_state["camera_active"] = False

    stframe = st.empty()

    if st.session_state["camera_active"]:
        cap = cv2.VideoCapture(0)  # Pastikan kamera di index 0

        while cap.isOpened() and st.session_state["camera_active"]:
            ret, frame = cap.read()
            if not ret:
                st.error("Gagal membaca frame dari webcam.")
                break

            detected_frame = detect_objects(frame, model)
            detected_frame_rgb = cv2.cvtColor(detected_frame, cv2.COLOR_BGR2RGB)
            stframe.image(detected_frame_rgb, channels="RGB", use_container_width=True)
            time.sleep(0.1)

        cap.release()
        st.session_state["camera_active"] = False
