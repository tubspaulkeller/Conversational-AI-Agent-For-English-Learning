from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.gamification.handle_user_scoring import get_tries


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp4_q3"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ sending a image for the next question """
        if get_tries() == 0:
            dispatcher.utter_message(
                image="https://res.cloudinary.com/dmnkxrxes/image/upload/v1670966055/Ben_Bot/Story_Card_3_po0u7x.jpg"
            )
        dispatcher.utter_message(response="utter_s_dp4_q3")

        return []
