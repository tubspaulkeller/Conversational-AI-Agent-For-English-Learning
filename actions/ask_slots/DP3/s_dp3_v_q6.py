from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType

from actions.gamification.evaluate_user_scoring import finish_quiz
from actions.common.common import get_dp_inmemory_db
from actions.helper.learn_goal import generate_learn_goal, is_user_accepting_learn_goal, customize_learn_goal, get_key_for_json
from actions.DPs.DP3 import utter_shorter_learntime, utter_longer_learntime


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp3_v_q6"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ If the user want to change his goal, the user can choose a different goal. """
        value = tracker.get_slot("s_dp3_v_q5")
        dp_3 = get_dp_inmemory_db("DP3.json")
        topic = tracker.slots.get("s_dp3_v_q1")
        goal = tracker.get_slot("s_dp3_v_customize_goal")
        if goal == None:
            key, pretext, deadline = get_key_for_json("s_dp3_v_q1", tracker)
            goal = dp_3["s_dp3_v_q1"]["goal"][topic] % "2000"
        if value == "shorter_learntime":
            utter_shorter_learntime(
                dispatcher, "Vokabelquiz", goal)
        elif value == "longer_learntime":
            utter_longer_learntime(
                dispatcher, "Vokabelquiz", goal)
        dispatcher.utter_message(response="utter_s_dp3_v_q6")
        return []
