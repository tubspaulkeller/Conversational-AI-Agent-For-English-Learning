from slack import WebClient
from slack_sdk.web.async_client import AsyncWebClient
from dotenv import load_dotenv
import os
import json
load_dotenv()

# client = AsyncWebClient(
#     token=_get_token()))
# here muss SLACK_TOKEN_TWO, SLACK_TOKEN_THREE,..

# TODO Test


async def get_user(id, tracker):
    print("API CALL: GET USER")
    try:
        client = AsyncWebClient(token=_get_token())
        if tracker.get_slot("first_name") is None:
            user_cred = await client.users_info(user=id, token=_get_token())
            return user_cred['user']['profile']['first_name']

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
