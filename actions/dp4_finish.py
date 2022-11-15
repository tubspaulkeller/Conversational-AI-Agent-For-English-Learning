from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType


class ActionStartLearnStory(Action):

    def name(self) -> Text:
        return "action_dp4_finish"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        print("action_dp4_finish")
        dispatcher.utter_message(response="utter_get_dp/3")
        return []

# We want to get to the coliseum
#  How much does it cost
#  Can I get two tickets please
#  Do you offer a student discount?
#  We have been living in Brunswick since 2017
