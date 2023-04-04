from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType

from actions.common.common import markdown_formatting


class ActionRepeatLastQuest(Action):
    def name(self) -> Text:
        return "action_give_skills"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """ total points are given to the user """
        text = "Frage mich gerne jeder Zeit zu deinen:\n- erzielten Punkten 🎯\n- gesammelten Sternen 🌟\n- verdienten Abzeichen 🎖\n\n Außerdem *erkläre* ich dir gerne, *wofür du Punkte, Abzeichen und Sterne erhältst*, damit du genau weißt, welche Leistungen ich belohne und wie du noch besser werden kannst, frag mich einfach nach dem jeweiligen Element z.B. _Wofür stehen Sterne?_\nEbenfalls kannst du mich immer nach der Bildung bestimmter Zeitformen fragen, wie z.B. _Wie wird das *Simple Past* gebildet_.\n\nFalls wir während deinen Fragen in einem Quiz stecken, kannst du jederzeit zur *letzten Quiz-Frage oder zur DP-Auswahl zurückkehren*, frag mich einfach nach der letzten Frage bzw. nach dem Menü.\n\nUnd wenn du dein *Lernziel anpassen* möchtest, weil du vielleicht noch intensiver lernen möchtest oder dein Tempo verändern willst, dann ist das überhaupt kein Problem! Sag mir einfach bescheid, dass du dein Lernziel anpassen möchtest.\n\nFalls du mich neustarten willst, schreib mir ein einfaches *restart*. 😎"
        dispatcher.utter_message(json_message=markdown_formatting(text))
        return [UserUtteranceReverted(), FollowupAction(tracker.active_form.get('latest_action_name'))]
