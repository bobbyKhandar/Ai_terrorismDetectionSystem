class Model:
    #{"dns":dns,"ip":currentIp,"token":token,"timeOfLastUpdate":time.time()}
    def __init__(self,dns,ip,token,timeOfLastUpdate):
        self.dns=dns
        self.ip=ip
        self.token=token
        self.timeOfLastUpdate=timeOfLastUpdate
    
    def __hash__(self):
        return hash(self.dns)
    
    def __eq__(self, newCashe):
        return isinstance(newCashe,Model) and self.dns==newCashe.dns
    
class OtpCashe:
    def __init__(self,otp,time,attempts,ip,username):
        self.otp=otp
        self.time=time
        self.attempts=attempts
        self.ip=ip
        self.username=username
    
    def __hash__(self):
        return hash((self.username, self.ip))
    
    def __eq__(self, newOtpCashe):
        return isinstance(newOtpCashe,OtpCashe) and self.username==newOtpCashe.username and self.ip==newOtpCashe.ip
        #{"otp":result,"time":datetime.now(),"attempts":0,"ip":request.headers.get('X-Forwarded-For', request.remote_addr),"username":request.json["uId"]})
        