from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.helper.debug import debug

not_repeat_bot_actions = ['utter_rephrase/de',
                          'utter_rephrase/en', 'utter_greet']


class ActionRepeatLastQuest(Action):
    def name(self) -> Text:
        return "action_repeat_last_quest"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """ Repeats the last question of the quiz question which was asked by the bot """
        for event in reversed(tracker.events):
            if event['event'] == 'bot':
                last_action = event['metadata'].get('utter_action')
                if last_action not in not_repeat_bot_actions and last_action is not None:
                    print('debug: repeat last action', last_action)
                    if last_action.find('/button') != -1:
                        dispatcher.utter_message(
                            response=last_action.replace('button', 'msg'))
                        dispatcher.utter_message(response=last_action)
                        return [UserUtteranceReverted()]
                    else:
                        dispatcher.utter_message(response=last_action)
                        return [UserUtteranceReverted()]
            if event['event'] == 'action_execution_rejected' and event['name'] == 'get_dp_form':
                last_reminder_action = event['name']
                print('debug_reminder: repeat last action', last_reminder_action)
                return [UserUtteranceReverted(), FollowupAction("get_dp_form")]
        return []
