from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
import time


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_lg_finish"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:

        goal = " "
        slot = " "
        user_selection = tracker.slots.get("s_lg_intro")

        if tracker.get_slot("s_lg_2") != None:
            goal = tracker.get_slot("s_lg_2")
        else:
            goal = tracker.get_slot("s_lg_1")

        if user_selection == "oberziel":
            slot = "s_oberziel"
        elif user_selection == "vokabelziel":
            slot = "s_vokabelziel"
        elif user_selection == "grammatikziel":
            slot = "s_grammatikziel"

        dispatcher.utter_message(response="utter_s_lg_intro")
        return [SlotSet("s_lg_intro", None), SlotSet("s_lg_0", None), SlotSet("s_lg_1", None), SlotSet("s_lg_2", None), SlotSet("s_lg_finish", None), SlotSet(slot, goal)]
