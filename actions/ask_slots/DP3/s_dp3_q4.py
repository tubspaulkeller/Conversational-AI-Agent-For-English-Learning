from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp3_q4"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ calls the next form depending on the user input """
        if tracker.slots.get("s_dp3_q3") == "vocabels":
            return [FollowupAction("dp3_form_voc"), SlotSet("s_dp3_q4", "vocabel_form")]
        else:
            return [FollowupAction("dp3_form_gram"), SlotSet("s_dp3_q4", "grammar_form")]
