import socket
from flask import Flask, request,jsonify,Response
import os
import createNewUser
import time
from datetime import datetime
import casheClasses
import time
import threading
import requests 
import random_strings
import dotenv
import cv2
from fastapi.responses import StreamingResponse
import videofeed
from flask_cors import CORS, cross_origin
import main
import boto3
import cloudFlare

dotenv.load_dotenv()
app=Flask(__name__)
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": "*",
        "allow_headers": ["Content-Type", "X-Forwarded-For"]
    }
})
accessCashe={}
otpCashe={}
ipCashe={}
blackListCashe={}
camera_streams = {}
camera_streams = {"bobby":["http://10.0.37.166:8080/video"]}
accessCashe["bobby"]={"mode":"otp","ip":"127.0.0.1","token":"t1","time":datetime.now()}
def start_camera_processing():
    main.process_camera_stream("http://10.0.37.166:8080/video", "bobby","1")

# Create and start the camera processing thread
camera_thread = threading.Thread(target=start_camera_processing, daemon=True)
camera_thread.start()

# Create and start the camera processing 
def autoCasheCleaner():
    while True:
        currentTime=datetime.now()
        for key,entry in list(ipCashe.items()):
            if (currentTime-entry["time"]).total_seconds() >300:
                del ipCashe[key]
        for key,entry in list(blackListCashe.items()):
            if (currentTime-entry["timeOfBlacklist"]).total_seconds() >(entry["timeTillBlackList(days)"]*24*60):
                del blackListCashe[key]
        for key,entry in list(otpCashe.items()):
            if (currentTime-entry["time"]).total_seconds() >300:
                del otpCashe[key]
        for key,entry in list(accessCashe.items()):
            if (currentTime-entry["time"]).total_seconds() >300:
                print("garbageee")
                del accessCashe[key]
        time.sleep(300)

gc_thread = threading.Thread(target=autoCasheCleaner, daemon=True)
gc_thread.start()

def getDnsIp(dns):
    return socket.gethostbyname(dns)
def validateIp(dns,currentIp):
    expectedIp= getDnsIp(dns)
    if expectedIp==currentIp:
        return True
    else:
        #will do ts later
        return False
@app.route("/getToken",methods=["POST"])
def getToken():
    dns=request.json["dns"]
    currentIp = request.headers.get('X-Forwarded-For', "0.0.0.0")
    userId=request.json["uId"]
    password=request.json["password"]
    print(dns)
    print(currentIp)
    print(userId)
    print(password)
    if validateIp(dns,currentIp):
        token=createNewUser.generateToken(userId,password,dns)
        if token:
            return jsonify({"message":"token Generated Sucessfully","token":token}),200
        else:
            return jsonify({"message":"invalid username or password"})
    else:
        return jsonify({"message":"Unable to generate token due to invalid ip try updating your token"}),400
         
@app.route("/generateOtp",methods=["POST"])
def generateOtp():
    # currentIp = request.headers.get('X-Forwarded-For', request.remote_addr)
    #for remote dev only 
    currentIp = request.headers.get('X-Forwarded-For', "0.0.0.0")
    ipLogs=ipCashe.get(currentIp)
    blacklisted=blackListCashe.get(currentIp)
    if blacklisted:
        return jsonify({"message":"you are blacklisted from using our service for too many unsucessful attempts please contact admin for further details"}),402
    if ipLogs:
        if ipLogs["attempts"]>10:
            return jsonify({"message":"sorry too many attempts trying to login try again later"}),400
    else:
        ipCashe[currentIp]={"attempts":1,"time":datetime.now()}
    result=createNewUser.generateOtp(request.json["uId"],request.json["password"])

    # ipCashe[currentIp]={"attempts":1,"time":datetime.now()}
    if result:
        otpCashe[request.json["uId"]]={
            "otp":result,
            "time":datetime.now(),
            "attempts":0,
            "password":request.json["password"],
            "ip":request.headers.get('X-Forwarded-For', request.remote_addr),
        }
        return jsonify({"message":"otp generated sucessfully"})
    else:
        ipCashe[currentIp]["attempts"]+=1
        ipCashe[currentIp]["time"]=datetime.now()
        return jsonify({"message":"invalid username"}),400

