from actions.helper.check_entities import exist_present_perfect, exist_all_parts_of_question
from actions.common.common import get_dp_inmemory_db
from actions.gamification.handle_user_scoring import get_tries, resetTries, increase_tries, set_points, user_score
from cgitb import text
from lib2to3.pgen2 import grammar
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
# import functions from other files

############################################################################################################
##### Check Grammar #####
############################################################################################################

"""these methods are use for DP2 and DP4 """


def validate_grammar_for_user_answer(value, json_file, name_of_slot, dispatcher, tracker):
    """ validate the grammar of the user input """
    if not check_if_question_is_already_answered(name_of_slot, dispatcher):
        if not check_if_user_answered_current_question(tracker, name_of_slot, dispatcher):
            return {name_of_slot: None}
        entities = value
        number_of_entities = len(entities)
        print(entities)
        # check entities
        entities_list = get_dp_inmemory_db(json_file)

        # Prüfung auf Present Perfect bei DP4 nur Q5
        if (name_of_slot[4] != '4' or name_of_slot == 's_dp4_q3A' or name_of_slot == 's_dp4_q3B'):
            if not exist_present_perfect(name_of_slot, entities, entities_list, dispatcher):
                increase_tries()
                return {name_of_slot: None}

        if not exist_all_parts_of_question(number_of_entities, name_of_slot, entities, entities_list, dispatcher):
            increase_tries()
            return {name_of_slot: None}

        # get Userinput
        usertext = tracker.latest_message['text']
        # first letter of the word is capitalized
        usertext = usertext[0].upper() + usertext[1:]

        if not valid_grammar(usertext, dispatcher):
            increase_tries()
            return {name_of_slot: None}
        else:
            points = 0
            if get_tries() == 0:
                set_points(5, name_of_slot[4: 7])
                points = 5
            elif get_tries() == 1:
                set_points(4, name_of_slot[4: 7])
                points = 4
            elif get_tries() == 2:
                set_points(3, name_of_slot[4: 7])
                points = 3
            elif get_tries() > 2:
                set_points(2, name_of_slot[4: 7])
                points = 2
            resetTries()
            dispatcher.utter_message(
                response="utter_correct_answer_qn", points=points)
            user_score[name_of_slot] = 1
            return {name_of_slot: True}
    else:
        return {name_of_slot: True}


def check_if_user_answered_current_question(tracker, name_of_slot, dispatcher):
    print('name_of_slot: ', name_of_slot)
    for event in reversed(tracker.events):
        if event['event'] == 'slot':
            print('event: ', event)
            if event['name'] == 'requested_slot':
                print('event: ', event['value'])
                if event['value'] == name_of_slot:
                    return True
                else:
                    dispatcher.utter_message(
                        text="Du antwortest nicht auf die momentan gestellte Frage. Bitte beantworte die aktuelle Frage.")
                    return False


def check_if_question_is_already_answered(name_of_slot, dispatcher):
    print('name_of_slot: ', name_of_slot)
    if user_score[name_of_slot] == 1:
        dispatcher.utter_message(
            text="Die Frage %s hast du schon vorher beantwortet. Bitte antworte auf die aktuelle Frage." % name_of_slot[len(name_of_slot)-2:])
        return True
    else:
        return False


def json_formatter(json_response):
    """ format json response """
    print(json.dumps(json_response, indent=4))


def grammar_check(user_input):
    """ calls a grammar check api """
    url = "https://dnaber-languagetool.p.rapidapi.com/v2/check"

    payload = f"language=en-US&text={user_input}"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key":
        os.getenv('GRAMMAR_TOOL_KEY'),
        "X-RapidAPI-Host": "dnaber-languagetool.p.rapidapi.com",
        "motherTongue": "de"
    }
    try:
        response = requests.request("POST",
                                    url,
                                    data=payload,
                                    headers=headers)
    except:
        print('error in calling the grammar check api')

    # json_formatter(response.json())
    return response.json()


def translate_to_german(grammar_error):
    # calls the translate api and translates the grammar error to german
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
    """ checks if the grammar is correct. If not it returns the error and the suggestion  """
    suggestions = []
    print("Grammar Response: ", grammar_response)
    if (len(grammar_response['matches']) > 0):
        if grammar_response['matches'][0]['message']:
            matches = grammar_response['matches'][0]['message']

            if len(grammar_response['matches'][0]['replacements']) > 0:
                for i, val in enumerate(grammar_response['matches'][0]
                                        ['replacements']):
                 #   print(i, ". suggestion: ", val['value'])
                    suggestions.append(val['value'])

        print(matches)
        return matches, suggestions

    print("No grammar errors found\n")
    return None, None


def valid_grammar(usertext, dispatcher):
    """ a meta method which calls the grammar check api and checks if the grammar is correct """
    grammar_response = grammar_check(usertext)
    grammar_error, grammar_suggestion = grammar_validation(grammar_response)
    if check_grammar_error(grammar_error, dispatcher, grammar_suggestion):
        return False
    else:
        return True


def check_grammar_error(grammar_error, dispatcher, grammar_suggestion):
    """ returns the suggestions for the correct answer """
    if grammar_error:
        dispatcher.utter_message(response="utter_grammar_error")
        dispatcher.utter_message(text=grammar_error)
        if grammar_suggestion:
            for i, val in enumerate(grammar_suggestion):
                dispatcher.utter_message(
                    text=f"- suggestion: {val}")
                if i == 1:
                    break
        return True
    else:
        return False
