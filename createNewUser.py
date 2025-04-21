from dotenv import load_dotenv 
from supabase import create_client, Client
import os
from fernet import Fernet
import random_strings
import messenger

load_dotenv()

url= os.environ["NEXT_PUBLIC_SUPABASE_URL"]
key = os.environ["service_role_SUPABASE_KEY"]
supabase: Client = create_client(url, key)

f = Fernet(os.environ["SupperSecretKey"].encode())

def createNewAcessPoint(dns,contactNo,role):
    password=random_strings.random_string(35)
    encriptedPassword=f.encrypt(password).decode("utf-8")
    userId=random_strings.random_string(15)
    try:
        response = (
            supabase.table("whitelist")
            .insert({"dns":dns,"userid":userId,"contact_no":contactNo,"role":role,"password":encriptedPassword})
            .execute()
        )
    except:
        print("error while creating an new user")
    
        
  

def checkRequest(userId,password):
    response = (
    supabase.table("whitelist")
    .select("*")
    .match({"userid":userId,"password":password})
    .execute()
    )
    if response:
        return response.data[0]["ip"]
    else:
        return ""

def generateToken(userId,password,dns):
    response= (
    supabase.table("whitelist")
    .select("*")
    .match({"userid":userId,"password":password,"dns":dns})
    .execute()
    )
    if response:
        return random_strings.random_string(20)
    else:
        return ""

def generateOtp(userId,password):
    encPass=f.encrypt(password).decode("utf-8")
    response= (
    supabase.table("whitelist")
    .select("contact_no")
    .match({"userid":userId,"password":password})
    .execute()
    )
    if response:
        otp=random_strings.random_string(6)
        messenger.sendMessage(response.data[0]["contact_no"],"some user has tried to access your account in ai weapon detection system if its you heres your otp\n"+otp)
        return otp
    else:
        return ""
# createNewAcessPoint("")