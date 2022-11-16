from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType

buttons_forms_to_fill = {
    "s_dp1_end": {'title': 'DP1', 'payload': "/i_get_dp{\"e_get_dp\":\"dp1_form\"}"},
    "s_dp2_end": {'title': 'DP2', 'payload': '/i_get_dp{\"e_get_dp\":\"dp2_form\"}'},
    "s_dp3_g_end": {'title': 'DP3', 'payload': '/i_get_dp{\"e_get_dp\":\"dp3_form\"}'},
    "s_dp4_end": {'title': 'DP4', 'payload': '/i_get_dp{\"e_get_dp\":\"dp4_form\"}'},
    "s_dp5_end": {'title': 'DP5', 'payload': '/i_get_dp{\"e_get_dp\":\"dp5_form\"}'},
}


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_get_dp_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        none_slots_for_form = get_none_slots_for_form(tracker.slots)
        #debug(self, tracker)
        buttons = []
        remaining_slots = get_remaining_slots(none_slots_for_form)
        for key in remaining_slots:
            buttons.append(buttons_forms_to_fill[key])

        if len(buttons) == 0:  # TODO set to 4, just for testing
            dispatcher.utter_message(text="You have filled all forms")
            return [SlotSet("s_get_dp_form", "done")]
        dispatcher.utter_message(text="Wähle ein DP!", buttons=buttons)
        return []


def get_none_slots_for_form(slots):
    return {k: v for k, v in slots.items() if k.endswith('_end') and v is None}


def get_remaining_slots(none_slots_for_form):
    d1_keys = set(buttons_forms_to_fill.keys())
    d2_keys = set(none_slots_for_form.keys())
    return d1_keys.intersection(d2_keys)


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
