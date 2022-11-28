from actions.common.common import get_dp_inmemory_db
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

# import functions from other files

############################################################################################################
##### Check Grammar #####
############################################################################################################

"""these methods are use for DP2 and DP4 """


def validate_grammar_for_user_answer(value, json_file, name_of_slot, dispatcher, tracker):
    """ validate the grammar of the user input """
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

    response = requests.request("POST",
                                url,
                                data=payload,
                                headers=headers)
    json_formatter(response.json())
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
    """ check if the user input contains all entities which are asked by the question of the quiz. The bot will ask the user to repeat the question if the user input is missing an entity """
    for entity in entities:
        # allow typos for entities till a certain threshold (80%)
        fuzzy_entity = process.extractOne(
            entity, entities_list[name_of_slot]["entities"])
        if not fuzzy_entity[1] > 80:
            return True
    return False


def check_entities(number_of_entities, entities_list, name_of_slot, entities, dispatcher):
    """ checks user input if the number of entities is correct and if the entities are correct """
    if number_of_entities != entities_list[name_of_slot]["quantity"] | check_missing_entities(name_of_slot, entities, entities_list):
        dispatcher.utter_message(
            text="You didn't answer all parts of the question, unfortunately. Try to make your answer more detailed and pay attention to use the right tense. Try again. :)")
        return True
    else:
        return False


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
                    text=f"{i}. suggestion: {val}")
                if i == 3:
                    break
        return True
    else:
        return False
