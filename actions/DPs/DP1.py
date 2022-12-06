from cgitb import text
from lib2to3.pgen2 import grammar
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted

# imports from different files
from actions.gamification.evaluate_user_scoring import evaluate_users_answer
from actions.common.common import get_dp_inmemory_db, get_slots_for_dp

############################################################################################################
##### DP1 #####
############################################################################################################


class ValidateDP1Form(FormValidationAction):
    def name(self) -> Text:
        # Unique identifier of the form"
        return "validate_dp1_form"

    def validate_s_dp1_q0(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        return {"s_dp1_q0": slot_value}

    def validate_s_dp1_evaluation(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict",) -> Dict[Text, Any]:
        return {"s_dp1_evaluation": slot_value}

    def validate_dp1(name_of_slot):
        """This function validates the slots corresponding to the users answer for question of DP1"""

        async def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            dp_1 = get_dp_inmemory_db("DP1.json")
            solution = dp_1[name_of_slot]["solution"]
            slots = dict(tracker.slots)
            slots_dp1 = get_slots_for_dp(slots, 's_dp1_')
            return evaluate_users_answer(solution, dp_1, name_of_slot, value, dispatcher, slots_dp1)
        return validate_slot

    validate_s_dp1_q1 = validate_dp1(name_of_slot="s_dp1_q1")
    validate_s_dp1_q2 = validate_dp1(name_of_slot="s_dp1_q2")
    validate_s_dp1_q3 = validate_dp1(name_of_slot="s_dp1_q3")
