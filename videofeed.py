from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
import queue

app = FastAPI()
yolo_stream_queue = queue.Queue()  # This will be injected externally from main.py

def gen_yolo_stream():
    while True:
        print("starting..")
        if not yolo_stream_queue.empty():
            frame = yolo_stream_queue.get()
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

