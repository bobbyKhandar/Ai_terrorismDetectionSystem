from ultralytics import YOLO

from datetime import datetime
import messenger
import os

model = YOLO(r"C:\project\aiTds\best (1).pt")


results = model(r"C:\project\aiTds\gunDetection.jpg")
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  
    result.save(filename="result.jpg")
    names = model.names
    print("boxes= \n")
    # lastSent=datetime(2012, 3, 5, 23, 8, 15) 
    lastSent = datetime(1, 1, 1, 0, 0, 0)
    labelSet=""
    for r in results:
        for box in r.boxes:
            confidence = box.conf.item()
            classId=int(box.cls.item())
            label=model.names[classId]
            print(model.names)
            if classId!=5:
                labelSet+=f"weapon/subject:{label}, Confidence:{confidence:.2f}"
    if labelSet!="":
        currentTime=datetime.now()
        difference=currentTime-lastSent
        durationSeconds=difference.total_seconds()
        durationMinutes=difference.total_seconds()/60
        print(durationMinutes)
        if durationMinutes>5:
            lastSent=currentTime
            print("hi")
            messenger.sendMessage(os.environ["userContactNo"],"this message was generated through an project made by a btech student learning to detect weapons in real time basis all of the messages are through an simulated enviorment.\n "+labelSet)
        


# # Find your Account SID and Auth Token at twilio.com/console
# # and set the environment variables. See http://twil.io/secure

