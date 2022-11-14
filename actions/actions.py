from cgitb import text
from lib2to3.pgen2 import grammar
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted
import requests
import json
from fuzzywuzzy import process
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
def getTries():
    return user_score["tries"]


def increaseTries():
    user_score["tries"] += 1


def resetTries():
    user_score["tries"] = 0


def resetUserPoints():
    user_score.update({}.fromkeys(user_score, 0))

##### methods for scoring #####


def evaluate_users_answer(solution, dp_n, name_of_slot, value, dispatcher):

    if solution.lower() == value.lower():
        evaluate_scoring(dp_n, name_of_slot, dispatcher)
        return {name_of_slot: value}
    # Users answer is wrong
    elif getTries() < 1:  # User hat einen weiteren Versuch
        return evaluate_tries_of_user(dp_n, name_of_slot, dispatcher)

    # say solution
    else:
        return give_solution(dp_n, name_of_slot, dispatcher, solution)


def evaluate_scoring(dp_n, name_of_slot):
    # user got first question correct
    if dp_n[name_of_slot]["question"] == 1 & user_score["tries"] == 0:
        first_quest_correct(dispatcher)
    # user got nte question correct
    if dp_n[name_of_slot]["question"] < dp_n["total_questions"]:

        # user hat die Fragen weiterhin im ersten richtig Versuch beantwortet

        # user hat die vorherige Frage nicht im ersten richtig Versuch beantwortet, diese aber schon

        # user hat diese Frage nicht im ersten Versuch richtig beantwortet, aber hat schon Punkte erzielt

        # dies ist die aller erste Frage, die der User richtig beantwortet

        # user hat die aller letzte Frage richtig beantwortet
    if dp_n[name_of_slot]["question"] == dp_n["total_questions"]:
        # user hat die Fragen weiterhin im ersten richtig Versuch beantwortet

        # user hat schon vorherige Punkte erzielt

        # user hat die letzte Frage als einziges richtig beantwortet


def evaluate_tries_of_user(name_of_slot, dispatcher):
    user_score["not_first_attempt"] = 1
    dispatcher.utter_message(response="utter_dp1_wrong")
    increaseTries()
    print("user_score", user_score)
    return {name_of_slot: None}


def give_solution(dp_n, name_of_slot, dispatcher, solution):
    user_score["last_question_correct"] = 0
    dispatcher.utter_message(
        text='Schade, leider ist die Lösung: %s' % solution)
    if dp_n[name_of_slot]["question"] == dp_n["total_questions"]:
        finish_quiz(dispatcher, dp_n)
    else:
        resetTries()
    print("user_score", user_score)
    return {name_of_slot: False}


def first_quest_correct(dispatcher):
    dispatcher.utter_message(response="utter_first_quest_correct")


def finish_quiz(dispatcher, dp_n):
    if (user_score["points"] == 0):
        dispatcher.utter_message(
            text="Damit hast du das Quiz abgeschlossen. 🎉")
    else:
        dispatcher.utter_message(
            text="Damit hast du das Quiz mit insgesamt %s von 15 Punkten abgeschlossen. 🎉" % user_score["points"])
        if user_score["not_first_attempt"] == 0:
            dispatcher.utter_message(
                text="Du hast alle Fragen im ersten Versuch richtig beantwortet. 🏆")
            dispatcher.utter_message(
                image=learn_quest["badge_naturtalent"])

            resetUserPoints()

############################################################################################################
##### DP1 #####
############################################################################################################


