from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp2_q1"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        dispatcher.utter_message(
            text="Okay, lass uns mit einem Quiz zum Present Perfect beginnen!\nWir sollten das Present Perfect besonders sorgfältig trainieren, da diese Zeitform in den Klausuren der letzten Jahr häufig abgefragt wurde.")
        dispatcher.utter_message(response="utter_s_dp2_q1")
        return []
