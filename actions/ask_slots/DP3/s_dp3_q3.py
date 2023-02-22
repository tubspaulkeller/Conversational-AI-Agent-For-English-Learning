from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from datetime import date
today = date.today().strftime("%Y-%m-%d")
buttons = {
    "s_date": {'title': 'Datum bestätigen', 'payload': "/i_date{\"e_date\":\"date\"}"},
}


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp3_q3"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ user can change his goal """
        dispatcher.utter_message(response="utter_s_dp3_q3")
        return []
