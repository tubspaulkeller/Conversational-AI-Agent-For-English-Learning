from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted, FollowupAction
from rasa_sdk.executor import CollectingDispatcher


class ActionRephrase(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_rephrase"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("debug: rephrase action", len(tracker.active_loop))
        print("REPHRASE", tracker.sender_id)
       # print(tracker.active_loop["name"])
        try:
            if tracker.active_loop.get('name') == 'get_dp_form':
                return [FollowupAction("action_repeat_last_quest")]

            if len(tracker.active_loop) > 0 and tracker.active_loop["name"] == "dp4_form":
                dispatcher.utter_message(response="utter_rephrase/en")
            else:
                dispatcher.utter_message(response="utter_rephrase/de")
        except:
            print("ERROR")
        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]
