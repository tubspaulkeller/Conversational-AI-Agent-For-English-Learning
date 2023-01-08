from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType


class ActionRepeatLastQuest(Action):
    def name(self) -> Text:
        return "action_give_skills"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """ total points are given to the user """
        dispatcher.utter_message(
            text="Mein Name ist Ben und ich bin dein persönlicher Assistent. Ich helfe dir dabei, deine Englisch-Fähigkeiten  zu verbessern. 🤖\nFrage mich gerne jeder Zeit zu deinen:\n- erzielten Punkten 🎯\n- gesammelten Sternen 🌟\n- verdienten Abzeichen 🎖\nGerne erkläre ich dir auch, wofür du Punkte, Sterne oder Abzeichen erhälst.\n\n Mit 'Was war die letzte Frage' o.ä. kehren wir anschließend zur Quiz-Frage zurück.\nUm mich neuzustarten, tippe bitte 'restart' ein. 😎")

        return [UserUtteranceReverted(), FollowupAction(tracker.active_form.get('latest_action_name'))]
