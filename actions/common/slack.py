from slack import WebClient
from slack_sdk.web.async_client import AsyncWebClient
from dotenv import load_dotenv
import os
import json
load_dotenv()

client = AsyncWebClient(
    token=os.getenv('xoxb-4393955305015-4421152854193-OIi3OXCUr3LteogsqMScLiB5'))


async def get_user(id, tracker):
    print("API CALL: GET USER")
    try:
        if tracker.get_slot("first_name") is None:
            user_cred = await client.users_info(user=id)
            return user_cred['user']['profile']['first_name']
            # l_name = user_cred['user']['profile']['last_name']
            # email = user_cred['user']['profile']['email']
        else:
            return tracker.get_slot("first_name")
    except Exception as e:
        print("ERROR: GETING USER ", e)
        return None
