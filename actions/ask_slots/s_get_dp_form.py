from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.helper.debug import debug
buttons_forms_to_fill = {
    "s_dp1_end": {'title': 'DP1', 'payload': "/i_get_dp{\"e_get_dp\":\"dp1_form\"}"},
    "s_dp2_end": {'title': 'DP2', 'payload': '/i_get_dp{\"e_get_dp\":\"dp2_form\"}'},
    "s_dp3_g_end": {'title': 'DP3', 'payload': '/i_get_dp{\"e_get_dp\":\"dp3_form\"}'},
    "s_dp4_end": {'title': 'DP4', 'payload': '/i_get_dp{\"e_get_dp\":\"dp4_form\"}'},
}


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_get_dp_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> List[EventType]:
        """ User can choose his first or different DP. Each DP has a different form. Is the user finished with one DP, this DP is removed from the list of available DPs. """
        none_slots_for_form = get_none_slots_for_form(tracker.slots)
        #debug(self, tracker)
        buttons = []
        remaining_slots = get_remaining_slots(none_slots_for_form)
        for key in remaining_slots:
            buttons.append(buttons_forms_to_fill[key])

        if len(buttons) == 0:
            dispatcher.utter_message(text="You have filled all forms")
            return [SlotSet("s_get_dp_form", "done")]
        dispatcher.utter_message(text="Wähle ein DP!", buttons=buttons)
        return []


def get_none_slots_for_form(slots):
    """ returns and check the still available forms """
    return {k: v for k, v in slots.items() if k.endswith('_end') and v is None}


def get_remaining_slots(none_slots_for_form):
    """" returns the remaining forms  """
    d1_keys = set(buttons_forms_to_fill.keys())
    d2_keys = set(none_slots_for_form.keys())
    return d1_keys.intersection(d2_keys)
