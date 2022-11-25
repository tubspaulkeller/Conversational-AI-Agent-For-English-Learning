from actions.common.slack import get_group_member, get_user
from typing import (Text)
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

##########################################################################################
# Get user credentials
##########################################################################################


class ActionGetUserCredentials(Action):
    def name(self) -> Text:
        return "action_get_user_credentials"

    async def run(self, dispatcher, tracker, domain):
        """ get user credentials """
        # if no channel
        first_name = await get_user(tracker.sender_id)
        #first_name = None
        # if group channel
        # group_members = ', '.join(await get_group_member())
        # if group_members != None:
        #     dispatcher.utter_message(f"Hey {group_members}! 😊")
        #     # return [SlotSet("first_name", first_name)]
        #     return []
        if first_name != None:
            # TODO replace with utter_greet
            dispatcher.utter_message(f"Hey {first_name}! 😊")
            return [SlotSet("first_name", first_name)]
        # else:
        #     # TODO replace with utter_greet/no_username
        #     dispatcher.utter_message(f"Hey Buddy! 😊")
        #     return [SlotSet("first_name", "Buddy")]
