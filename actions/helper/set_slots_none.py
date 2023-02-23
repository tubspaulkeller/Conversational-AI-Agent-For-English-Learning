from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.helper.debug import debug
from actions.gamification.handle_user_scoring import user_score
from actions.common.common import get_dp_inmemory_db


class ActionGetSkills(Action):
    def name(self) -> Text:
        return "action_set_slots_none"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("s_lg_0", None), SlotSet("s_lg_1", None), SlotSet("s_lg_2", None), SlotSet("s_lg_3", None), SlotSet("s_lg_4", None), FollowupAction("learngoals_form")]
