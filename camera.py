import cv2
import base64
import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Cattura video dalla webcam
cap = cv2.VideoCapture(0)

def encode_frame(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def video_stream():
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame_encoded = encode_frame(frame)
        socketio.emit('video_frame', {'image': frame_encoded})
        eventlet.sleep(0.03)  # Riduce il carico sulla CPU

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("Client connesso")
    eventlet.spawn(video_stream)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
