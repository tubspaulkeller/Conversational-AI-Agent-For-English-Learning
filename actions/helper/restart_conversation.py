from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, ActionExecuted

# import function from different file
from actions.gamification.handle_user_scoring import user_score, user_score_simple_past, user_score_present_progressive
##########################################################################################
# Restart the conversation
##########################################################################################

from actions.ask_slots.s_get_dp_form import buttons_forms_to_fill


class ActionRestart(Action):
    def name(self) -> Text:
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        """ restart the conversation and sets the user score to 0 """
        user_score.update({}.fromkeys(user_score, 0))
        user_score_present_progressive.update(
            {}.fromkeys(user_score_present_progressive, 0))
        user_score_simple_past.update({}.fromkeys(user_score_simple_past, 0))

        buttons_forms_to_fill["s_dp3_g_end"] = {
            'title': 'DP1', 'payload': '/i_get_dp{\"e_get_dp\":\"dp3_form\"}'}

        dispatcher.utter_message(text="Ich habe neu gestartet. 🤖")
        # , FollowupAction("action_send_i_greet")]
        return [AllSlotsReset(),  Restarted()]
