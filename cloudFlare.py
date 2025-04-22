import boto3
from dotenv import load_dotenv 
from supabase import create_client, Client
import os
from flask import jsonify
import base64
load_dotenv()

session = boto3.session.Session()
r2 = session.client(
    service_name='s3',
    aws_access_key_id=os.environ['cloudflareAcessId'],
    aws_secret_access_key=os.environ['cloudFlareSecretAcessKey'],
    endpoint_url=os.environ['CloudFlareEndpoint_url']
)
def get_all_images(username):
    bucket = "ai-terrorism-detection-system"
    prefix = f"{username}/"
    images = []

    try:
        response = r2.list_objects_v2(Bucket=bucket, Prefix=prefix)
        contents = response.get("Contents", [])

        for obj in contents:
            key = obj["Key"]
            if not key.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                continue  # skip non-image files

            image_data = r2.get_object(Bucket=bucket, Key=key)["Body"].read()
            encoded = base64.b64encode(image_data).decode("utf-8")
            content_type = "jpeg" if key.endswith(".jpg") else key.split('.')[-1]
            images.append(f"data:image/{content_type};base64,{encoded}")

        return jsonify(images)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def uploadImages(filePath,userName,fileName):
    with open(filePath, "rb") as f:
        r2.upload_fileobj(f, "ai-terrorism-detection-system",f"{userName}/{fileName}.jpg")
        print("Upload complete.")