@app.route( "/validateOtp", methods=["POST"])
def validateOtp():
    currentIp = request.headers.get('X-Forwarded-For', "0.0.0.0")
    username=request.json["uId"]
    userCashe=otpCashe.get(username)
    if not userCashe:
        return jsonify({"message": "OTP session not found"}), 404
    userCashe["attempts"]+=1
    otpAttempts=userCashe["attempts"]
    otpIp=userCashe["ip"]
    userPassword=request.json["password"]
    ip=ipCashe.get(currentIp)
    if blackListCashe.get(currentIp):
        return jsonify({"message":"you are currently blacklisted from accessing our services because of susipicious activity please contact admin to get unbanned"})
    if ip:
        ip["attempts"]=ip["attempts"]+1
        if ip["attempts"]>10:
            blackListCashe[currentIp]={"reason":"attempted to login and failed more then 10 times","timeOfBlacklist":datetime.now(),"timeTillBlackList(days)":1}
    else:    
        ipCashe[currentIp]={"attempts":1,"time":datetime.now()}
    if (datetime.now()-userCashe["time"]).total_seconds() >300:
        del otpCashe[username]
        return jsonify({"message":"otp expired"}),400
    if otpAttempts>3:
        return jsonify({"message": "Sorry too many attempts. Try again later"}), 400
    if currentIp!=otpIp:
        return jsonify({"message":"The ip mismatch please try login again"}),400
    if userPassword!=userCashe["password"]:
        return jsonify({"message":"invalid username or password"}),400
    if userPassword==userCashe["password"] and userCashe["otp"] == request.json["otp"]:
        token=random_strings(20)
        accessCashe[username]={"mode":"otp","ip":currentIp,"token":token,"time":datetime.now()}
        return jsonify({"message":"sucessfull","token":"todo"}),200


@app.route("/list-images/<username>", methods=["GET"])
def get_images(username):
    return cloudFlare.get_all_images(username)
# @app.route("/cameras/<username>", methods=["POST"])
# def get_cameras(username):
#     data = request.get_json()
#     token = data.get("token")
#     print(username)
#     current_ip = request.headers.get('X-Forwarded-For', "127.0.0.1")
    
    
#     session = accessCashe.get(username)
#     if not session:
#         print("err1")
#         return jsonify({"error": "No active session for this user."}), 401
#     if session["token"] != token:
#         print("err21")
#         for key, value in accessCashe.items():
#             print(f"Key: {key}, Value: {value}")
#         return jsonify({"error": "Invalid token."}), 401

#     if username not in camera_streams:
#         print("err12")
#         for key, value in camera_streams.items():
#             print(f"Key: {key}, Value: {value}")
#         return jsonify({"cameras": []}), 200
    
#     # Return the number of cameras available
#     cam_count = len(camera_streams[username])
#     return jsonify({"cameras": list(range(cam_count))}), 200

# @app.route("/watch/<username>/<int:cam_index>",methods={"GET"})
# def watch_stream(username, cam_index):
#     token = request.args.get("token")
#     current_ip = request.headers.get("X-Forwarded-For", "127.0.0.1")

#     session = accessCashe.get(username)
#     if not session or session["token"] != token:
#         print("[AUTH ERROR] Token mismatch for user:", username)
#         return "Unauthorized", 401

#     if username not in main.yolo_stream_queues:
#         print(f"username not found in yolo stream queue {username}")
#         for key, entry in list(main.yolo_stream_queues.items()):
#             print(f"keys={key} entry={entry}")
#         return "username not found in yolo stream queue", 404

#     # Ensure cam_index is used as string since queue keys are strings like "1"
#     cam_index_str = str(cam_index)

#     if cam_index_str not in main.yolo_stream_queues[username]:
#         print("cam index not in yoloSteamQueue")
#         print(main.yolo_stream_queues[username])
#         return "cam index not in yolo stream queue", 404

#     def generate():
#         try:
#             while True:
#                 if not main.yolo_stream_queues[username][cam_index_str].empty():
#                     frame = main.yolo_stream_queues[username][cam_index_str].get()
#                     _, buffer = cv2.imencode('.jpg', frame)
#                     frame_bytes = buffer.tobytes()
#                     yield (b'--frame\r\n'
#                            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
#         except GeneratorExit:
#             print(f"[STREAM CLOSED] Client closed connection for {username} cam {cam_index}")
#         except Exception as e:
#             print(f"[STREAM CRASH] {e}")
#             yield b"--frame\r\nContent-Type: text/plain\r\n\r\nStream error\r\n"
#     return Response(generate(), content_type='multipart/x-mixed-replace; boundary=frame')
if __name__ == "__main__":
    app.run(debug=True)