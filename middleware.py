import socket
from flask import Flask, request,jsonify
import os
import createNewUser
import time
from datetime import datetime
import casheClasses
import time
import threading
import random_strings
import dotenv
dotenv.load_dotenv()
app=Flask(__name__)

accessCashe={}
otpCashe={}
ipCashe={}
blackListCashe={}

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



if __name__ == "__main__":
    app.run(debug=True)