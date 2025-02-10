import streamlit as st
import torch
import cv2
import numpy as np
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import pathlib
import platform

# --- Caching Model ---
@st.cache_resource(show_spinner=False)
def load_model(model_path):
    return torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

def get_color(class_id):
    np.random.seed(int(class_id))
    return tuple(np.random.randint(100, 255, size=3).tolist())

def detect_objects(frame, model):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame_rgb)
    detections = results.xyxy[0].cpu().numpy()

    for detection in detections:
        xmin, ymin, xmax, ymax, confidence, class_id = detection
        label = f"{model.names[int(class_id)]} {confidence:.2f}"
        color = get_color(class_id)

        cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
        cv2.putText(frame, label, (int(xmin), int(ymin) - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    return frame

# --- Kelas untuk proses video ---
class VideoProcessor(VideoTransformerBase):
    def __init__(self, model):
        self.model = model

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        detected_frame = detect_objects(img, self.model)
        return av.VideoFrame.from_ndarray(detected_frame, format="bgr24")

def homepage():
    st.title("Deteksi Bahasa Isyarat BISINDO")
    
    # Check the operating system and set the appropriate path type
    if platform.system() == 'Windows':
        pathlib.PosixPath = pathlib.WindowsPath
    else:
        pathlib.WindowsPath = pathlib.PosixPath
    # Load model
    model_path = "./streamlit-apps-signlanguage/model_used/yolov5/best.pt"
    model = load_model(model_path)

    # Streaming Kamera
    webrtc_streamer(
        key="sign_language_stream",
        video_processor_factory=lambda: VideoProcessor(model),
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    )
