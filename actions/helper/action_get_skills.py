from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.helper.debug import debug
from actions.gamification.handle_user_scoring import user_score
from actions.common.common import get_dp_inmemory_db


class ActionGetSkills(Action):
    def name(self) -> Text:
        return "action_get_skills"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Frage mich gerne jeder Zeit zu deinen:\n- erzielten Punkten 🎯\n- gesammelten Sternen 🌟\n- verdienten Abzeichen 🎖\n Gerne erkläre ich dir auch, wofür du Punkte, Sterne oder Abzeichen erhälst.\n Außerdem kannst du dein Lernziel jeder Zeit anpassen \n\n Mit 'Was war die letzte Frage' o.ä. kehren wir anschließend zur Quiz-Frage zurück.\nUm mich neuzustarten, tippe bitte 'restart' ein. 😎")
        return [UserUtteranceReverted(), FollowupAction("action_set_reminder_set_dp")]
