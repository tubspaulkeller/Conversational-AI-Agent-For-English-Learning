from cgitb import text
from lib2to3.pgen2 import grammar
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted
import requests
import json
from fuzzywuzzy import process
import os
from dotenv import load_dotenv

load_dotenv()
user_score = {
    "points": 0,
    "stars": 0,
    "total_badges": 0,
    "tries": 0,  # nach jedem DP auf null setzen
    "last_question_correct": 0,
    "not_first_attempt": 0,
}

##########################################################################################
# Restart the conversation
##########################################################################################


class ActionRestart(Action):
    def name(self) -> Text:
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        user_score.update({}.fromkeys(user_score, 0))
        dispatcher.utter_message(text="Ich habe neu gestartet. 🤖")
        return [AllSlotsReset(), Restarted()]


############################################################################################################
##### Methods for user_scoring #####
# These methods are used by DP1, DP2 and DP3
############################################################################################################
def get_dp_inmemory_db(json_file):
    with open(json_file, "r") as jsonFile:
        return json.load(jsonFile)


def get_slots_for_dp(slots, slot_dp):
    return {k: v for k, v in slots.items() if k.startswith(slot_dp)}


def get_tries():
    return user_score["tries"]


def set_points(points):
    user_score["points"] += points
    user_score["last_question_correct"] = 1


def increase_tries():
    user_score["tries"] += 1


def resetTries():
    user_score["tries"] = 0


def reset_user_score():
    user_score.update({}.fromkeys(user_score, 0))

##### methods for evaluating users answer during quest #####


def evaluate_users_answer(solution, dp_n, name_of_slot, value, dispatcher, slots):

    if solution.lower() == value.lower():
        evaluate_scoring(dp_n, name_of_slot, dispatcher, slots)
        set_points(dp_n[name_of_slot]["points"])
        # check letzte Frage und gibt Gesamtpunkte aus

        if dp_n[name_of_slot]["question"] == dp_n["total_questions"]:
            finish_quiz(dispatcher, dp_n)
        else:
            resetTries()
        return {name_of_slot: value}
    # Users answer is wrong
    elif get_tries() < 1:  # User hat einen weiteren Versuch
        return evaluate_tries_of_user(name_of_slot, dispatcher)

    # say solution
    else:
        return give_solution(dp_n, name_of_slot, dispatcher, solution)


def evaluate_scoring(dp_n, name_of_slot, dispatcher, slots):
    # user got first question correct
    if dp_n[name_of_slot]["question"] == 1 and user_score["tries"] == 0:
        utter_first_quest_correct(dispatcher)
    # user got nte or last  question correct at first try
    elif user_score["tries"] == 0:
        # user has answered the last question and the previous ones correctly
        if "wrong_answer" not in slots.values() and dp_n[name_of_slot]["question"] == dp_n["total_questions"]:
            utter_last_and_previous_correct(dispatcher)

        # user has correctly answered the nth question and the previous ones
        elif "wrong_answer" not in slots.values():
            utter_nth_and_previuos_correct(dispatcher)

        # user has answered the last question correctly for the very first time, nevertheless in the first attempt
        elif dp_n[name_of_slot]["question"] == dp_n["total_questions"]:
            utter_last_question_users_first_time_correct_but_first_attempt(
                dispatcher)

        # user has answered a question correctly for the very first time, nevertheless in the first attempt
        else:
            utter_users_first_time_correct_but_first_attempt(dispatcher)

    # user did not answer the question correctly in the first attempt, but has already scored points
    elif user_score["points"] > 0 and user_score["tries"] > 0:
        # the question is the last
        if dp_n[name_of_slot]["question"] == dp_n["total_questions"]:
            utter_last_previous_correct_not_first_attempt(dispatcher)
        # the question is the nth
        else:
            utter_nth_previous_correct_not_first_attempt(dispatcher)

    # user answers a question correctly for the very first time, but needs several tries
    elif user_score["points"] == 0 and user_score["tries"] > 0:
        # the question is the last
        if dp_n[name_of_slot]["question"] == dp_n["total_questions"]:
            utter_last_quest_users_first_correct_not_first_attempt(dispatcher)
        # the question is the nth
        else:
            utter_nth_quest_user_first_correct_not_first_attempt(dispatcher)


