from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType

buttons_forms_to_fill = {
    "s_dp1_end": {'title': 'DP1', 'payload': '/i_dp1{{"e_dp1":"DP1"}}'},
    "s_dp2_end": {'title': 'DP2', 'payload': '/i_dp2{{"e_dp2":"DP2"}}'},
    "s_dp3_g_end": {'title': 'DP3', 'payload': '/i_dp3{{"e_dp3":"DP3"}}'},
    # "s_dp3_v_end": "",
    "s_dp4_end": {'title': 'DP4', 'payload': '/i_dp4{{"e_dp4":"DP4"}}'},
    "s_dp5_end": {'title': 'DP5', 'payload': '/i_dp5{{"e_dp1":"DP5"}}'},
}


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_get_dp"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        print(tracker.active_loop["name"])
        none_slots_for_form = get_none_slots(tracker.slots)

        print("none_slots", none_slots_for_form)

        debug(self, tracker)

        buttons = []
       # shared_items = {k: x[k] for k in x if k in y and x[k] == y[k]}

        d1_keys = set(buttons_forms_to_fill.keys())
        d2_keys = set(none_slots_for_form.keys())
        shared_keys = d1_keys.intersection(d2_keys)

        print("shared_key", shared_keys)

       # dispatcher.utter_message(text = text, buttons = button_stop_emoji)
        dispatcher.utter_message(response="utter_get_dp")
        # tracker.change_loop_to
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


def get_none_slots(slots):
    return {k: v for k, v in slots.items() if k.endswith('_end') and v is None}
