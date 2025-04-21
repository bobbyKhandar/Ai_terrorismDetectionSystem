import boto3
from dotenv import load_dotenv 
from supabase import create_client, Client
import os
load_dotenv()

session = boto3.session.Session()
r2 = session.client(
    service_name='s3',
    aws_access_key_id=os.environ['cloudflareAcessId'],
    aws_secret_access_key=os.environ['cloudFlareSecretAcessKey'],
    endpoint_url=os.environ['CloudFlareEndpoint_url']
)

def uploadImages(filePath,userName,fileName):
    with open(filePath, "rb") as f:
        r2.upload_fileobj(f, "ai-terrorism-detection-system",f"{userName}/{fileName}.jpg")
        print("Upload complete.")

uploadImages(r"C:\project\aiTds\gunDetection.jpg","bobby","deez")