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
            # if quiz ist finished, do not repeat last question
            for event in reversed(tracker.events):
                if event['event'] == 'bot':
                    last_action = event['metadata'].get('utter_action')
                    if last_action == 'utter_quest_end_give_user_score':
                        dispatcher.utter_message(
                            text="Wir haben alle Quizfragen beantwortet. Du kannst jetzt mit der gemeinsamen Lern-Session beginnen. Bis gleich. 😁")
                        return []
                    else:
                        break

            if tracker.active_loop.get('name') == 'dp1_form' or tracker.active_loop.get('name') == 'dp3_form' or tracker.active_loop.get('name') == 'dp3_form_voc' or tracker.active_loop.get('name') == 'dp3_form_gram' or tracker.active_loop.get('name') == 'dp2_form' or tracker.active_loop.get('name') == 'get_dp_form':
                return [FollowupAction("action_repeat_last_quest")]

            # dp2_application_tasks_form or dp4_form
            if tracker.active_loop.get('name') != 'dp4_form':
                return [FollowupAction("action_repeat_last_quest")]

            if len(tracker.active_loop) > 0 and tracker.active_loop["name"] == "dp4_form":
                dispatcher.utter_message(response="utter_rephrase/en")
            else:
                dispatcher.utter_message(response="utter_rephrase/de")
        except:
            print("ERROR")
        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]
