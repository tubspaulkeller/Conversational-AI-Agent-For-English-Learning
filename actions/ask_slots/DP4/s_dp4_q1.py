from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp4_q1"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ sending a image for intro in learning story and ask Q1 """

        if tracker.get_slot("s_dp4_intro") is None:
            dispatcher.utter_message(response="utter_s_dp4_intro")
            dispatcher.utter_message(
                image="https://res.cloudinary.com/dmnkxrxes/image/upload/c_scale,w_250/v1667902166/Ben_Bot/story_one_fmhkes.png"
            )
            dispatcher.utter_message(response="utter_s_dp4_q1")
            return [SlotSet("s_dp4_intro", "INTRO_GIVEN")]
        else:
            dispatcher.utter_message(response="utter_s_dp4_q1")
            return []
