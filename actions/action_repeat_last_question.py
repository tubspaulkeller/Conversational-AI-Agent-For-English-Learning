from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType

not_repeat_bot_actions = ['utter_rephrase/de', 'utter_rephrase/en']


class ActionRepeatLastQuest(Action):
    def name(self) -> Text:
        return "action_repeat_last_quest"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        bot_events = []
        for event in tracker.events:
            if event['event'] == 'bot':
                last_action = event['metadata'].get('utter_action')
                bot_events.append(last_action)

        for bot_action in reversed(bot_events):
            if bot_action not in not_repeat_bot_actions:
                #debug(self, tracker)
                print('debug: repeat last action', bot_action)
                # TODO
                # mit action einbauen
               #  dispatcher.utter_message(response=bot_action)
                break

        return []


def debug(action, tracker=None):
    output = '>>> Action: ' + action.name()
    output = '=' * min(100, len(output)) + '\n' + output
    if tracker:
        try:
            msg = tracker.latest_message
            slots = tracker.slots
            filled_slots = {}
            output += '\n- Text:       ' + str(msg['text'])
            output += '\n- Intent:     ' + str(msg['intent']['name'])
            output += '\n- Confidence: ' + str(msg['intent']['confidence'])
            output += '\n- Entities:   ' + ', '.join(msg['entities'])
            output += '\n- Slots:      '
            for slot_key, slot_value in slots.items():
                if slot_value is not None:
                    filled_slots[slot_key] = slot_value
            if len(filled_slots) > 0:
                for slot_key, slot_value in filled_slots.items():
                    output += str(slot_key) + ': ' + str(slot_value) + ', '
                output = output[:-2]
        except Exception as e:
            print(f'\n> announce: [ERROR] {e}')
    print(output)
