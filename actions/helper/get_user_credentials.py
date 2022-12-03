from actions.common.slack import get_user
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
        first_name = await get_user(tracker.sender_id, tracker)
        if first_name != None:
            # TODO replace with utter_greet
            dispatcher.utter_message(f"Hey {first_name}! 😊")
            return [SlotSet("first_name", first_name)]
        else:
            #     # TODO replace with utter_greet/no_username
            dispatcher.utter_message(f"Hey Buddy! 😊")
            return [SlotSet("first_name", "Buddy")]
