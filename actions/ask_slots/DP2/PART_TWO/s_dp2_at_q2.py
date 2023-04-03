from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
import time
from actions.gamification.handle_user_scoring import increase_badges, user_score, get_tries
from actions.common.common import markdown_formatting


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp2_at_q2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        if tracker.get_slot("s_dp2_at_q1") == 'yes':
            if get_tries() == 0:
                dispatcher.utter_message(
                    json_message=markdown_formatting("Die *Spielregeln* ändern sich: Bei jeder Frage kannst du max. 5 Punkte und min. 3 Punkte holen. Allerdings werden pro Fehler 1 Punkt von den 5 Punkten abgezogen. Nach drei Versuchen gebe ich dir die Lösung."))
            dispatcher.utter_message(response="utter_s_dp2_at_q2")
        return []
