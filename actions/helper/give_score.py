from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.helper.debug import debug
from actions.gamification.handle_user_scoring import user_score


class ActionRepeatLastQuest(Action):
    def name(self) -> Text:
        return "action_give_user_score"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """ total points are given to the user """
        dispatcher.utter_message(
            text="Dein Punktestand beträgt: {} 🎉".format(user_score["total_points"]))

        return [UserUtteranceReverted(), FollowupAction(tracker.active_form.get('latest_action_name'))]
