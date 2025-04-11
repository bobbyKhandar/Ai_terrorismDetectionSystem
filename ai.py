from ultralytics import YOLO
from dotenv import load_dotenv
import os
from twilio.rest import Client
from datetime import datetime

load_dotenv()




def sendMessage(weapons):
    account_sid = os.environ['twirlo_ssid']
    auth_token = os.environ['auth_token']
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    # added an precausious message  
        body="this message was generated through an project made by a btech student learning to detect weapons in real time basis all of the messages are through an simulated enviorment.\n "+weapons,
        from_=os.environ["twirloContactNo"],
        to=os.environ["userContactNo"],
    )
model = YOLO(r"C:\project\aiTds\best (1).pt")

results = model(r"C:\project\aiTds\gunDetection.jpg")  # return a list of Results objects

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
    lastSent=datetime.now()
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
        if durationMinutes>5:
            sendMessage(labelSet)
        


# # Find your Account SID and Auth Token at twilio.com/console
# # and set the environment variables. See http://twil.io/secure

