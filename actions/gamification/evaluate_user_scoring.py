from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted
import json
from .handle_user_scoring import user_score, set_points, increase_tries, resetTries, reset_user_score, get_tries
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


