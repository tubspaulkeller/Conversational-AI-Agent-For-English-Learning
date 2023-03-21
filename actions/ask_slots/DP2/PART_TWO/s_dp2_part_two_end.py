from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.gamification.handle_user_scoring import increase_badges, user_score


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp2_part_two_end"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ DP2 is finished, the user can choose a different DP """

        if user_score['call_anwendungsaufgabe'] == 0:
            dispatcher.utter_message(
                text="Übrigens, ich merke mir die Quiz-Fragen und werde dich demnächst nochmal daran erinnern, das Quiz zu wiederholen.\nErfahrungsgemäß lernt man nämlich Inhalte besser, wenn man sie in zunehmend größer werdenden Abständen wiederholt. Ich werde dabei helfen! 😁")
        user_score['call_anwendungsaufgabe'] = 0
        return [SlotSet("s_dp2_part_two_end", "end_part_two_of_dp2_form"), FollowupAction("action_set_reminder_set_dp")]
