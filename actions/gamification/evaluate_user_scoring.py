from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted
import json
import time
from .handle_user_scoring import user_score, set_points, increase_tries, resetTries, get_tries, increase_badges, user_score_simple_past, user_score_present_progressive
from actions.common.common import get_dp_inmemory_db
""" this file contains methods for evaluating the scoring of the user during the quiz """


def evaluate_users_answer(solution, dp_n, name_of_slot, value, dispatcher, slots, dp):
    """ users input is evaluated and the correct response is given to the user """

    if solution.lower() == value.lower():
        evaluate_scoring(dp_n, name_of_slot, dispatcher, slots)

        # different points when the users answers the first time corectly
        if user_score["tries"] == 0:
            set_points(dp_n[name_of_slot]["points"], name_of_slot[4:7])
        else:
            set_points(dp_n[name_of_slot]["points"] - 3, name_of_slot[4:7])
        if dp == "dp1":
            if name_of_slot in user_score_present_progressive:
                user_score_present_progressive[name_of_slot] += 1
            if name_of_slot in user_score_simple_past:
                user_score_simple_past[name_of_slot] += 1

        # check letzte Frage und gibt Gesamtpunkte aus
       # if dp_n[name_of_slot]["question"] == dp_n["total_questions"]:
        #    finish_quiz(dispatcher, name_of_slot, dp_n)
        # else:

        # TODO BADGES SENDEN UND FORTSCHRITTBALKEN

        if dp == "dp1":
            badges = get_dp_inmemory_db("badges.json")
            if user_score["badge_60_prozent"] == 0:
                if user_score["DP1_q_points"] >= 36:
                    increase_badges("badge_60_prozent")
                    dispatcher.utter_message(image=badges['quiz_master'])
            if user_score["badge_grammatik_profi"] == 0:
                if _has_one_value(user_score_present_progressive) == 1 and _has_one_value(user_score_simple_past) == 1:
                    increase_badges("badge_grammatik_profi")
                    dispatcher.utter_message(image=badges['grammar_king'])
        resetTries()
        return {name_of_slot: value}
    # Users answer is wrong
    elif get_tries() < 1:  # User hat einen weiteren Versuch
        return evaluate_tries_of_user(name_of_slot, dispatcher)

    # say solution
    else:
        return give_solution(dp_n, name_of_slot, dispatcher, solution)


def _has_one_value(d):
    return 1 in d.values()


def evaluate_scoring(dp_n, name_of_slot, dispatcher, slots):
    """ evaluate the scoring of the user, which is based on the number of tries"""

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

    elif user_score['DP'+name_of_slot[4:7]+'_points'] > 0 and user_score["tries"] > 0:
        # the question is the last
        if dp_n[name_of_slot]["question"] == dp_n["total_questions"]:
            utter_last_previous_correct_not_first_attempt(dispatcher)
        # the question is the nth
        else:
            utter_nth_previous_correct_not_first_attempt(dispatcher)

    # user answers a question correctly for the very first time, but needs several tries
    elif user_score['DP'+name_of_slot[4:7]+'_points'] == 0 and user_score["tries"] > 0:
        # the question is the last
        if dp_n[name_of_slot]["question"] == dp_n["total_questions"]:
            utter_last_quest_users_first_correct_not_first_attempt(dispatcher)
        # the question is the nth
        else:
            utter_nth_quest_user_first_correct_not_first_attempt(dispatcher)


def evaluate_tries_of_user(name_of_slot, dispatcher):
    """ users tries are evaluated and the correct response is given to the user """
    user_score["not_first_attempt"] = 1
    increase_tries()
    utter_wrong_answer(dispatcher)

    return {name_of_slot: None}


def give_solution(dp_n, name_of_slot, dispatcher, solution):
    """ the user could not answer the question correctly at second attempt and the solution is given to the user """
    user_score["last_question_correct"] = 0
    utter_solution(dispatcher, solution)
   # if dp_n[name_of_slot]["question"] == dp_n["total_questions"]:
    # finish_quiz(dispatcher, name_of_slot, dp_n)
    # else:
    resetTries()

    return {name_of_slot: "wrong_answer"}


def finish_quiz(dispatcher, name_of_slot, dp_n):
    """ the user finished the quiz and the score is given to the user """
    if (user_score['DP'+name_of_slot[4:7]+'_points'] == 0):
        utter_finished_quiz_no_points(dispatcher)
    elif name_of_slot[4] == "1":
        # just for DP1
        user_score['stars'] = user_score['stars'] + 1
        utter_finished_quiz_with_points(dispatcher, name_of_slot[4:7], dp_n)

        if user_score["not_first_attempt"] == 0 and name_of_slot[4] == "1":
            utter_all_quest_correct_at_first_attempt(dp_n, dispatcher)
    else:

        dispatcher.utter_message(
            text="Damit hast du dieses Quiz mit insgesamt %s von %s Punkten abgeschlossen. 🎉" % (user_score['DP'+name_of_slot[4:7]+'_points'], dp_n["total_points"]))
    resetTries()


##### Utter messages funtions #####
""" the following functions are used to give the user the correct response based on the number of tries and the question number. 
 If the user has answered the question correctly at first attempt, the user gets a different response than if the user has answered the question correctly at second attempt."""


def utter_solution(dispatcher, solution):
    solution_msg = {
        "blocks": [
            {
                "type": "section",
                "text": {
                        "text": "Schade, leider ist die Lösung: *%s*" % solution,
                        "type": "mrkdwn"
                }
            }
        ]
    }
    dispatcher.utter_message(
        json_message=solution_msg)


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


def utter_finished_quiz_with_points(dispatcher, dp, dp_n):
    dispatcher.utter_message(
        text="Damit hast du dieses Quiz mit insgesamt %s von %s Punkten abgeschlossen. 🎉\nFür die erfolgreiche Beendigung des Quiz hast du dir 1 ⭐️ verdient!" % (user_score['DP'+dp+'_points'], dp_n["total_points"]))


def utter_all_quest_correct_at_first_attempt(dp_n, dispatcher):
    increase_badges("badge_naturtalent")
    dispatcher.utter_message(
        text="Da du das Quiz direkt beim ersten Versuch fehlerfrei beendet hast, erhälst du außerdem ein neues Abzeichen. 🏆")
    dispatcher.utter_message(image=dp_n["badge_naturtalent"])
