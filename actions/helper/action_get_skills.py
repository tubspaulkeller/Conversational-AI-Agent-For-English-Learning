from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.helper.debug import debug
from actions.gamification.handle_user_scoring import user_score
from actions.common.common import get_dp_inmemory_db, markdown_formatting, get_skills_text
lets_go_button = [
    {'title': "zurück", 'payload': '/i_lets_go{\"e_lets_go\":\"LETS_GO\"}'}]


class ActionGetSkills(Action):
    def name(self) -> Text:
        return "action_get_skills"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = get_skills_text()
        dispatcher.utter_message(json_message=markdown_formatting(text))

        # dispatcher.utter_message(
        #   text=" ", buttons=lets_go_button)
        return [SlotSet("s_get_dp_form", None), SlotSet("s_set_next_form", None), FollowupAction("get_dp_form")]
