import json
import pytest

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher, Tracker
from rasa_sdk.events import SlotSet, ActionExecuted, SessionStarted
from rasa_sdk.types import DomainDict

from actions.DPs.GET_DP import ValidateGetDPForm
from actions.helper.check_grammar_of_users_input import grammar_check, grammar_validation, validate_grammar_for_user_answer
from tests.conftest import EMPTY_TRACKER, GET_DP, DP1
from actions.DPs.DP1 import ValidateDP1Form
import os

from pathlib import Path
#here = Path(__file__).parent.resolve()

# @pytest.mark.asyncio
# def test_run_check_grammar_api():
#     input = "How much does it costs?"
#     grammar_response = grammar_check(input)
#     grammar_error, grammar_suggestion = gramvalidate_grammar_for_user_answer()
#     #to get print output: pytest -s 
#     print(grammar_error)
#     assert grammar_error !=  None




@pytest.mark.asyncio
def test_run_validate_grammar_for_user_answer():
    input = "[We](e_dp4_q1) want to the [Coliseum](e_dp4_q1)"

    validate_grammar_for_user_answer(input,  "DP4.json", name_of_slot = "s_dp4_q1", dispatcher= CollectingDispatcher, tracker=Tracker)
    print(dispatcher.messages)
   
      #events = action.validate_slot("s_dp1_q1",dispatcher, tracker, domain)(
    #expected_events = [
     #   SlotSet("s_dp1_q1", "Fought"),
    #]
       #assert events == expected_events
    #assert dispatcher.messages[0]["template"] == "utter_first_quest_correct"
    #print(dispatcher.messages)
