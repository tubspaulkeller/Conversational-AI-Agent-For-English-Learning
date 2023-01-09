from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.helper.debug import debug
from actions.gamification.handle_user_scoring import user_score


class ActionRepeatLastQuest(Action):
    def name(self) -> Text:
        return "action_ask_present_progressive"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        present_progressive = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "text": "Das Present Progressive (oder Present Continuous) wird gebildet aus einer Form von to *be* (*am*, *are* oder *is*), dem *Infinitiv* (der Stammform) des Verbs und der Endung *-ing*. Deswegen heißt diese Form manchmal auch -ing Form.\nBeispiel: I am playing volleyball",
                        "type": "mrkdwn"
                    }
                }
            ]
        }
        dispatcher.utter_message(
            json_message=present_progressive)

        return [UserUtteranceReverted(), FollowupAction(tracker.active_form.get('latest_action_name'))]
