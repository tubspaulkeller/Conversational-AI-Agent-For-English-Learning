from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType


class ActionRepeatLastQuest(Action):
    def name(self) -> Text:
        return "action_repeat_last_quest"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        getSlotValue = ""
        for event in tracker.events:
            if event['event'] == 'slot':
                if event['name'] == 'requested_slot':
                    getSlotValue = event['value']
                 #   print(getSlotValue)
       # if getSlotValue is not None:
        #    if getSlotValue[0] == '2':
         #       dispatcher.utter_message(response='utter_ask_' + getSlotValue))
       # print("a", tracker.active_form.get('latest_action_name'))
        print("TRACKER", tracker)
        return [UserUtteranceReverted(), FollowupAction(tracker.active_form.get('latest_action_name'))]
