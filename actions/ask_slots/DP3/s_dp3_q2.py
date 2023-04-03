from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from datetime import date
from actions.helper.learn_goal import generate_learn_goal
today = date.today().strftime("%Y-%m-%d")
buttons = {
    "s_date": {'title': 'Datum bestätigen', 'payload': "/i_date{\"e_date\":\"date\"}"},
}


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp3_q2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ user can change his goal """
        slot_value = tracker.get_slot("s_dp3_q1")
        generate_learn_goal('s_dp3_q1', 's_dp3_q1', dispatcher, slot_value,
                            'Das klingt interessant! Ich würde daraus folgendes Lernziel forumlieren:', 'Ende des Jahres', " ")

        dispatcher.utter_message(response="utter_s_dp3_q2")
        return []
