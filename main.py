import cv2
import time
import threading
import queue
from random_strings import random_string
from ultralytics import YOLO

# Load YOLO model once (outside the function for efficiency)
model = YOLO("C:/project/aiTds/detect/train/weights/best.pt")

# Queue to store frames for processing
frame_queue = queue.Queue(maxsize=5)

def process_frames():
    """ Function to process frames asynchronously using YOLO """
    while True:
        if not frame_queue.empty():
            image_path = frame_queue.get()
            results = model(image_path)  # Run YOLO inference
            
            for result in results:
                print("Detections:", len(result.boxes))
                
                filepaths = random_string(20)
                result.save(filename=f"C:/project/aiTds/ai/{filepaths}.jpg")

# Start YOLO processing thread
processing_thread = threading.Thread(target=process_frames, daemon=True)
processing_thread.start()

# IP Camera URL
url = 'http://192.168.135.114:8080/video'
cap = cv2.VideoCapture(url)

# Time tracking for capturing frames
last_capture_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit if video stream is unavailable

    current_time = time.time()

    # Capture frame every 300ms (0.3 seconds)
    if (current_time - last_capture_time) >= 0.3:
        last_capture_time = current_time  # Update timestamp
        
        cv2.imshow('Mobile Video Stream', frame)
        
        filepath = random_string(20)
        image_path = f"C:/project/aiTds/image/{filepath}.jpg"
        cv2.imwrite(image_path, frame)  # Save frame
        
        # Add frame to queue for YOLO processing
        if not frame_queue.full():
            frame_queue.put(image_path)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
