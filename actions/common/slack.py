from slack import WebClient
from slack_sdk.web.async_client import AsyncWebClient
from dotenv import load_dotenv
import os
load_dotenv()

client = AsyncWebClient(
    token=os.getenv('SLACK_TOKEN'))


async def slackitems(tracker):
    # get person from slack
   # get_channel()
    user_id = tracker.sender_id
    try:
        user_cred = await client.users_info(user=user_id)
        # aprint(user_cred)

        u_id = user_cred['user']['id']
        f_name = user_cred['user']['profile']['first_name']
        # l_name = user_cred['user']['profile']['last_name']
        # email = user_cred['user']['profile']['email']

    except Exception as e:
        print("Error while get user : {0}".format(e))
        # a_user = User(u_id='00000000000', f_name='User',
        #               l_name='', email='', level=0)
        return user_id, None, None

    return u_id, f_name, await get_channel()


async def get_channel():
    channel = await client.users_conversations()
    for channel in channel['channels']:
        return channel['id']
