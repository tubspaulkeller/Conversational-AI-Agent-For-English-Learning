from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.common.common import markdown_formatting


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp3_g_start_button"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        # user can change his goal
        text = "Lass uns nun mit dem Quiz beginnen!\n*Spielregel*: Für eine korrekte Antwort erhälst du 5 Punkte und für eine korrekte Antwort im zweiten Versuch erhälst du 2 Punkte. Du bekommst zwei Chancen von mir, die Frage richtig zu beantworten."
        dispatcher.utter_message(json_message=markdown_formatting(text))
        dispatcher.utter_message(response="utter_s_dp3_g_start_button")
        return []
