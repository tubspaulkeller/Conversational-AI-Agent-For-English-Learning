from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp3_q3"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ user can change his goal """
        if tracker.slots.get("s_dp3_q2") == "deny":
            dispatcher.utter_message(response="utter_s_dp3_q1/repeat")
            return [SlotSet("s_dp3_q1", None), SlotSet("s_dp3_q2", None)]
        else:

            dispatcher.utter_message(response="utter_s_dp3_q3")
        return []
