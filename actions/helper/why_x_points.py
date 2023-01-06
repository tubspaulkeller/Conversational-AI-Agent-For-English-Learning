from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.helper.debug import debug
from actions.gamification.handle_user_scoring import user_score


class ActionRepeatLastQuest(Action):
    def name(self) -> Text:
        return "action_why_x_points"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message.get('entities')
        try:
            value = entities[0]['value']
        except:
            value = ""
            dispatcher.utter_message(
                text="Ich habe dich leider nicht verstanden. Bitte wiederhole deine Eingabe.")

        if value == "5":
            dispatcher.utter_message(
                text="5 Punkte sind die maximale Punktzahl, die du für eine Aufgabe bekommen kannst. Du hast also die Aufgabe im ersten Versuch richtig gelöst. Mach weiter so!")
        elif value == "4":
            dispatcher.utter_message(
                text="Sobald du 4 Punkte bekommen hast, hast du zuvor einen Fehler gemacht, bevor du die Aufgabe richtig gelöst hast.")
        elif value == "3":
            dispatcher.utter_message(
                text="Bei 3 Punkten, hast du vor deiner richtigen Antwort mindestens zwei Fehler gemacht. Dennoch hast du die Aufgabe richtig gelöst, allerdings nicht direkt im ersten Versuch.")
        elif value == "2":
            dispatcher.utter_message(
                text="2 Punkte sind die minimale Punktzahl, die du für eine Aufgabe bekommen kannst. Du hast also die Aufgabe richtig gelöst, allerdings nicht im ersten Versuch.")

        return [UserUtteranceReverted(), FollowupAction(tracker.active_form.get('latest_action_name'))]
