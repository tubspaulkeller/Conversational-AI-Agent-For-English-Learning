from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType

from actions.common.common import markdown_formatting


class ActionRepeatLastQuest(Action):
    def name(self) -> Text:
        return "action_back_navigation"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("s_get_dp_form", None), SlotSet("s_set_next_form", None), FollowupAction("get_dp_form")]
