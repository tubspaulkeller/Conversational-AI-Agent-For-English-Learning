from slack import WebClient
from slack_sdk.web.async_client import AsyncWebClient
from dotenv import load_dotenv
import os
import json
load_dotenv()

filter_slackbot_id = 'USLACKBOT'
filter_is_admin = False
filter_is_bot = False

client = AsyncWebClient(
    token=os.getenv('SLACK_TOKEN'))


async def get_group_member():
    users = await client.users_list()
    group_members = []
    try:
        for member in users['members']:
            if member['id'] != filter_slackbot_id and member['is_admin'] == filter_is_admin and member['is_bot'] == filter_is_bot:
                group_members.append(member['profile']['first_name'])
                print("DEBUG: MEMBER, ", member['profile']['first_name'])
    except Exception as e:
        print("ERROR: GETING GROUP MEMBERS ", e)

    return group_members


async def get_user(id):
    try:
        user_cred = await client.users_info(user=id)
        return user_cred['user']['profile']['first_name']
        # l_name = user_cred['user']['profile']['last_name']
        # email = user_cred['user']['profile']['email']
    except Exception as e:
        print("ERROR: GETING USER ", e)
        return None, None