class ValidateDP1Form(FormValidationAction):

    def name(self) -> Text:
        # Unique identifier of the form"
        return "validate_dp1_form"

    def validate_dp1(name_of_slot):

        def setPoints(points):
            user_score["points"] += points
            user_score["last_question_correct"] = 1

        def finishedDP1(dispatcher, learn_quest):
            if (user_score["points"] == 0):
                dispatcher.utter_message(
                    text="Damit hast du das Quiz abgeschlossen. 🎉")
            else:
                dispatcher.utter_message(
                    text="Damit hast du das Quiz mit insgesamt %s von 15 Punkten abgeschlossen. 🎉" % user_score["points"])
                if user_score["not_first_attempt"] == 0:
                    dispatcher.utter_message(
                        text="Du hast alle Fragen im ersten Versuch richtig beantwortet. 🏆")
                    dispatcher.utter_message(
                        image=learn_quest["badge_naturtalent"])

            resetUserPoints()

        def say_utter_n_question(dispatcher):
            if user_score["points"] > 0 & user_score["tries"] == 0:
                # user hat die Fragen weiterhin im ersten Versuch richtig beantwortet
                if user_score["last_question_correct"] == 1:
                    dispatcher.utter_message(
                        response="utter_dp1_correct_n_first_approach")
                else:
                    # user hat die vorherige Frage nicht im ersten Versuch richtig beantwortet, diese aber schon
                    dispatcher.utter_message(
                        response="utter_dp1_another_correct_answer")
             # user hat diese Frage nicht im ersten Versuch richtig beantwortet, aber hat schon Punkte erzielt
            elif user_score["points"] > 0 & user_score["tries"] > 0:
                dispatcher.utter_message(
                    response="utter_dp1_correct_n_second_approach")
            # dies ist die aller erste Frage, die der User richtig beantwortet
            else:
                dispatcher.utter_message(
                    response="utter_dp1_first_correct_answer")

        def say_utter_last_question(dispatcher):
            if user_score["last_question_correct"] == 1:
                dispatcher.utter_message(
                    response="utter_dp1_correct_n_first_approach")

            elif user_score["points"] > 0:
                dispatcher.utter_message(
                    response="utter_dp1_another_correct_answer")
            else:
                dispatcher.utter_message(
                    response="utter_dp1_first_correct_answer")

        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            print("val", value)

            with open("DP1.json", "r") as jsonFile:
                learn_quest = json.load(jsonFile)

            solution = learn_quest[name_of_slot]["solution"]
            # scoring(solution, learn_quest, name_of_slot, value, dispatcher)

            # Users answer is correct
            if solution.lower() == value.lower():

                # evaluate_users_answer(learn_quest, name_of_slot, value, dispatcher)

                # 1. Frage, direkt richtig
                if learn_quest[name_of_slot]["question"] == 1 & user_score["tries"] == 0:
                    dispatcher.utter_message(
                        response="utter_dp1_correct_1_first_approach")

                # nte Frage
                if learn_quest[name_of_slot]["question"] < learn_quest["total_questions"]:
                    say_utter_n_question(dispatcher)

                # letzte Frage
                if learn_quest[name_of_slot]["question"] == learn_quest["total_questions"]:
                    say_utter_last_question(dispatcher)

                setPoints(learn_quest[name_of_slot]["points"])
                # check letzte Frage und gibt Gesamtpunkte aus
                print("user_score", user_score)
                if learn_quest[name_of_slot]["question"] == learn_quest["total_questions"]:
                    finishedDP1(dispatcher, learn_quest)
                else:
                    resetTries()
                return {name_of_slot: value}

            # Users answer is wrong
            elif getTries() < 1:  # User hat einen weiteren Versuch
                user_score["not_first_attempt"] = 1
                print("tries", getTries())
                dispatcher.utter_message(response="utter_dp1_wrong")
                increaseTries()
                print("user_score", user_score)
                return {name_of_slot: None}

            # User has no more tries
            else:
                user_score["last_question_correct"] = 0
                dispatcher.utter_message(
                    text='Schade, leider ist die Lösung: %s' % solution)
                if learn_quest[name_of_slot]["question"] == learn_quest["total_questions"]:
                    finishedDP1(dispatcher, learn_quest)
                else:
                    resetTries()
                print("user_score", user_score)
                return {name_of_slot: False}

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
            # If the user dont want more information, we dont need to ask
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
            dispatcher.utter_message(text="Gute Entscheidung!  😊")
            return {"s_dp2_q4": value}
        elif value == "no":

            dispatcher.utter_message(
                text="Ok, wir können dies sonst zu einem anderen Zeitpunkt üben. 😊")
            dispatcher.utter_message(response="utter_get_dp")
            return {"s_dp2_q4": value}
        else:
            return {"s_dp2_q4": None}

    def validate_s_dp2_q5(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:

        entities = slot_value
        name_of_slot = "s_dp2_q5"
        number_of_entities = len(entities)
        print("Debug", entities, number_of_entities)

        # check entities
        entities_list = json.load(open('DP2.json'))

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

    def validate_dp2(name_of_slot):
        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            print("val", value)
            with open("DP2.json", "r") as jsonFile:
                dp2 = json.load(jsonFile)

            solution = dp2[name_of_slot]["solution"]

            # Users answer is correct
            if solution.lower() == value.lower():
                if dp2[name_of_slot]["question"] == 1:
                    dispatcher.utter_message(
                        response="utter_correct_answer_q1")
                elif user_score["last_question_correct"] == 1:
                    dispatcher.utter_message(
                        response="utter_another_correct_answer")
                else:
                    dispatcher.utter_message(
                        response="utter_correct_answer_qn")
                resetTries()
                user_score["last_question_correct"] = 1
                if dp2[name_of_slot]["question"] == dp2["total_questions"]:
                    resetUserPoints()
                return {name_of_slot: value}

            elif getTries() < 1:  # User hat einen weiteren Versuch
                increaseTries()
                dispatcher.utter_message(response="utter_wrong_answer")
            else:
                resetTries()
                dispatcher.utter_message(
                    text='Schade, leider ist die Lösung: %s' % solution)
                if dp2[name_of_slot]["question"] == dp2["total_questions"]:
                    resetUserPoints()
                return {name_of_slot: False}
            return {name_of_slot: None}

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
        value = slot_value
        dp3 = json.load(open('DP3.json'))
        dispatcher.utter_message(
            text="Das klingt interessant! Ich würde daraus folgendes Lernziel forumlieren: %s" % dp3["s_dp3_q1"]["goal"][value])
        return {"s_dp3_q1": value}

    def validate_s_dp3_q2(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: "DomainDict") -> Dict[Text, Any]:
        if slot_value == "affirm":
            dispatcher.utter_message(response="utter_affirm_learn_goal")
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

    validate_s_dp3_q3 = validate_dp3(name_of_slot="s_dp3_q3")
    validate_s_dp3_q4 = validate_dp3(name_of_slot="s_dp3_q4")


############################################################################################################
##### Check Grammar #####
# these methods are use for DP2 and DP4
############################################################################################################

def json_formatter(json_response):
    print(json.dumps(json_response, indent=4))


def grammar_check(user_input):
    url = "https://dnaber-languagetool.p.rapidapi.com/v2/check"

    payload = f"language=en-US&text={user_input}"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key":
        "dc09bffcb7msh11b3124e909d941p1fa26ajsn8621ad32fdbb",
        "X-RapidAPI-Host": "dnaber-languagetool.p.rapidapi.com",
        "motherTongue": "de"
    }

    response = requests.request("POST",
                                url,
                                data=payload,
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

        def translate_to_german(grammar_error):

            url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"
            payload = {"q": grammar_error, "source": "en", "target": "de"}
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key":
                "dc09bffcb7msh11b3124e909d941p1fa26ajsn8621ad32fdbb",
                "X-RapidAPI-Host": "deep-translate1.p.rapidapi.com"
            }

            response = requests.request("POST",
                                        url,
                                        json=payload,
                                        headers=headers)
            json_formatter(response.json())
            return response.json()

        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:

            entities = value
            number_of_entities = len(entities)
            print("Debug", entities, number_of_entities)

            # check entities
            entities_list = json.load(open('DP4.json'))

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


