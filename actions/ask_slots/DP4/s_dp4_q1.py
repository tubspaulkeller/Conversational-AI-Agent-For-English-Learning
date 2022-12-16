from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp4_q1A"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ sending a image for intro in learning story and ask Q1 """

        if tracker.get_slot("s_dp4_intro") is None:
            dispatcher.utter_message(response="utter_s_dp4_intro")
            dispatcher.utter_message(
                image="https://res.cloudinary.com/dmnkxrxes/image/upload/v1670965838/Ben_Bot/Story_Card_2_ndwafo.jpg"
            )
            dispatcher.utter_message(response="utter_s_dp4_q1A")
            return [SlotSet("s_dp4_intro", "INTRO_GIVEN")]
        else:
            dispatcher.utter_message(response="utter_s_dp4_q1A")
            return []
