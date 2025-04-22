import cv2
import time
import os
from ultralytics import YOLO
from random_strings import random_string
import cloudFlare

# Load YOLO model
model = YOLO(r'C:\project\aiTds\best (1).pt')

def process_video(video_path, username):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[ERROR] Cannot open video: {video_path}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[INFO] End of video or stream error.")
            break

        filename = random_string(20)
        image_path = f"C:/project/aiTds/ai/{filename}.jpg"
        cv2.imwrite(image_path, frame)

        try:
            results = model(image_path)
            detection_found = False
            for result in results:
                if len(result.boxes) > 0:
                    detection_found = True
                    print(f"[DETECTED] {len(result.boxes)} object(s).")
                    output_path = f"C:/project/aiTds/ai/{filename}_out.jpg"
                    result.save(filename=output_path)
                    cloudFlare.uploadImages(output_path, username, filename)

            if detection_found:
                # Show frame only if objects were detected
                cv2.imshow("YOLO Stream", frame)
            else:
                print("[INFO] No detections. Deleting frame.")
                os.remove(image_path)

        except Exception as e:
            print("[ERROR] YOLO processing failed:", e)

        # Break on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run it
process_video(r"C:\project\aiTds\Video Shows How Students Fled From Nashville Shooting.mp4", "bobby")
