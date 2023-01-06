from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.helper.debug import debug
from actions.gamification.handle_user_scoring import user_score


class ActionRepeatLastQuest(Action):
    def name(self) -> Text:
        return "action_call_anwendungsaufgabe"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text="Schö, dass du dich dafür entschieden hast! 😊")
        user_score['s_dp2_at_q2'] = 0
        user_score['call_anwendungsaufgabe'] = 1
        return [UserUtteranceReverted(), SlotSet("s_dp2_at_q1", None), SlotSet("s_dp2_at_q2", None), SlotSet("s_dp2_part_two_end", None), FollowupAction("dp2_application_tasks_form")]
