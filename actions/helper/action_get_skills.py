from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.helper.debug import debug
from actions.gamification.handle_user_scoring import user_score
from actions.common.common import get_dp_inmemory_db, markdown_formatting
lets_go_button = [
    {'title': "zurück", 'payload': '/i_lets_go{\"e_lets_go\":\"LETS_GO\"}'}]


class ActionGetSkills(Action):
    def name(self) -> Text:
        return "action_get_skills"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = "Frage mich gerne jeder Zeit zu deinen:\n- erzielten Punkten 🎯\n- gesammelten Sternen 🌟\n- verdienten Abzeichen 🎖\n\n Außerdem *erkläre* ich dir gerne, *wofür du Punkte, Abzeichen und Sterne erhältst*, damit du genau weißt, welche Leistungen ich belohne und wie du noch besser werden kannst, frag mich einfach nach dem jeweiligen Element z.B. _Wofür stehen Sterne?_\nEbenfalls kannst du mich immer nach der Bildung bestimmter Zeitformen fragen, wie z.B. _Wie wird das *Simple Past* gebildet_.\n\nFalls wir während deinen Fragen in einem Quiz stecken, kannst du jederzeit zur *letzten Quiz-Frage oder zur DP-Auswahl zurückkehren*, frag mich einfach nach der letzten Frage.\n\nUnd wenn du dein *Lernziel anpassen* möchtest, weil du vielleicht noch intensiver lernen möchtest oder dein Tempo verändern willst, dann ist das überhaupt kein Problem! Sag mir einfach bescheid, dass du dein Lernziel anpassen möchtest.\n\nFalls du mich neustarten willst, schreib mir ein einfaches *restart*. 😎"
        dispatcher.utter_message(json_message=markdown_formatting(text))

        # dispatcher.utter_message(
        #   text=" ", buttons=lets_go_button)
        return [SlotSet("s_get_dp_form", None), SlotSet("s_set_next_form", None), FollowupAction("get_dp_form")]
