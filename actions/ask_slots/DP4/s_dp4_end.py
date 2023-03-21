from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.gamification.handle_user_scoring import user_score
from actions.helper.non_cancellable_shield import non_cancellable_shield


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_dp4_end"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                  domain: Dict) -> List[EventType]:
        """ DP4 is finished, the user can choose a different DP """

       # await non_cancellable_shield(asyncio.sleep(2))
        dispatcher.utter_message(
            response="utter_dp4_finish", total_points=user_score['DP4_q_points'])
        return [SlotSet("s_dp4_end", "end_of_dp4_form"),  FollowupAction("action_set_reminder_set_dp")]


# We want to get to the coliseum
# How much does it cost
# Can I get two tickets pls
# Do you offer a discount for students
# We have lived in Eldoria since 2000
