from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
import time
from actions.common.common import get_dp_inmemory_db
from actions.helper.learn_goal import get_key_for_json


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_lg_finish"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:

        goal = " "
        slot = " "
        user_selection = tracker.slots.get("s_lg_intro")
        key, pretext, deadline = get_key_for_json(user_selection, tracker)
        # in s_lg_2 ist custom goal
        if tracker.get_slot("s_lg_2") != None:
            goal = tracker.get_slot("s_lg_2")
        else:
            dp3 = get_dp_inmemory_db('DP3.json')
            topic = tracker.slots.get("s_lg_0")
            deadline = "bis zum Ende des Jahres"
            goal = dp3[key]["goal"][topic] % deadline

        if user_selection == "oberziel":
            slot = "s_oberziel"
        elif user_selection == "vokabelziel":
            slot = "s_vokabelziel"
        elif user_selection == "grammatikziel":
            slot = "s_grammatikziel"

        dispatcher.utter_message(response="utter_s_lg_intro")
        return [SlotSet("s_lg_intro", None), SlotSet("s_lg_0", None), SlotSet("s_lg_1", None), SlotSet("s_lg_2", None), SlotSet("s_lg_finish", None), SlotSet(slot, goal)]