def evaluate_tries_of_user(name_of_slot, dispatcher):
    user_score["not_first_attempt"] = 1
    increase_tries()
    utter_wrong_answer(dispatcher)

    return {name_of_slot: None}


def give_solution(dp_n, name_of_slot, dispatcher, solution):
    user_score["last_question_correct"] = 0
    utter_solution(dispatcher, solution)
    if dp_n[name_of_slot]["question"] == dp_n["total_questions"]:
        finish_quiz(dispatcher, dp_n)
    else:
        resetTries()

    return {name_of_slot: "wrong_answer"}


def finish_quiz(dispatcher, dp_n):
    if (user_score["points"] == 0):
        utter_finished_quiz_no_points(dispatcher)
    else:
        utter_finished_quiz_with_points(dispatcher, dp_n)
        if user_score["not_first_attempt"] == 0:
            utter_all_quest_correct_at_first_attempt(dp_n, dispatcher)
    reset_user_score()

 ##### Utter messages funtions #####


def utter_solution(dispatcher, solution):
    dispatcher.utter_message(
        text='Schade, leider ist die Lösung: %s' % solution)


def utter_wrong_answer(dispatcher):
    dispatcher.utter_message(response="utter_quest_wrong")


def utter_first_quest_correct(dispatcher):
    dispatcher.utter_message(response="utter_first_quest_correct")


def utter_last_and_previous_correct(dispatcher):
    dispatcher.utter_message(response="utter_last_and_previous_correct")


def utter_nth_and_previuos_correct(dispatcher):
    dispatcher.utter_message(response="utter_nth_and_previuos_correct")


def utter_last_question_users_first_time_correct_but_first_attempt(dispatcher):
    dispatcher.utter_message(
        response="utter_last_question_users_first_time_correct_but_first_attempt")


def utter_users_first_time_correct_but_first_attempt(dispatcher):
    dispatcher.utter_message(
        response="utter_users_first_time_correct_but_first_attempt")


def utter_last_previous_correct_not_first_attempt(dispatcher):
    dispatcher.utter_message(
        response="utter_last_previous_correct_not_first_attempt")


def utter_nth_previous_correct_not_first_attempt(dispatcher):
    dispatcher.utter_message(
        response="utter_nth_previous_correct_not_first_attempt")


def utter_last_quest_users_first_correct_not_first_attempt(dispatcher):
    dispatcher.utter_message(
        response="utter_last_quest_users_first_correct_not_first_attempt")


def utter_nth_quest_user_first_correct_not_first_attempt(dispatcher):
    dispatcher.utter_message(
        response="utter_nth_quest_user_first_correct_not_first_attempt")


def utter_finished_quiz_no_points(dispatcher):
    dispatcher.utter_message(text="Damit hast du das Quiz abgeschlossen. 🎉")


def utter_finished_quiz_with_points(dispatcher, dp_n):
    dispatcher.utter_message(
        text="Damit hast du das Quiz mit insgesamt %s von %s Punkten abgeschlossen. 🎉" % (user_score["points"], dp_n["total_points"]))


def utter_all_quest_correct_at_first_attempt(dp_n, dispatcher):
    dispatcher.utter_message(
        text="Du hast alle Fragen im ersten Versuch richtig beantwortet. 🏆")
    dispatcher.utter_message(image=dp_n["badge_naturtalent"])


############################################################################################################
##### DP1 #####
############################################################################################################


