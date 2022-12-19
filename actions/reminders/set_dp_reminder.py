import datetime
from rasa_sdk.events import ReminderScheduled, ReminderCancelled, FollowupAction, SlotSet
from rasa_sdk import Action
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionSetReminderSetDP(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_set_reminder_set_dp"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        date = datetime.datetime.now() + datetime.timedelta(seconds=3)
        print("SET REMINDER - DP-FORM")
        reminder = ReminderScheduled(
            "EXTERNAL_reminder_set_dp",
            trigger_date_time=date,
            name="set_dp_reminder",
            kill_on_user_message=False,
        )

        # check if the user has already finished the quest
        for event in reversed(tracker.events):
            if event['event'] == 'bot':
                last_action = event['metadata'].get('utter_action')
                if last_action == 'utter_quest_end_give_user_score':
                    dispatcher.utter_message(
                        text="Wir haben alle Quizfragen beantwortet. Du kannst jetzt mit der gemeinsamen Lern-Session beginnen. Bis gleich. 😁")
                    return []

        return [reminder, SlotSet("s_get_dp_form", None), SlotSet("s_set_next_form", None)]


class ActionReactToReminderSetDP(Action):
    """Reminds the user to call someone."""

    def name(self) -> Text:
        return "action_react_to_reminder_set_dp"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print("REACT TO REMINDER: DP-FORM")
        return [FollowupAction("get_dp_form"), ReminderCancelled()]
