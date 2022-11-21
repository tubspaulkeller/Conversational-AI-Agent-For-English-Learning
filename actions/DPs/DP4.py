from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted

# imports from different files
from actions.helper.check_grammar_of_users_input import validate_grammar_for_user_answer

############################################################################################################
##### DP4 #####
############################################################################################################


class ValidateDP4Form(FormValidationAction):

    def name(self) -> Text:
        # Unique identifier of the form"
        return "validate_dp4_form"

    def validate_dp4(name_of_slot):
 
        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            """ The slots corresponding to the users answer for question of DP4 are validated here. 
            The user input is checked for grammar errors. Therefore a function is called from the helper folder"""

            return validate_grammar_for_user_answer(value, "DP4.json", name_of_slot, dispatcher, tracker)

        return validate_slot

    validate_s_dp4_q1 = validate_dp4(name_of_slot="s_dp4_q1")
    validate_s_dp4_q2 = validate_dp4(name_of_slot="s_dp4_q2")
    validate_s_dp4_q3 = validate_dp4(name_of_slot="s_dp4_q3")
    validate_s_dp4_q4 = validate_dp4(name_of_slot="s_dp4_q4")
    validate_s_dp4_q5 = validate_dp4(name_of_slot="s_dp4_q5")