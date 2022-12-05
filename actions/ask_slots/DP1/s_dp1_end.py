from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.gamification.evaluate_user_scoring import finish_quiz
from actions.common.common import get_dp_inmemory_db


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp1_end"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ DP1 is finished, the user can choose a different DP """
        dp_1 = get_dp_inmemory_db("DP1.json")
        finish_quiz(dispatcher, "s_dp1_q", dp_1)
        return [SlotSet("s_dp1_end", "end_of_dp1_form"), FollowupAction("action_set_reminder_set_dp")]
