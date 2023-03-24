from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.common.common import get_dp_inmemory_db
from actions.gamification.evaluation_learn_goal import give_user_feedback_on_learn_goal_if_he_changes, give_user_feedback_on_learn_goal_with_no_change
from actions.helper.learn_goal import get_key_for_json


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp3_g_end"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ The next form get called depending on the user input. If the user choosed before vocabluary, the form grammar is called. If the user choosed before grammar, the form grammar is called. """
        dp_3 = get_dp_inmemory_db("DP3.json")

        # generate goal for vocabulary form
        topic = tracker.slots.get("s_dp3_g_q1")
        customize = tracker.slots.get("s_dp3_g_q5")

        goal = goal = tracker.get_slot("s_dp3_g_customize_goal")
        print("goal: ", goal)
        if tracker.slots.get("s_dp3_g_q6") == "deny":
            dispatcher.utter_message(response="utter_ask_s_dp3_g_q5")
            return [SlotSet("s_dp3_g_q5", None), SlotSet("s_dp3_g_q6", None)]

        elif tracker.slots.get("s_dp3_g_q5") == "deny" or tracker.slots.get("s_dp3_g_q6") == "affirm":
            # grammar form are done by the user
            if tracker.slots.get("s_dp3_q4") == "grammar_form":
                if tracker.get_slot("s_dp3_g_q5") != "deny":
                    give_user_feedback_on_learn_goal_if_he_changes(
                        "s_dp3_g_end", "s_dp3_g_q5", "s_dp3_q1", dp_3, tracker, dispatcher)

                else:
                    give_user_feedback_on_learn_goal_with_no_change(
                        "s_dp3_q1", dp_3, tracker, dispatcher)

                dispatcher.utter_message(
                    response="utter_activate_form_via_button/g")
                return [SlotSet("s_grammatikziel", goal)]

            # both forms are finisched
            elif tracker.slots.get("s_dp3_q4") == "vocabel_form":
                if tracker.get_slot("s_dp3_g_q5") != "deny":
                    give_user_feedback_on_learn_goal_if_he_changes(
                        "s_dp3_g_end", "s_dp3_g_q5", "s_dp3_q1", dp_3, tracker, dispatcher)
                else:
                    give_user_feedback_on_learn_goal_with_no_change(
                        "s_dp3_q1", dp_3, tracker, dispatcher)
                # the user can choose a different DP
                return [SlotSet("s_dp3_g_end", "grammar_form"), FollowupAction("action_set_reminder_set_dp"), SlotSet("s_grammatikziel", goal)]
