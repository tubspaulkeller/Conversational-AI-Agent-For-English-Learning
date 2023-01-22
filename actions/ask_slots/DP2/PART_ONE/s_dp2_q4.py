from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
import time


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp2_q4"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        dispatcher.utter_message(response="utter_s_dp2_q4/msg")
        dispatcher.utter_message(response="utter_s_dp2_q4/button")
        return []
