from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted
import requests
import json
from datetime import datetime, date

# imports from different files
from actions.gamification.evaluate_user_scoring import evaluate_users_answer
from actions.helper.check_grammar_of_users_input import validate_grammar_for_user_answer
from actions.common.common import get_dp_inmemory_db, get_slots_for_dp
from actions.helper.learn_goal import generate_learn_goal, is_user_accepting_learn_goal, customize_learn_goal, get_key_for_json

############################################################################################################
##### DP3 #####
############################################################################################################


class ValidateDP3Form(FormValidationAction):

    def name(self) -> Text:
        # Unique identifier of the form"
        return "validate_dp3_form"

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
        if tracker.slots.get("s_dp3_q2") == 'affirm':
            # there we will skip next slot
            updated_slots.remove("s_dp3_date")
            updated_slots.remove("s_dp3_date_confirm")
        return updated_slots

    def validate_s_dp3_q1(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        """ validates the first question of DP3. The user can choose his learning goal """
        return generate_learn_goal('s_dp3_q1', 's_dp3_q1', dispatcher, slot_value,
                                   'Das klingt interessant! Ich würde daraus folgendes Lernziel forumlieren:', 'Ende des Jahres', " ")

    def validate_s_dp3_q2(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        """ validates the second question of DP3. The user can affirm or deny his learning goal """
        return is_user_accepting_learn_goal('s_dp3_q2', 'oberziel', slot_value, dispatcher)

    def validate_s_dp3_date(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        """ validates the date of the third question of DP3. The user can choose a date for his learning goal """
        return customize_learn_goal('s_dp3_date', 's_dp3_q1', 's_dp3_q2', dispatcher, tracker, "s_dp3_q1")

    def validate_dp3(name_of_slot):
        """validates the following questions of DP3. The answers has not be checked at all bcs they are checked at different actions. """

        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            return {name_of_slot: value}
        return validate_slot

############################################################################################################

    validate_s_dp3_date_confirm = validate_dp3(
        name_of_slot="s_dp3_date_confirm")
    validate_s_dp3_q3 = validate_dp3(name_of_slot="s_dp3_q3")
    validate_s_dp3_q4 = validate_dp3(name_of_slot="s_dp3_q4")


############################################################################################################
##### DP3 voc #####
############################################################################################################


class ValidateDP3VOCForm(FormValidationAction):

    def name(self) -> Text:
        # Unique identifier of the form"
        return "validate_dp3_form_voc"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        """ updates the required slots of the form """
        updated_slots = domain_slots.copy()
        if tracker.slots.get("s_dp3_v_q5") == 'deny':
            # there we will skip next slot
            updated_slots.remove("s_dp3_v_q6")
        if tracker.slots.get("s_dp3_v_q2") == 'affirm':
            # there we will skip next slot
            updated_slots.remove("s_dp3_v_customize_goal")
           # updated_slots.remove("s_dp3_v_start_button")
        return updated_slots

    def validate_s_dp3_v_q1(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """ validates the first question of DP3. The user can choose his learning goal """

        # define_learn_goal("s_dp3_v_q1", value, dispatcher)
        key, pretext, deadline = get_key_for_json("s_dp3_v_q1", tracker)

        return generate_learn_goal(key, 's_dp3_v_q1', dispatcher, value,
                                   pretext, deadline, " ")

    def validate_s_dp3_v_q2(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """ validates the second question of DP3. It does not need to be validated bcs it is checked at the action """
        return is_user_accepting_learn_goal('s_dp3_v_q2', 'vokabelziel', value, dispatcher)

    def validate_s_dp3_v_customize_goal(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        """ validates the second question of DP3. The user can affirm or deny his learning goal """
        return customize_learn_goal('s_dp3_v_customize_goal', 's_dp3_v_q1', tracker.get_slot('s_dp3_v_q2'), dispatcher, tracker, "s_dp3_v_q1")

    def validate_s_dp3_v_evaluation(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_v_evaluation": value}

    def validate_s_dp3_v_q4(self,
                            value: Text,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: Dict[Text, Any],
                            ) -> Dict[Text, Any]:
        if value == "deny":
            utter_problem_of_learn_process(dispatcher)
        elif value == "affirm":
            utter_affirm_learn_process(dispatcher)
        return {"s_dp3_v_q4": value}

    def validate_s_dp3_v_q5(self,
                            value: Text,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: Dict[Text, Any],
                            ) -> Dict[Text, Any]:
        """ validates the fifth question of DP3. The user can change his learning goal """
        if value == "shorter_learntime":
            utter_shorter_learntime(
                dispatcher, "Vobabelquiz", "2000 neuen Wörtern")
        elif value == "longer_learntime":
            utter_longer_learntime(
                dispatcher, "Vobabelquiz", "2000 neuen Wörtern")
        return {"s_dp3_v_q5": value}

    def validate_s_dp3_v_q6(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """ slot does not need to be validated bcs it is checked at the action """
        return {"s_dp3_v_q6": value}

    def validate_s_dp3_v_end(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_v_end": value}

    def validate_s_dp3_activate_form(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_activate_form": value}

    def validate_s_dp3_display_form_button(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_display_form_button": "DISPLAYED"}

    def validate_s_dp3_v_start_button(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_v_start_button": value}

    def validate_dp3voc(name_of_slot):
        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            """ validates the multiple choice questions of DP3. The user can choose one of the given answers """
            dp_3 = get_dp_inmemory_db("DP3.json")
            solution = dp_3[name_of_slot]["solution"]
            slots = dict(tracker.slots)
            slots_dp3 = get_slots_for_dp(slots, 's_dp3_v_')
            return evaluate_users_answer(solution, dp_3, name_of_slot, value, dispatcher, slots_dp3, "dp3")
        return validate_slot

    validate_s_dp3_v_q3_0 = validate_dp3voc(name_of_slot="s_dp3_v_q3_0")
    validate_s_dp3_v_q3_1 = validate_dp3voc(name_of_slot="s_dp3_v_q3_1")
    validate_s_dp3_v_q3_2 = validate_dp3voc(name_of_slot="s_dp3_v_q3_2")
    validate_s_dp3_v_q3_3 = validate_dp3voc(name_of_slot="s_dp3_v_q3_3")
    validate_s_dp3_v_q3_4 = validate_dp3voc(name_of_slot="s_dp3_v_q3_4")
    validate_s_dp3_v_q3_5 = validate_dp3voc(name_of_slot="s_dp3_v_q3_5")


############################################################################################################
##### DP3 gram #####
############################################################################################################


class ValidateDP3GRAMForm(FormValidationAction):

    def name(self) -> Text:
        # Unique identifier of the form
        return "validate_dp3_form_gram"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        """ updates the required slots of the form """
        updated_slots = domain_slots.copy()
        if tracker.slots.get("s_dp3_g_q5") == 'deny':
            updated_slots.remove("s_dp3_g_q6")

        if tracker.slots.get("s_dp3_g_q2") == 'affirm':
            # there we will skip next slot
            updated_slots.remove("s_dp3_g_customize_goal")
            # updated_slots.remove("s_dp3_g_start_button")
        return updated_slots

    def validate_s_dp3_g_q1(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """ the user can choose his learning goal """
        # define_learn_goal("s_dp3_g_q1", value, dispatcher)

        key, pretext, deadline = get_key_for_json("s_dp3_g_q1", tracker)

        return generate_learn_goal(key, 's_dp3_g_q1', dispatcher, value,
                                   pretext, deadline, " ")

    def validate_s_dp3_g_q2(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """ validates the second question of DP3. It does not need to be validated bcs it is checked at the action """
        return is_user_accepting_learn_goal('s_dp3_g_q2', 'grammatikziel', value, dispatcher)

    def validate_s_dp3_g_customize_goal(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        """ validates the second question of DP3. The user can affirm or deny his learning goal """
        return customize_learn_goal('s_dp3_g_customize_goal', 's_dp3_g_q1', tracker.get_slot('s_dp3_g_q2'), dispatcher, tracker, "s_dp3_g_q1")

    def validate_s_dp3_g_evaluation(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_g_evaluation": value}

    def validate_s_dp3_g_q4(self,
                            value: Text,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: Dict[Text, Any],
                            ) -> Dict[Text, Any]:
        """ user can choose if he wants to change his learning goal """
        if value == "deny":
            utter_problem_of_learn_process(dispatcher)
        elif value == "affirm":
            utter_affirm_learn_process(dispatcher)
        return {"s_dp3_g_q4": value}

    def validate_s_dp3_g_q5(self,
                            value: Text,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: Dict[Text, Any],
                            ) -> Dict[Text, Any]:
        """ user can change his learning goal """
        if value == "shorter_learntime":
            utter_shorter_learntime(
                dispatcher, "Grammatikquiz", "zwei Zeitformen")
        elif value == "longer_learntime":
            utter_longer_learntime(
                dispatcher, "Grammatikquiz", "zwei Zeitformen")
        return {"s_dp3_g_q5": value}

    def validate_s_dp3_g_q6(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """ does not need to be validated bcs it is checked at different action """
        return {"s_dp3_g_q6": value}

    def validate_s_dp3_display_form_button(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_display_form_button": "DISPLAYED"}

    def validate_s_dp3_g_end(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_g_end": "END"}

    def validate_s_dp3_activate_form(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_activate_form": value}

    def validate_s_dp3_g_start_button(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_g_start_button": value}

    def validate_dp3gram(name_of_slot):

        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            """ validates the multiple choice questions of DP3. The user can choose one of the given answers """
            dp_3 = get_dp_inmemory_db("DP3.json")
            solution = dp_3[name_of_slot]["solution"]
            slots = dict(tracker.slots)
            slots_dp3 = get_slots_for_dp(slots, 's_dp3_g_')
            return evaluate_users_answer(solution, dp_3, name_of_slot, value, dispatcher, slots_dp3, "dp3")

        return validate_slot

    validate_s_dp3_g_q3_0 = validate_dp3gram(name_of_slot="s_dp3_g_q3_0")
    validate_s_dp3_g_q3_1 = validate_dp3gram(name_of_slot="s_dp3_g_q3_1")
    validate_s_dp3_g_q3_2 = validate_dp3gram(name_of_slot="s_dp3_g_q3_2")
    validate_s_dp3_g_q3_3 = validate_dp3gram(name_of_slot="s_dp3_g_q3_3")
    validate_s_dp3_g_q3_4 = validate_dp3gram(name_of_slot="s_dp3_g_q3_4")
    validate_s_dp3_g_q3_5 = validate_dp3gram(name_of_slot="s_dp3_g_q3_5")


############################################################################################################
    #### utter_messages for DP3_vocabels and DP3_grammar #####
############################################################################################################
def define_learn_goal(slot_value, value, dispatcher):
    dp3 = get_dp_inmemory_db("DP3.json")
    learn_goal = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "text": "%s" % dp3[slot_value]["goal"][value],
                    "type": "mrkdwn"
                }
            }
        ]
    }
    dispatcher.utter_message(json_message=learn_goal)


def utter_problem_of_learn_process(dispatcher):
    dispatcher.utter_message(
        text="Okay, vielleicht liegt es an unserem Lernprozess.")


def utter_affirm_learn_process(dispatcher):
    dispatcher.utter_message(text="Das freut mich zu hören!")


def utter_shorter_learntime(dispatcher, quest, goal):
    dispatcher.utter_message(
        text="Oh, ich verstehe. Was hälst du davon, wenn wir das %s von 50 auf 35 Fragen verkürzen? So könntest du dein Ziel von %s trotzdem noch erreichen." % (quest, goal))


def utter_longer_learntime(dispatcher, quest, goal):
    dispatcher.utter_message(
        text="Cool, dann erhöhren wir das %s von 50 auf 60 Fragen. So kannst du dein Ziel von %s sogar übertreffen!" % (quest, goal))
