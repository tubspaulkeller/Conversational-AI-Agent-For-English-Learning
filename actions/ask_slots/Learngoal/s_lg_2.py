from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.common.common import markdown_formatting
from datetime import date
today = date.today().strftime("%Y-%m-%d")
msg = {
    "blocks": [
        {
            "type": "section",
            "block_id": "section_date",
            "text": {
                    "type": "mrkdwn",
                    "text": "Bis wann möchtest du diesen Kurs beenden? Gebe hier bitte das *Datum* ein."
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
        user_selection = tracker.slots.get("s_lg_intro")
        topic = tracker.slots.get("s_lg_0")
        date_button = [{'title': 'Datum bestätigen',
                        'payload': "/i_lg_2{\"e_lg_2\":\"date\"}"}]
        confirm_button = [{'title': 'Bestätigen',
                           'payload': "/i_lg_2{\"e_lg_2\":\"confirm\"}"},
                          {'title': 'Doch nicht ändern',
                           'payload': "/i_lg_2{\"e_lg_2\":\"deny\"}"}]

        if is_accepting_learngoal == "deny":
            dispatcher.utter_message(
                response="utter_s_lg_0/%s/repeat" % user_selection)
            return [SlotSet("s_lg_0", None), SlotSet("s_lg_1", None)]

        elif is_accepting_learngoal == "need_longer" or is_accepting_learngoal == "faster":

            if topic == "Englisch-Konversation":
                text = " "
                if is_accepting_learngoal == "faster":
                    text = "Ich kann schon nach der *hälfte der Lektion* eine Konversation mit einem Muttersprachler führen."
                elif is_accepting_learngoal == "need_longer":
                    text = "Ich kann nach *zwei Lektionen* eine Konversation mit einem Muttersprachler führen."
                dispatcher.utter_message(
                    json_message=markdown_formatting(text))
                dispatcher.utter_message(text=" ", buttons=confirm_button)
            else:
                dispatcher.utter_message(json_message=msg)
                dispatcher.utter_message(text=" ", buttons=date_button)

        else:
            return