class ValidateDP1Form(FormValidationAction):

    def name(self) -> Text:
        # Unique identifier of the form"
        return "validate_dp1_form"

    def validate_dp1(name_of_slot):
        def validate_slot(
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


############################################################################################################
##### DP2 #####
############################################################################################################


class ValidateDP2Form(FormValidationAction):

    def name(self) -> Text:
        # Unique identifier of the form"
        return "validate_dp2_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()

        if tracker.slots.get("s_dp2_q4") == 'no':
            # there we will skip next slot
            updated_slots.remove("s_dp2_q5")
        return updated_slots

    def validate_s_dp2_q1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        value = slot_value
        if value == "Zusammenfassung":
            # TODO Reminder for utter as delays
            dispatcher.utter_message(response="utter_zusammenfassung_part1")
            dispatcher.utter_message(response="utter_zusammenfassung_part2")
            dispatcher.utter_message(response="utter_zusammenfassung_part3")
            dispatcher.utter_message(text="Ok, dann starte ich das Quiz. 🎮")
            return {"s_dp2_q1": value}
        elif value == "Quiz":
            dispatcher.utter_message(text="Ok, dann starte ich das Quiz. 🎮")
            return {"s_dp2_q1": value}
        else:
            return {"s_dp2_q1": None}

    def validate_s_dp2_q4(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        value = slot_value
        if value == "yes":
            self.utter_affirm_more_learning_quests(dispatcher)
            return {"s_dp2_q4": value}
        elif value == "no":
            self.utter_deny_more_learning_quests(dispatcher)
            return {"s_dp2_q4": value}
        else:
            return {"s_dp2_q4": None}

    @staticmethod
    def utter_affirm_more_learning_quests(dispatcher):
        dispatcher.utter_message(text="Gute Entscheidung!  😊")

    @staticmethod
    def utter_deny_more_learning_quests(dispatcher):
        dispatcher.utter_message(
            text="Ok, wir können dies sonst zu einem anderen Zeitpunkt üben. 😊")

    def validate_s_dp2_q5(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        return validate_grammar_for_user_answer(slot_value, "DP2.json", "s_dp2_q5", dispatcher, tracker)

    def validate_dp2(name_of_slot):
        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            dp_2 = get_dp_inmemory_db("DP2.json")
            solution = dp_2[name_of_slot]["solution"]
            slots = dict(tracker.slots)
            slots_dp2 = get_slots_for_dp(slots, 's_dp2_')
            return evaluate_users_answer(solution, dp_2, name_of_slot, value, dispatcher, slots_dp2)

        return validate_slot

    validate_s_dp2_q2 = validate_dp2(name_of_slot="s_dp2_q2")
    validate_s_dp2_q3 = validate_dp2(name_of_slot="s_dp2_q3")


############################################################################################################
##### DP3 #####
############################################################################################################

class ValidateDP3Form(FormValidationAction):

    def name(self) -> Text:
        # Unique identifier of the form"
        return "validate_dp3_form"

    def validate_s_dp3_q1(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        dp3 = get_dp_inmemory_db("DP3.json")
        self.utter_learn_goal(dispatcher, dp3, slot_value)
        return {"s_dp3_q1": slot_value}

    def validate_s_dp3_q2(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        if slot_value == "affirm":
            self.utter_affirm_learn_goal(dispatcher)
            return {"s_dp3_q2": "affirm"}
        elif slot_value == "deny":
            return {"s_dp3_q2": "deny"}

    def validate_dp3(name_of_slot):
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
##### Check Grammar #####
# these methods are use for DP2 and DP4
############################################################################################################

def validate_grammar_for_user_answer(value, json_file, name_of_slot, dispatcher, tracker):
    entities = value
    number_of_entities = len(entities)
    print("Debug", entities, number_of_entities)

    # check entities
    entities_list = get_dp_inmemory_db(json_file)
    if check_entities(number_of_entities, entities_list, name_of_slot, entities, dispatcher):
        return {name_of_slot: None}

    # get Userinput
    usertext = tracker.latest_message['text']
    # first letter of the word is capitalized
    usertext = usertext[0].upper() + usertext[1:]

    if not valid_grammar(usertext, dispatcher):
        return {name_of_slot: None}
    else:
        dispatcher.utter_message(response="utter_correct_answer_qn")
        return {name_of_slot: True}


def json_formatter(json_response):
    print(json.dumps(json_response, indent=4))


def grammar_check(user_input):
    url = "https://dnaber-languagetool.p.rapidapi.com/v2/check"

    payload = f"language=en-US&text={user_input}"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key":
        os.getenv('GRAMMAR_TOOL_KEY'),
        "X-RapidAPI-Host": "dnaber-languagetool.p.rapidapi.com",
        "motherTongue": "de"
    }

    response = requests.request("POST",
                                url,
                                data=payload,
                                headers=headers)
    json_formatter(response.json())
    return response.json()


def translate_to_german(grammar_error):

    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"
    payload = {"q": grammar_error, "source": "en", "target": "de"}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key":
        os.getenv('TRANSLATE_KEY'),
        "X-RapidAPI-Host": "deep-translate1.p.rapidapi.com"
    }

    response = requests.request("POST",
                                url,
                                json=payload,
                                headers=headers)
    json_formatter(response.json())
    return response.json()


def grammar_validation(grammar_response):
    suggestions = []
    if (len(grammar_response['matches']) > 0):
        if grammar_response['matches'][0]['message']:
            matches = grammar_response['matches'][0]['message']

            if len(grammar_response['matches'][0]['replacements']) > 0:
                for i, val in enumerate(grammar_response['matches'][0]
                                        ['replacements']):
                    print(i, ". suggestion: ", val['value'])
                    suggestions.append(val['value'])

        print(matches)
        return matches, suggestions

    print("No grammar errors found")
    return None, None


def check_missing_entities(name_of_slot, entities, entities_list):
    for entity in entities:
        # allow typos for entities till a certain threshold (80%)
        fuzzy_entity = process.extractOne(
            entity, entities_list[name_of_slot]["entities"])
        if not fuzzy_entity[1] > 80:
            return True
    return False


def check_entities(number_of_entities, entities_list, name_of_slot, entities, dispatcher):
    if number_of_entities != entities_list[name_of_slot]["quantity"] | check_missing_entities(name_of_slot, entities, entities_list):
        dispatcher.utter_message(
            text="You have not answered the question correctly. Please try again.")
        return True
    else:
        return False


def valid_grammar(usertext, dispatcher):
    grammar_response = grammar_check(usertext)
    grammar_error, grammar_suggestion = grammar_validation(grammar_response)
    if check_grammar_error(grammar_error, dispatcher, grammar_suggestion):
        return False
    else:
        return True


def check_grammar_error(grammar_error, dispatcher, grammar_suggestion):
    if grammar_error:
        dispatcher.utter_message(response="utter_grammar_error")
        dispatcher.utter_message(text=grammar_error)
        if grammar_suggestion:
            for i, val in enumerate(grammar_suggestion):
                dispatcher.utter_message(
                    text=f"{i}. suggestion: {val}")
                if i == 4:
                    break
        return True
    else:
        return False


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

            return validate_grammar_for_user_answer(value, "DP4.json", name_of_slot, dispatcher, tracker)

        return validate_slot

    validate_s_dp4_q1 = validate_dp4(name_of_slot="s_dp4_q1")
    validate_s_dp4_q2 = validate_dp4(name_of_slot="s_dp4_q2")
    validate_s_dp4_q3 = validate_dp4(name_of_slot="s_dp4_q3")
    validate_s_dp4_q4 = validate_dp4(name_of_slot="s_dp4_q4")
    validate_s_dp4_q5 = validate_dp4(name_of_slot="s_dp4_q5")

############################################################################################################
##### DP5 #####
############################################################################################################


class ValidateDP5Form(FormValidationAction):

    def name(self) -> Text:
        # Unique identifier of the form"
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

        define_learn_goal("s_dp3_v_q1", value, dispatcher)
        return {"s_dp3_v_q1": value}

    def validate_s_dp3_v_q2(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
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
        return {"s_dp3_v_q6": value}

    def validate_s_dp3_v_end(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_v_end": value}

    def validate_dp3voc(name_of_slot):
        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
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
        # Unique identifier of the form"
        return "validate_dp3_form_gram"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
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
        define_learn_goal("s_dp3_g_q1", value, dispatcher)
        return {"s_dp3_g_q1": value}

    def validate_s_dp3_g_q2(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_g_q2": value}

    def validate_s_dp3_g_q4(self,
                            value: Text,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: Dict[Text, Any],
                            ) -> Dict[Text, Any]:
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
        return {"s_dp3_g_q6": value}

    def validate_s_dp3_g_end(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_g_end": value}

    def validate_dp3gram(name_of_slot):

        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
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
