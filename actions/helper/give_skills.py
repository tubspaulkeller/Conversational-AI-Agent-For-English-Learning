from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType

from actions.common.common import markdown_formatting, get_skills_text


class ActionRepeatLastQuest(Action):
    def name(self) -> Text:
        return "action_give_skills"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """ total points are given to the user """
        text = get_skills_text()
        dispatcher.utter_message(json_message=markdown_formatting(text))
        return [UserUtteranceReverted(), FollowupAction(tracker.active_form.get('latest_action_name'))]
