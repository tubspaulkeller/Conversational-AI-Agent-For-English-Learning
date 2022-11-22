from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_set_next_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ the next form is set, which got selected by the user """
        print(tracker.sender_id)
        next_form = tracker.get_slot("s_get_dp_form")
        return [FollowupAction(next_form), SlotSet("s_set_next_form", next_form)]
