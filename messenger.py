from dotenv import load_dotenv
import os
from twilio.rest import Client
load_dotenv()
def sendMessage(to,body):
    account_sid = os.environ['twirlo_ssid']
    auth_token = os.environ['auth_token']
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    # added an precausious message  
        body=body,
        from_=os.environ["twirloContactNo"],
        to=to,
    )

