from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
import time
from datetime import date
today = date.today().strftime("%Y-%m-%d")
msg = {
    "blocks": [
        {
            "type": "section",
            "block_id": "section_date",
            "text": {
                    "type": "mrkdwn",
                    "text": "Gebe hier bitte das *Datum* ein."
            },
            "accessory": {
                "type": "datepicker",
                "initial_date": today,
                "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date",
                },
                "action_id": "datepicker-action",

            }
        }
    ]
}


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_lg_2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:

        is_accepting_learngoal = tracker.slots.get("s_lg_1")
        date_button = [{'title': 'Datum bestätigen',
                        'payload': "/i_lg_2{\"e_lg_2\":\"date\"}"}]

        if is_accepting_learngoal == "deny":
            dispatcher.utter_message(response="utter_s_lg_0/repeat")
            return [SlotSet("s_lg_0", None), SlotSet("s_lg_1", None)]
        elif is_accepting_learngoal == "need_longer":
            dispatcher.utter_message(json_message=msg)
            dispatcher.utter_message(text=" ", buttons=date_button)

        elif is_accepting_learngoal == "faster":
            dispatcher.utter_message(json_message=msg)
            dispatcher.utter_message(text=" ", buttons=date_button)

        else:
            return
        return []

        return []
