from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.common.common import markdown_formatting


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp3_g_q1"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        # user can change his goal
        text = "Bevor wir mit der Grammatik-Lektion anfangen, lass uns noch ein *Monatsziel als Teilziel* für diese Grundlagen-Lektion festlegen, damit wir zusammen auf etwas hinarbeiten können 😊"
        dispatcher.utter_message(json_message=markdown_formatting(text))
        dispatcher.utter_message(response="utter_s_dp3_g_q1/buttons")
        return []
