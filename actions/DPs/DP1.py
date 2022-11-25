from cgitb import text
from lib2to3.pgen2 import grammar
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted

# imports from different files
from actions.gamification.evaluate_user_scoring import evaluate_users_answer
from actions.common.common import get_dp_inmemory_db, get_slots_for_dp
from actions.common.slack import get_group_member, get_user

############################################################################################################
##### DP1 #####
############################################################################################################


class ValidateDP1Form(FormValidationAction):
    def name(self) -> Text:
        # Unique identifier of the form"
        return "validate_dp1_form"

    def validate_dp1(name_of_slot):
        """This function validates the slots corresponding to the users answer for question of DP1"""

        async def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            # # GROUP CHANNEL
            # u_id = ""
            # name = ""
            # for event in tracker.events:
            #     if event['event'] == 'user':
            #         user_ids = event['metadata'].get('users')

            # for id in reversed(user_ids):
            #     print('DEBUG: user id', id)
            #     u_id, name = await get_user(id)
            #     break
            # print("USER ID", u_id)
            # print("NAME", name)
            dp_1 = get_dp_inmemory_db("DP1.json")
            solution = dp_1[name_of_slot]["solution"]
            slots = dict(tracker.slots)
            slots_dp1 = get_slots_for_dp(slots, 's_dp1_')
            return evaluate_users_answer(solution, dp_1, name_of_slot, value, dispatcher, slots_dp1)
        return validate_slot

    validate_s_dp1_q1 = validate_dp1(name_of_slot="s_dp1_q1")
    validate_s_dp1_q2 = validate_dp1(name_of_slot="s_dp1_q2")
    validate_s_dp1_q3 = validate_dp1(name_of_slot="s_dp1_q3")
