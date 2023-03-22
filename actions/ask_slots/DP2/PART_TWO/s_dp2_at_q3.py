from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
import time
from actions.gamification.handle_user_scoring import increase_badges, user_score


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp2_at_q3"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        increase_badges("badge_anwendungsaufgabe")
        dispatcher.utter_message(
            text="Damit hast du deine erste Anwendungsaufgabe in dieser Lektion gemeistert und dir ein Abzeichen verdient!")
        dispatcher.utter_message(
            image="https://res.cloudinary.com/dmnkxrxes/image/upload/v1677413377/Ben_Bot/Abschluss_einer_Anwendungsaufgabe_oucoaz.png")

        dispatcher.utter_message(response="utter_s_dp2_at_q3")
        return []
