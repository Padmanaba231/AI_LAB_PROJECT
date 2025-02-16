import streamlit as st
import streamlit.components.v1 as components

def homepage():
    st.title("Deteksi Bahasa Isyarat BISINDO - Realtime dengan Yolo")
    
    start_detection = st.button("Mulai Deteksi")
    stop_detection = st.button("Hentikan Deteksi")
    
    if start_detection:
        # Menyematkan kode HTML yang memuat roboflow.js untuk deteksi langsung di browser
        html_code = """
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Realtime Detection</title>
          <script src="https://cdn.roboflow.com/0.2.25/roboflow.js"></script>
          <style>
            body {
              font-family: Arial, sans-serif;
              text-align: center;
            }
            canvas {
              border: 1px solid black;
              margin-top: 10px;
            }
          </style>
        </head>
        <body>
          <h2>Deteksi Objek dengan Yolo</h2>
          <p>Pastikan Anda memberikan izin akses kamera.</p>
          <canvas id="video_canvas" width="640" height="480"></canvas>
          <video id="video" width="640" height="480" autoplay style="display: none;"></video>
          <script>
            var publishable_key = "rf_cNyibtTHvcM7QIxiQaMSBQjzVKc2";
            const MODEL_NAME = "test1-ridk5";
            const MODEL_VERSION = 6;
            const CONFIDENCE_THRESHOLD = 0.5;
            
            const video = document.getElementById("video");
            const canvas = document.getElementById("video_canvas");
            const ctx = canvas.getContext("2d");
            
            const classColors = {};
            function getColorForClass(className) {
              if (!(className in classColors)) {
                classColors[className] = `rgb(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)})`;
              }
              return classColors[className];
            }
            
            navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
              video.srcObject = stream;
              video.play();
              
              roboflow.auth({ publishable_key }).load({ model: MODEL_NAME, version: MODEL_VERSION }).then(model => {
                function detect() {
                  ctx.clearRect(0, 0, canvas.width, canvas.height);
                  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                  model.detect(video).then(predictions => {
                    let scaleX = canvas.width / video.videoWidth;
                    let scaleY = canvas.height / video.videoHeight;
                    
                    predictions.forEach(pred => {
                      let x = (pred.bbox.x - pred.bbox.width / 2) * scaleX;
                      let y = (pred.bbox.y - pred.bbox.height / 2) * scaleY;
                      let width = pred.bbox.width * scaleX;
                      let height = pred.bbox.height * scaleY;
                      
                      let color = getColorForClass(pred.class);
                      ctx.strokeStyle = color;
                      ctx.lineWidth = 2;
                      ctx.strokeRect(x, y, width, height);
                      ctx.fillStyle = color;
                      ctx.font = "16px Arial";
                      ctx.fillText(pred.class + " (" + Math.round(pred.confidence * 100) + "%)", x, y - 10);
                    });
                  });
                  requestAnimationFrame(detect);
                }
                detect();
              });
            }).catch(error => console.error("Error accessing webcam:", error));
          </script>
        </body>
        </html>
        """
        
        components.html(html_code, height=550)
