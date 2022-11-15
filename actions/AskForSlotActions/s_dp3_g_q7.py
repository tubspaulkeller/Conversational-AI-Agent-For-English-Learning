from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
import time


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp3_g_q7"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:

        if tracker.slots.get("s_dp3_g_q6") == "deny":
            dispatcher.utter_message(response="utter_ask_s_dp3_g_q5")
            return [SlotSet("s_dp3_g_q5", None), SlotSet("s_dp3_g_q6", None)]

        elif tracker.slots.get("s_dp3_g_q5") == "deny" or tracker.slots.get("s_dp3_g_q6") == "affirm":
            # nur die Grammatik Form wurde abgeschlossen
            if tracker.slots.get("s_dp3_q4") == "grammar_form":
                dispatcher.utter_message(
                    text="Super, dann können wir uns auf die Vokabel Lektion konzentrieren.")
                return [FollowupAction("dp3_form_voc"), SlotSet("s_dp3_g_q7", "vocabel_form")]

            # beide Froms wurden abgeschlossen
            elif tracker.slots.get("s_dp3_q4") == "vocabel_form":
                dispatcher.utter_message(text="Ok super!")
                return [SlotSet("s_dp3_g_q7", "grammar_form"), FollowupAction("utter_get_dp/3")]
