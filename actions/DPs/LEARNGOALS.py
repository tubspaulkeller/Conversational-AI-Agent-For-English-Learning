from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted

# imports from different files
from datetime import datetime, date

from actions.common.common import get_dp_inmemory_db, get_slots_for_dp
from actions.helper.learn_goal import generate_learn_goal, is_user_accepting_learn_goal, customize_learn_goal

############################################################################################################
##### DP4 #####
############################################################################################################


class ValidateLearngoalsForm(FormValidationAction):

    def name(self) -> Text:
        # Unique identifier of the form
        return "validate_learngoals_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        """
        updates the order of the slots that should be requested
        """
        updated_slots = domain_slots.copy()
        if tracker.slots.get("s_lg_1") == 'affirm':
            # there we will skip next slot
            updated_slots.remove("s_lg_2")
        return updated_slots

    def validate_s_lg_0(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:

        return generate_learn_goal('s_lg_0', dispatcher, slot_value,
                                   'Das klingt interessant! Ich würde daraus folgendes Lernziel forumlieren:', 'Ende des Jahres', " ")

    def validate_s_lg_1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        return is_user_accepting_learn_goal('s_lg_1', slot_value, dispatcher)

    def validate_s_lg_2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        return customize_learn_goal('s_lg_2', 's_lg_0', 's_lg_1', dispatcher, tracker)

    def validate_learngoals(name_of_slot):
        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            """validate learngoals"""
            print("test", value)
            return {name_of_slot: value}
        return validate_slot

    validate_s_lg_3 = validate_learngoals(name_of_slot="s_lg_3")
    validate_s_lg_4 = validate_learngoals(name_of_slot="s_lg_4")
