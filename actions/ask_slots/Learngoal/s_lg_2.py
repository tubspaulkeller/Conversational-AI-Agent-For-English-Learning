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

        elif is_accepting_learngoal == "more_words":
            text = "Wähle eine Anzahl der Wört aus, die du lernen möchtest."
            buttons_words = [
                {'title': '3000', 'payload': '/i_lg_2{\"e_lg_2\":\"3000\"}'},
                {'title': '4000', 'payload': '/i_lg_2{\"e_lg_2\":\"4000\"}'},
                {'title': '5000', 'payload': '/i_lg_2{\"e_lg_2\":\"5000\"}'},
                {'title': '6000', 'payload': '/i_lg_2{\"e_lg_2\":\"6000\"}'},
                {'title': '7000', 'payload': '/i_lg_2{\"e_lg_2\":\"7000\"}'}
            ]

            dispatcher.utter_message(text=text, buttons=buttons_words)

        elif is_accepting_learngoal == "less_words":
            text = "Wähle eine Anzahl der Wört aus, die du lernen möchtest."
            buttons_words = [
                {'title': '500', 'payload': '/i_lg_2{\"e_lg_2\":\"500\"}'},
                {'title': '1000', 'payload': '/i_lg_2{\"e_lg_2\":\"1000\"}'},
                {'title': '1500', 'payload': '/i_lg_2{\"e_lg_2\":\"1500\"}'}
            ]
            dispatcher.utter_message(text=text, buttons=buttons_words)
        elif is_accepting_learngoal == "more_zeitformen":
            text = "Wähle eine Anzahl an Zeitformen aus, die du lernen möchtest."
            buttons_words = [
                {'title': '3-4', 'payload': '/i_lg_2{\"e_lg_2\":\"3-4\"}'},
                {'title': '5-6', 'payload': '/i_lg_2{\"e_lg_2\":\"5-6\"}'},
                {'title': '7-8', 'payload': '/i_lg_2{\"e_lg_2\":\"7-8\"}'},
                {'title': '9-10', 'payload': '/i_lg_2{\"e_lg_2\":\"9-10\"}'}
            ]
            dispatcher.utter_message(text=text, buttons=buttons_words)
        elif is_accepting_learngoal == "less_zeitformen":
            text = "Wir setzen unser Monatsziel auf mindestens eine und maximal auf zwei Zeitformen."
            buttons_words = [
                {'title': 'Ok', 'payload': '/i_lg_2{\"e_lg_2\":\"1-2\"}'},
            ]
            dispatcher.utter_message(text=text, buttons=buttons_words)
        else:
            return
