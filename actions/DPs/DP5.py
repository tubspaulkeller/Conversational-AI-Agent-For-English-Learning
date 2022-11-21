from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType

############################################################################################################
##### DP5 #####
############################################################################################################


class ValidateDP5Form(FormValidationAction):

    def name(self) -> Text:
        # Unique identifier of the form
        return "validate_dp5_form"

    def validate_dp5(name_of_slot):

        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            print("val", value)
            return {name_of_slot: None}

        return validate_slot

    validate_s_dp5_q1 = validate_dp5(name_of_slot="s_dp5_q1")