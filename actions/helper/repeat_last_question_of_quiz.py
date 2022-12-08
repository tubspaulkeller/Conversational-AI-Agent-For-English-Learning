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
        bot_events = []
        for event in tracker.events:
            if event['event'] == 'bot':
                last_action = event['metadata'].get('utter_action')
                bot_events.append(last_action)

        for bot_action in reversed(bot_events):
            if bot_action not in not_repeat_bot_actions and bot_action is not None:
                print('debug: repeat last action', bot_action)
                dispatcher.utter_message(response=bot_action)
                break

        return []
