from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
#from rasa_core.trackers import DialogueStateTracker
#from rasa_core.domain import Domain
from actions.common.slack import slackitems
##########################################################################################
# Get user credentials
##########################################################################################


class ActionGetUserCredentials(Action):
    def name(self) -> Text:
        return "action_get_user_credentials"

    async def run(self, dispatcher, tracker, domain):
        """ get user credentials """
        user_id, first_name, channel_id = await slackitems(tracker)
        print(channel_id)
        print(tracker.current_state())
        #tracker.sender_id = channel_id

        #t1 = DialogueStateTracker(sender_id, domain.slots)

        if first_name != None:
            # TODO replace with utter_greet
            dispatcher.utter_message(f"Hey {first_name}! 😊")
            return [SlotSet("user_id", user_id), SlotSet("first_name", first_name)]
        else:
            # TODO replace with utter_greet/no_username
            dispatcher.utter_message(f"Hey Buddy! 😊")
            return [SlotSet("user_id", user_id), SlotSet("first_name", "Buddy")]
