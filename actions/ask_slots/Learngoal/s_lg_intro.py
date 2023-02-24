from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
import time


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_lg_intro"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        # TODO überprüfen ob DP3 schon gemacht wurde

        # wenn DP3 gemacht wurde dann kann Ziel angepasst werden

        dispatcher.utter_message(response="utter_s_lg_intro")

        return []
