from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
import time


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp3_g_end"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ The next form get called depending on the user input. If the user choosed before vocabluary, the form grammar is called. If the user choosed before grammar, the form grammar is called. """
        if tracker.slots.get("s_dp3_g_q6") == "deny":
            dispatcher.utter_message(response="utter_ask_s_dp3_g_q5")
            return [SlotSet("s_dp3_g_q5", None), SlotSet("s_dp3_g_q6", None)]

        elif tracker.slots.get("s_dp3_g_q5") == "deny" or tracker.slots.get("s_dp3_g_q6") == "affirm":
            # grammar form are done by the user
            if tracker.slots.get("s_dp3_q4") == "grammar_form":
                dispatcher.utter_message(
                    text="Super, dann können wir uns auf die Vokabel Lektion konzentrieren.")
                return [FollowupAction("dp3_form_voc"), SlotSet("s_dp3_g_end", "vocabel_form")]

            # both forms are finisched
            elif tracker.slots.get("s_dp3_q4") == "vocabel_form":
                dispatcher.utter_message(text="Ok super!")
                # the user can choose a different DP
                return [SlotSet("s_dp3_g_end", "grammar_form"), SlotSet("s_get_dp_form", None), SlotSet("s_set_next_form", None), FollowupAction("get_dp_form")]
