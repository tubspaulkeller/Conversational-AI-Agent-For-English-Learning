from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.common.common import get_dp_inmemory_db


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp3_q4"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ calls the next form depending on the user input """
        oberziel = " "
        if tracker.slots.get("s_dp3_date") != None:
            oberziel = tracker.slots.get("s_dp3_date")
        else:
            dp3 = get_dp_inmemory_db('DP3.json')
            user_selection = tracker.slots.get("s_dp3_q1")
            deadline = "bis zum Ende des Jahres"
            oberziel = dp3["s_dp3_q1"]["goal"][user_selection] % deadline

        if tracker.slots.get("s_dp3_q3") == "vocabels":
            return [FollowupAction("dp3_form_voc"), SlotSet("s_dp3_q4", "vocabel_form"), SlotSet("s_oberziel", oberziel)]
        else:
            return [FollowupAction("dp3_form_gram"), SlotSet("s_dp3_q4", "grammar_form"), SlotSet("s_oberziel", oberziel)]
