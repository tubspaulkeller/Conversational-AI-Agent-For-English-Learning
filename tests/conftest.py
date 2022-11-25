
import os
from pathlib import Path
import pytest
import json


from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker

here = Path(__file__).parent.resolve()

EMPTY_TRACKER = Tracker.from_dict(
    json.load(open(here / "./data/empty_tracker.json")))

DP2 = Tracker.from_dict(
    json.load(open(here / "./data/dp2.json"))
)

REPHRASE = Tracker.from_dict(
    json.load(open(here / "./data/rephrase.json"))
)


@pytest.fixture
def dispatcher():
    return CollectingDispatcher()


@pytest.fixture
def domain():
    return dict()


@pytest.fixture
def tracker():
    return Tracker()
