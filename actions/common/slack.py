from slack import WebClient
from slack_sdk.web.async_client import AsyncWebClient
from dotenv import load_dotenv
import os
import json
load_dotenv()

client = AsyncWebClient(
    token=os.getenv('SLACK_TOKEN'))

USER = {}


async def get_user(id, tracker):
    print("API CALL: GET USER")
    try:
        if tracker.get_slot("first_name") is None:
            user_cred = await client.users_info(user=id)
            USER = dict(
                name=user_cred['user']['profile']['first_name'],
                id=id
            )
            return user_cred['user']['profile']['first_name']
            # l_name = user_cred['user']['profile']['last_name']
            # email = user_cred['user']['profile']['email']
        else:
            return USER['name']
    except Exception as e:
        print("ERROR: GETING USER ", e)
        return None
