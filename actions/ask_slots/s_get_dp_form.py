import time
from typing import Any
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.common.common import markdown_formatting
from actions.helper.non_cancellable_shield import non_cancellable_shield
buttons_forms_to_fill = {
    "s_dp3_g_end": {'title': 'DP1', 'payload': '/i_get_dp{\"e_get_dp\":\"dp3_form\"}'},
    "s_dp2_part_one_end": {'title': 'DP2', 'payload': '/i_get_dp{\"e_get_dp\":\"dp2_form\"}'},
    "s_dp1_end": {'title': 'DP3', 'payload': "/i_get_dp{\"e_get_dp\":\"dp1_form\"}"},
    "s_dp4_end": {'title': 'DP4', 'payload': '/i_get_dp{\"e_get_dp\":\"dp4_form\"}'},
}


class AskForSlotAction(Action):

    def name(self) -> Text:
        return "action_ask_s_get_dp_form"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                  domain: Dict) -> List[EventType]:
        """ User can choose his first or different DP. Each DP has a different form. Is the user finished with one DP, this DP is removed from the list of available DPs. """
        none_slots_for_form = get_none_slots_for_form(tracker.slots)
        buttons = []
        remaining_slots = get_remaining_slots(none_slots_for_form)

        print("Remaining Slots: ", remaining_slots)

        for key in remaining_slots:
            buttons.append(buttons_forms_to_fill[key])

        buttons.append(
            {'title': 'Skills', 'payload': '/i_get_dp{\"e_get_dp\":\"SKILLS\"}'})

        print("Buttons: ", buttons)

        sorted_title_buttons = sort_array_by_title(buttons)
        if len(sorted_title_buttons) == 1:
            return [SlotSet("s_get_dp_form", "DONE"), SlotSet("s_set_next_form", "DONE"), FollowupAction("action_quest_end_give_user_score")]
        dispatcher.utter_message(
            json_message=markdown_formatting("Wenn du mehr über meine Fähigkeiten erfahren möchtest, dann schau doch mal unter *Skills* nach! Oder frage mich jederzeit nach diesen.\nBitte wähle ein *Design-Prinzip* (DP) aus."))
        dispatcher.utter_message(text=" ", buttons=sorted_title_buttons)
        return []


def get_none_slots_for_form(slots):
    """ returns and check the still available forms """
    return {k: v for k, v in slots.items() if k.endswith('_end') and v is None}


def get_remaining_slots(none_slots_for_form):
    """" returns the remaining forms  """
    d1_keys = set(buttons_forms_to_fill.keys())
    d2_keys = set(none_slots_for_form.keys())
    return d1_keys.intersection(d2_keys)


def sort_array_by_title(array):
    sorted_array = sorted(array, key=lambda x: x['title'])
    return sorted_array
