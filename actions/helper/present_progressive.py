from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.helper.debug import debug
from actions.gamification.handle_user_scoring import user_score
from actions.common.common import markdown_formatting
zeitformen = {
    "simple past": "Das Simple Past wird bei regelmäßigen Verben durch den *Infinitiv des Verbs + -ed* gebildet. Beispiel: I played volleyball yesterday.\nBei unregelmäßigen Verben gibt es Besonderheiten, die beachtet werden müssen.",
    "present perfect": "Das Present Perfect wird gebildet aus einer Form von to *have* und der *dritten Form des Verbs*. Beispiel: I have played volleyball.",
    "past perfect": "Das Past Perfect wird gebildet aus der Kombination to *had* und *des Verbs im Simple Past*. Beispiel: I had played volleyball.",
    "present progressive": "Das Present Progressive (oder Present Continuous) wird gebildet aus einer Form von to *be* (*am*, *are* oder *is*), dem *Infinitiv* (der Stammform) des Verbs und der Endung *-ing*. Deswegen heißt diese Form manchmal auch -ing Form.\nBeispiel: I am playing volleyball"
}


class ActionRepeatLastQuest(Action):
    def name(self) -> Text:
        return "action_ask_zeitform"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entity = tracker.latest_message.get('entities')
        text = zeitformen[entity[0]['value'].lower()]
        dispatcher.utter_message(
            json_message=markdown_formatting(text))

        return [UserUtteranceReverted(), FollowupAction(tracker.active_form.get('latest_action_name'))]
