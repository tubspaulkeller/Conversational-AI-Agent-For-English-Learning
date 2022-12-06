from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.gamification.evaluate_user_scoring import finish_quiz
from actions.common.common import get_dp_inmemory_db


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp3_g_q4"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ If the user want to change his goal, the user can choose a different goal. """

        dp_3 = get_dp_inmemory_db("DP3.json")
        finish_quiz(dispatcher, "s_dp3_g", dp_3)

        dispatcher.utter_message(
            text="Mit deiner heutigen Leistung bist du deinem Ziel ein großes Stück näher gekommen!")
        dispatcher.utter_message(response="utter_s_dp3_g_q4")
        return []
