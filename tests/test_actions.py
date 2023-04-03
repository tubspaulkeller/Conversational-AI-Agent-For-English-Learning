import json
import pytest

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher, Tracker
from rasa_sdk.events import SlotSet, SessionStarted
from rasa_sdk.types import DomainDict

from actions.helper.rephrase import ActionRephrase
from actions.helper.check_grammar_of_users_input import grammar_check, grammar_validation, validate_grammar_for_user_answer
from tests.conftest import EMPTY_TRACKER, DP2, REPHRASE
from actions.DPs.DP2 import ValidateDP2Form
import os

from pathlib import Path
#here = Path(__file__).parent.resolve()

# execute
# pytest -v tests/test_actions.py


def test_run_check_grammar_api():
    input = "How much does it costs?"
    grammar_response = grammar_check(input)
    grammar_error, grammar_suggestion = grammar_validation(grammar_response)
    # to get print output: pytest -s
    print(grammar_error)
    assert grammar_error != None


# async test
@pytest.mark.asyncio
async def test_run_rephrase(dispatcher: CollectingDispatcher, domain: DomainDict):
    tracker = REPHRASE
    action = ActionRephrase()
    events = await action.run(dispatcher, tracker, domain)
    expected_template = "utter_rephrase/en"
    assert dispatcher.messages[0]["template"] == expected_template
