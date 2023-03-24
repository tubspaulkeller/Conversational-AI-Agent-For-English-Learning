from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
import time
from actions.common.common import markdown_formatting


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_lg_0"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        user_selection = tracker.slots.get("s_lg_intro")
        if user_selection == "EXIT":
            return [UserUtteranceReverted(), SlotSet("s_get_dp_form", None), SlotSet("s_set_next_form", None), FollowupAction("get_dp_form")]

        if user_selection == "oberziel":
            dispatcher.utter_message(response="utter_s_lg_0/oberziel")

        if user_selection == "vokabelziel":
            dispatcher.utter_message(response="utter_s_lg_0/vokabelziel")

        if user_selection == "grammatikziel":
            dispatcher.utter_message(response="utter_s_lg_0/grammatikziel")

        if user_selection == "INFO":
            oberziel = tracker.get_slot("s_oberziel")
            vokabelziel = tracker.get_slot("s_vokabelziel")
            grammatikziel = tracker.get_slot("s_grammatikziel")

            text = "Deine aktuellen Lernziele sind:\n\nOberziel: *%s*\n\nVokabelziel: *%s*\n\nGrammatikziel: *%s*" % (
                oberziel, vokabelziel, grammatikziel)
            dispatcher.utter_message(json_message=markdown_formatting(text))
            dispatcher.utter_message(response="utter_s_lg_intro")
            return [SlotSet("s_lg_intro", None)]
        return []
