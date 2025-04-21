import cv2
import time
import threading
import queue
from random_strings import random_string
from ultralytics import YOLO

# Load YOLO model once (globally)
model = YOLO(r'C:\project\aiTds\best (1).pt')

def process_camera_stream(camera_url,):
    cap = cv2.VideoCapture(camera_url)
    if not cap.isOpened():
        print(f"[ERROR] Cannot open stream: {camera_url}")
        return

    frame_queue = queue.Queue(maxsize=5)

    def process_frames():
        while True:
            if not frame_queue.empty():
                image_path = frame_queue.get()
                try:
                    results = model(image_path)
                    for result in results:
                        print(f"[{camera_url}] Detections:", len(result.boxes))
                        filepath = random_string(20)
                        result.save(filename=f"C:/project/aiTds/ai/{filepath}.jpg")
                except Exception as e:
                    print(f"[ERROR][{camera_url}] YOLO processing failed:", e)

    # Start processing thread for this camera
    threading.Thread(target=process_frames, daemon=True).start()

    last_capture_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"[WARNING] Stream disconnected: {camera_url}")
            break

        current_time = time.time()
        if (current_time - last_capture_time) >= 0.3:
            last_capture_time = current_time
            filepath = random_string(20)
            image_path = f"C:/project/aiTds/image/{filepath}.jpg"
            cv2.imwrite(image_path, frame)
            if not frame_queue.full():
                frame_queue.put(image_path)

        cv2.imshow(f'Stream - {camera_url}', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
