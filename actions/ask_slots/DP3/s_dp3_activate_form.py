from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp3_activate_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        if tracker.get_slot("s_dp3_v_end") is not None:
            return [SlotSet("s_dp3_activate_form", "ACTIVATED"), FollowupAction("dp3_form_gram")]

        if tracker.get_slot("s_dp3_g_end") is not None:
            return [SlotSet("s_dp3_activate_form", "ACTIVATED"), FollowupAction("dp3_form_voc")]
