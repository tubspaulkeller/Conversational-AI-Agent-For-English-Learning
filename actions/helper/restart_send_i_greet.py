from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted


##########################################################################################
# Send I Greet
##########################################################################################


class ActionIGreet(Action):
    def name(self) -> Text:
        return "action_send_i_greet"

    def run(self, dispatcher, tracker, domain):
        # data = {
        #     "intent": {
        #         "name": "/i_greet",
        #         "confidence": 1.0,
        #     }
        # }
        # UserUttered(text="/i_greet", parse_data=data)]  # , FollowupAction("action_get_user_credentials")]
        return []
