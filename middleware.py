import socket
from flask import Flask, request
import os
def getDnsIp(dns):
    return socket.gethostbyname(dns)
app=Flask(__name__)
def validateIp(dns):
    currentIp = request.headers.get('X-Forwarded-For', request.remote_addr)
    expectedIp= getDnsIp(dns)
    if expectedIp==currentIp:
        return True
    #temp
    else:
        #will do ts later
        return False
@app.route(os.environ["server_dns"]+"/getToken")
def getToken():
    #will do ts later
    validateIp()
    