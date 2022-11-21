from cgitb import text
from lib2to3.pgen2 import grammar
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted
import requests
import json
from fuzzywuzzy import process

# imports from different files
from actions.gamification.evaluate_user_scoring import evaluate_users_answer
from actions.helper.check_grammar_of_users_input import validate_grammar_for_user_answer
from actions.common.common import get_dp_inmemory_db, get_slots_for_dp

############################################################################################################
##### DP3 #####
############################################################################################################

class ValidateDP3Form(FormValidationAction):

    def name(self) -> Text:
        # Unique identifier of the form"
        return "validate_dp3_form"

    def validate_s_dp3_q1(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        """ validates the first question of DP3. The user can choose his learning goal """
        dp3 = get_dp_inmemory_db("DP3.json")
        self.utter_learn_goal(dispatcher, dp3, slot_value)
        return {"s_dp3_q1": slot_value}

    def validate_s_dp3_q2(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        """ validates the second question of DP3. The user can affirm or deny his learning goal """
        if slot_value == "affirm":
            self.utter_affirm_learn_goal(dispatcher)
            return {"s_dp3_q2": "affirm"}
        elif slot_value == "deny":
            return {"s_dp3_q2": "deny"}

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
        #### utter_messages for DP3 #####
############################################################################################################

    @staticmethod
    def utter_affirm_learn_goal(dispatcher):
        dispatcher.utter_message(response="utter_affirm_learn_goal")

    @staticmethod
    def utter_learn_goal(dispatcher, dp_n, value):
        dispatcher.utter_message(
            text="Das klingt interessant! Ich würde daraus folgendes Lernziel forumlieren: %s" % dp_n["s_dp3_q1"]["goal"][value])

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
        return updated_slots

    def validate_s_dp3_v_q1(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """ validates the first question of DP3. The user can choose his learning goal """

        define_learn_goal("s_dp3_v_q1", value, dispatcher)
        return {"s_dp3_v_q1": value}

    def validate_s_dp3_v_q2(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """ validates the second question of DP3. It does not need to be validated bcs it is checked at the action """
        return {"s_dp3_v_q2": value}

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
        """ slot does not need to be validated bcs it is checked at the action """
        return {"s_dp3_v_end": value}

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
            return evaluate_users_answer(solution, dp_3, name_of_slot, value, dispatcher, slots_dp3)
        return validate_slot

    validate_s_dp3_v_q3 = validate_dp3voc(name_of_slot="s_dp3_v_q3")

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
        return updated_slots

    def validate_s_dp3_g_q1(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """ the user can choose his learning goal """
        define_learn_goal("s_dp3_g_q1", value, dispatcher)
        return {"s_dp3_g_q1": value}

    def validate_s_dp3_g_q2(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """ does not need to be validated bcs it is checked at different action """
        return {"s_dp3_g_q2": value}

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

    def validate_s_dp3_g_end(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """ does not need to be validated bcs it is checked at different action """
        return {"s_dp3_g_end": value}

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
            return evaluate_users_answer(solution, dp_3, name_of_slot, value, dispatcher, slots_dp3)

        return validate_slot

    validate_s_dp3_g_q3 = validate_dp3gram(name_of_slot="s_dp3_g_q3")


############################################################################################################
    #### utter_messages for DP3_vocabels and DP3_grammar #####
############################################################################################################
def define_learn_goal(slot_value, value, dispatcher):
    dp3 = get_dp_inmemory_db("DP3.json")
    dispatcher.utter_message(
        text="Ich würde daraus folgendes Lernziel forumlieren: %s" % dp3[slot_value][value])


def utter_problem_of_learn_process(dispatcher):
    dispatcher.utter_message(
        text="Okay, vielleicht liegt es an unserem Lernprozess.")


def utter_affirm_learn_process(dispatcher):
    dispatcher.utter_message(text="Das freut mich zu hören!")


def utter_shorter_learntime(dispatcher, quest, goal):
    dispatcher.utter_message(
        text="Oh, ich verstehe. Was hälst du davon, wenn wir das %s von 50 auf 35 Fragen verkürzen? So könntest du dein Ziel von %s bis zum Ende des Jahres trotzdem noch erreichen." % (quest, goal))


def utter_longer_learntime(dispatcher, quest, goal):
    dispatcher.utter_message(
        text="Cool, dann erhöhren wir das %s von 50 auf 60 Fragen. So kannst du dein Ziel von %s bis zum Ende des Jahres sogar übertreffen!" % (quest, goal))
