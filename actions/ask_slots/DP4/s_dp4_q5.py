from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp4_q5"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ sending a image for the next question """

        dispatcher.utter_message(
            image="https://res.cloudinary.com/dmnkxrxes/image/upload/c_scale,w_251/v1667902166/Ben_Bot/story_three_k50xli.png"
        )
        dispatcher.utter_message(response="utter_s_dp4_q5")

        return []
