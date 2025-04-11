#droped the idea of making and .exe 

import requests
import random_strings
import time
from flask import Flask
import socket

def getIp():
    return requests.get("https://api.ipify.org").text

def createDns():
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "API-Key": API_KEY
    }
    data = {
        "name": DOMAIN.split('.')[0],
        "domainName": DOMAIN,
        "ipv4Address": get_public_ip(),
        "ttl": 60
    }
    response = requests.post("https://api.dynu.com/v2/dns", json=data, headers=headers)
    print("DNS Creation:", response.json())