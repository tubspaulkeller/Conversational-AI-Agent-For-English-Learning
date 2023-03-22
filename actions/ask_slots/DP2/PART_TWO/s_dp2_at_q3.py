from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
import time
from actions.gamification.handle_user_scoring import increase_badges, user_score
from actions.common.common import get_dp_inmemory_db


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp2_at_q3"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        increase_badges("badge_anwendungsaufgabe")
        badges = get_dp_inmemory_db("badges.json")
        dispatcher.utter_message(
            text="Damit hast du deine erste Anwendungsaufgabe in dieser Lektion gemeistert und dir ein Abzeichen verdient!")
        dispatcher.utter_message(
            image=badges['badge_anwendungsaufgabe'])

        dispatcher.utter_message(response="utter_s_dp2_at_q3")
        return []
