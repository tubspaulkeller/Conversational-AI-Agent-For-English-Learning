from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
import time
from actions.common.common import markdown_formatting


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_lg_1"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        user_selection = tracker.slots.get("s_lg_intro")
        if user_selection == "oberziel":
            dispatcher.utter_message(response="utter_s_lg_1")

        if user_selection == "vokabelziel":
            dispatcher.utter_message(response="utter_s_lg_1/vokabelziel")

        if user_selection == "grammatikziel":
            dispatcher.utter_message(response="utter_s_lg_1/grammatikziel")
        return []
