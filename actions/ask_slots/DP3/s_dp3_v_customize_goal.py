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
        return "action_ask_s_dp3_v_customize_goal"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:

        is_accepting_learngoal = tracker.slots.get("s_dp3_v_q2")
        topic = tracker.slots.get("s_dp3_v_q1")

        date_button = [{'title': 'Datum bestätigen',
                        'payload': "/i_dp3_v_customize_goal{\"e_dp3_v_customize_goal\":\"date\"}"}]
        confirm_button = [{'title': 'Bestätigen',
                           'payload': "/i_dp3_v_customize_goal{\"e_dp3_v_customize_goal\":\"confirm\"}"},
                          {'title': 'Doch nicht ändern',
                           'payload': "/i_dp3_v_customize_goal{\"e_dp3_v_customize_goal\":\"deny\"}"}]

        if is_accepting_learngoal == "deny":
            dispatcher.utter_message(
                response="utter_s_dp3_v_q1/repeat")
            return [SlotSet("s_dp3_v_q1", None), SlotSet("s_dp3_v_q2", None)]

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
                {'title': '3000', 'payload': '/i_dp3_v_customize_goal{\"e_dp3_v_customize_goal\":\"3000\"}'},
                {'title': '4000', 'payload': '/i_dp3_v_customize_goal{\"e_dp3_v_customize_goal\":\"4000\"}'},
                {'title': '5000', 'payload': '/i_dp3_v_customize_goal{\"e_dp3_v_customize_goal\":\"5000\"}'},
                {'title': '6000', 'payload': '/i_dp3_v_customize_goal{\"e_dp3_v_customize_goal\":\"6000\"}'},
                {'title': '7000', 'payload': '/i_dp3_v_customize_goal{\"e_dp3_v_customize_goal\":\"7000\"}'}
            ]

            dispatcher.utter_message(text=text, buttons=buttons_words)

        elif is_accepting_learngoal == "less_words":
            text = "Wähle eine Anzahl der Wört aus, die du lernen möchtest."
            buttons_words = [
                {'title': '500', 'payload': '/i_dp3_v_customize_goal{\"e_dp3_v_customize_goal\":\"500\"}'},
                {'title': '1000', 'payload': '/i_dp3_v_customize_goal{\"e_dp3_v_customize_goal\":\"1000\"}'},
                {'title': '1500', 'payload': '/i_lg_2{\"e_dp3_v_customize_goal\":\"1500\"}'}
            ]
            dispatcher.utter_message(text=text, buttons=buttons_words)
        else:
            return
