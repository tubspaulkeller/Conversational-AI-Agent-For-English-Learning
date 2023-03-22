from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType

from actions.common.common import markdown_formatting


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp4_q0"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ sending a image for intro in learning story and ask Q1 """
        text = "Da wir das Grundlagen-Kapitel erfolgreich beendet haben, lass uns dein neues Wissen bei einer Lern-Story anwenden!\nIch werde nicht Teil der Geschichte sein, damit du diese eigenständig bewältigen kannst. Aber ich werde dich mit Feedback und Tipps zu deinen Antworten unterstützen!\nDie *Spielregeln* ändern sich: Bei jeder Frage kannst du max. 5 Punkte und min. 3 Punkte holen. Allerdings werden pro Fehler 1 Punkt von den 5 Punkten abgezogen.\n Bitte meide Abkürzung wie z.B. _I've_ und schreibe dies aus _I have_"

        dispatcher.utter_message(json_message=(markdown_formatting(text)))
        dispatcher.utter_message(response="utter_s_dp4_q0")
