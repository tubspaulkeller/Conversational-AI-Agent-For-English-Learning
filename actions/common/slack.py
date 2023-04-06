from slack import WebClient
from slack_sdk.web.async_client import AsyncWebClient
from dotenv import load_dotenv
import os
import json
load_dotenv()

# client = AsyncWebClient(
#     token=_get_token()))
# here muss SLACK_TOKEN_TWO, SLACK_TOKEN_THREE,..


async def get_user(id, tracker):
    print("API CALL: GET USER")
    try:
        if tracker.get_slot("first_name") is None:
            client = AsyncWebClient(token=_get_token())
            user_cred = await client.users_info(user=id)
            return user_cred['user']['profile']['first_name']
            # l_name = user_cred['user']['profile']['last_name']
            # email = user_cred['user']['profile']['email']

        else:
            return tracker.get_slot("first_name")
    except Exception as e:
        print("ERROR: GETING USER ", e)
        return None


def _get_token():
    try:
        return os.environ['SLACK_TOKEN'] if os.environ['SLACK_TOKEN'] is not None else os.getenv('SLACK_TEST_TOKEN')

    except:
        return os.getenv('SLACK_TEST_TOKEN')
