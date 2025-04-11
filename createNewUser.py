from dotenv import load_dotenv 
from supabase import create_client, Client
import os
from fernet import Fernet
import random_strings
load_dotenv()

url= os.environ["NEXT_PUBLIC_SUPABASE_URL"]
key = os.environ["service_role_SUPABASE_KEY"]
supabase: Client = create_client(url, key)

f = Fernet(os.environ["SupperSecretKey"].encode())

def createNewAcessPoint(ipv4,contactNo,role):
    token = Fernet.generate_key().decode()
    encriptedToken=f.encrypt(token).decode("utf-8")
    userId=random_strings.random_string(15)
    password=random_strings.random_string(35)
    response = (
        supabase.table("whitelist")
        .insert({"ip":ipv4,"userid":userId,"contact_no":contactNo,"role":role,"password":password})
        .execute()
    )
    print(response)

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











# createNewAcessPoint("")


