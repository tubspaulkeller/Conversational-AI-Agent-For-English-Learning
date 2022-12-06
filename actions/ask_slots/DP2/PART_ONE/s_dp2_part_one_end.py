from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.gamification.evaluate_user_scoring import finish_quiz
from actions.common.common import get_dp_inmemory_db


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp2_part_one_end"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        dp_2 = get_dp_inmemory_db("DP2.json")
        finish_quiz(dispatcher, "s_dp2_q", dp_2)
        return [SlotSet("s_dp2_part_one_end", "end_part_one_of_dp2_form"), FollowupAction("dp2_application_tasks_form")]
