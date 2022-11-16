from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp4_end"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        return [SlotSet("s_dp4_end", "end_of_dp4_form"), SlotSet("s_get_dp", None), SlotSet("s_set_next_form", None), FollowupAction("get_dp_form")]

# We want to get to the coliseum
# How much does it cost
# Can I get two tickets pls
# Do you offer a discount for students
# We have lived in Braunschweig since 2000
