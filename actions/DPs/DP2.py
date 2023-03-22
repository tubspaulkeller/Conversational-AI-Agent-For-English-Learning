from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted


# imports from different files
from actions.helper.check_grammar_of_users_input import validate_grammar_for_user_answer
from actions.gamification.evaluate_user_scoring import evaluate_users_answer
from actions.common.common import get_dp_inmemory_db, get_slots_for_dp

############################################################################################################
##### DP2 #####
############################################################################################################


class ValidateDP2Form(FormValidationAction):

    def name(self) -> Text:
        # Unique identifier of the form
        return "validate_dp2_form"

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

        if tracker.slots.get("s_dp2_q1") == 'Quiz':
            # there we will skip next slot
            updated_slots.remove("s_dp2_q1_2")
        return updated_slots

    def validate_s_dp2_q0(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        return {"s_dp2_q0": slot_value}

    def validate_s_dp2_evaluation(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        return {"s_dp2_evaluation": slot_value}

    def validate_s_dp2_q1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        value = slot_value
        if value == "Zusammenfassung":
            dispatcher.utter_message(response="utter_zusammenfassung")
            return {"s_dp2_q1": value}
        elif value == "Quiz":
            dispatcher.utter_message(text="Ok, dann starte ich das Quiz. 🎮")
            return {"s_dp2_q1": value}
        else:
            return {"s_dp2_q1": None}

    def validate_s_dp2_q1_2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        return {"s_dp2_q1_2": slot_value}

    def validate_dp2(name_of_slot):
        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            """ validate the slots multiple choice questions of DP2. The user input is compared to the correct answer in the json file.
            If the user input is correct, the slot is filled with the correct answer. If the user input is incorrect, the slot is filled with None.
            """
            dp_2 = get_dp_inmemory_db("DP2.json")
            solution = dp_2[name_of_slot]["solution"]
            slots = dict(tracker.slots)
            slots_dp2 = get_slots_for_dp(slots, 's_dp2_')
            return evaluate_users_answer(solution, dp_2, name_of_slot, value, dispatcher, slots_dp2, "dp2")

        return validate_slot

    validate_s_dp2_q2 = validate_dp2(name_of_slot="s_dp2_q2")
    validate_s_dp2_q3 = validate_dp2(name_of_slot="s_dp2_q3")
    validate_s_dp2_q4 = validate_dp2(name_of_slot="s_dp2_q4")
    validate_s_dp2_q5 = validate_dp2(name_of_slot="s_dp2_q5")
    validate_s_dp2_q6 = validate_dp2(name_of_slot="s_dp2_q6")
    validate_s_dp2_q7 = validate_dp2(name_of_slot="s_dp2_q7")
    validate_s_dp2_q8 = validate_dp2(name_of_slot="s_dp2_q8")


class ValidateDP2ApplicationTasksForm(FormValidationAction):

    def name(self) -> Text:
        # Unique identifier of the form
        return "validate_dp2_application_tasks_form"

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
        if tracker.slots.get("s_dp2_at_q1") == 'no':
            # there we will skip next slot
            updated_slots.remove("s_dp2_at_q2")
            updated_slots.remove("s_dp2_at_q3")
            updated_slots.remove("s_dp2_at_q4")
        return updated_slots

    def validate_s_dp2_at_q1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        # validates the slot of the fourth question of DP2
        value = slot_value
        if value == "yes":
            self.utter_affirm_more_learning_quests(dispatcher)
            return {"s_dp2_at_q1": value}
        elif value == "no":
            self.utter_deny_more_learning_quests(dispatcher)
            return {"s_dp2_at_q1": value}
        else:
            return {"s_dp2_at_q1": None}

    @staticmethod
    def utter_affirm_more_learning_quests(dispatcher):
        dispatcher.utter_message(text="Gute Entscheidung!  😊")

    @staticmethod
    def utter_deny_more_learning_quests(dispatcher):
        dispatcher.utter_message(
            text="Ok, wir können dies sonst zu einem anderen Zeitpunkt üben. 😊")

    def validate_dp2_application_tasks_form(name_of_slot):

        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            print("Start validation of slot: ", name_of_slot)
            return validate_grammar_for_user_answer(value, "DP2.json", name_of_slot, dispatcher, tracker)

        return validate_slot

    validate_s_dp2_at_q2 = validate_dp2_application_tasks_form(
        name_of_slot="s_dp2_at_q2")
    validate_s_dp2_at_q3 = validate_dp2_application_tasks_form(
        name_of_slot="s_dp2_at_q3")

    validate_s_dp2_at_q4 = validate_dp2_application_tasks_form(
        name_of_slot="s_dp2_at_q4")
