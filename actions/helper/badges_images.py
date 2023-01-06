from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.helper.debug import debug
from actions.gamification.handle_user_scoring import user_score
from actions.common.common import get_dp_inmemory_db


class ActionRepeatLastQuest(Action):
    def name(self) -> Text:
        return "action_badges_images"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        badges = get_dp_inmemory_db("badges.json")

        if user_score["total_badges"] == 0:  # change to 0
            dispatcher.utter_message(
                text="Du hast bislang noch keine Abzeichen erhalten. Sobald du einen besonderen Fortschritt gemacht hast, erhältst du ein Abzeichen.\nFrage mich nach der letzten Frage, um sie zu wiederholen und fortzufahren.")
            return [UserUtteranceReverted(), FollowupAction(tracker.active_form.get('latest_action_name'))]

        user_badges = {k: v for k, v in user_score.items() if k.startswith('badge_')
                       and v == 1}

        for k in user_badges.keys():
            dispatcher.utter_message(image=badges[k])

        dispatcher.utter_message(
            text="Frage mich nach der letzten Frage, um sie zu wiederholen und fortzufahren.")
        return [UserUtteranceReverted(), FollowupAction(tracker.active_form.get('latest_action_name'))]
