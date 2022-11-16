from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType


class ActionStartLearnStory(Action):

    def name(self) -> Text:
        return "action_dp2_finish"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        print("action_dp2_finish")
        return []
      #  return [SlotSet("s_get_dp", None), SlotSet("s_set_next_form", None), FollowupAction("get_dp_form")]
