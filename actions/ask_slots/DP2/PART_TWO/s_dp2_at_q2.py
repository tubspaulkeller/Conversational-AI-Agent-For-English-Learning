from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
import time
from actions.gamification.handle_user_scoring import increase_badges, user_score


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp2_at_q2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        if tracker.get_slot("s_dp2_at_q1") == 'yes':
            dispatcher.utter_message(response="utter_s_dp2_at_q2")
        return []