def check_answer(name_of_slot, value, dispatcher):
    dp3 = json.load(open('DP3.json'))
    if (dp3[name_of_slot]["solution"] == value):
        dispatcher.utter_message(text="Richtig!")
        return {name_of_slot: value}
    else:
        dispatcher.utter_message(
            text="Leider falsch. Versuche es noch einmal.")
        return {name_of_slot: None}


def define_learn_goal(slot_value, value, dispatcher):
    dp3 = json.load(open('DP3.json'))
    dispatcher.utter_message(
        text="Ich würde daraus folgendes Lernziel forumlieren: %s" % dp3[slot_value][value])


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
            # If the user dont want more information, we dont need to ask
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
            dispatcher.utter_message(
                text="Okay, vielleicht liegt es an unserem Lernprozess.")
        elif value == "affirm":
            dispatcher.utter_message(text="Das freut mich zu hören!")
        return {"s_dp3_v_q4": value}

    def validate_s_dp3_v_q5(self,
                            value: Text,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: Dict[Text, Any],
                            ) -> Dict[Text, Any]:
        if value == "shorter_learntime":
            dispatcher.utter_message(
                text="Oh, ich verstehe. Was hälst du davon, wenn wir das Vokabelquiz von 50 auf 35 Fragen verkürzen? So könntest du dein Ziel von 2000 neuen Wörter bis zum Ende des Jahres trotzdem noch erreichen.")
        elif value == "longer_learntime":
            dispatcher.utter_message(
                text="Cool, dann erhöhren wir das Vokabelquiz von 50 auf 60 Fragen. So kannst du dein Ziel von 2000 neuen Wörtern bis zum Ende des Jahres sogar übertreffen!")
        return {"s_dp3_v_q5": value}

    def validate_s_dp3_v_q6(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_v_q6": value}

    def validate_s_dp3_v_q7(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_v_q7": value}

    def validate_dp3voc(name_of_slot):
        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            return check_answer(name_of_slot, value, dispatcher)
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
            dispatcher.utter_message(
                text="Okay, vielleicht liegt es an unserem Lernprozess.")
        elif value == "affirm":
            dispatcher.utter_message(text="Das freut mich zu hören!")
        return {"s_dp3_g_q4": value}

    def validate_s_dp3_g_q5(self,
                            value: Text,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: Dict[Text, Any],
                            ) -> Dict[Text, Any]:
        if value == "shorter_learntime":
            dispatcher.utter_message(
                text="Oh, ich verstehe. Was hälst du davon, wenn wir das Grammatikquiz von 50 auf 35 Fragen verkürzen? So könntest du dein Ziel von zwei Zeitformen bis zum Ende des Jahres trotzdem noch erreichen.")
        elif value == "longer_learntime":
            dispatcher.utter_message(
                text="Cool, dann erhöhren wir das Grammatikquiz von 50 auf 60 Fragen. So kannst du dein Ziel von zwei Zeitformen bis zum Ende des Jahres sogar übertreffen!")
        return {"s_dp3_g_q5": value}

    def validate_s_dp3_g_q6(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_g_q6": value}

    def validate_s_dp3_g_q7(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        return {"s_dp3_g_q7": value}

    def validate_dp3gram(name_of_slot):

        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            return check_answer(name_of_slot, value, dispatcher)

        return validate_slot

    validate_s_dp3_g_q3 = validate_dp3gram(name_of_slot="s_dp3_g_q3")
