from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.helper.debug import debug
from actions.gamification.handle_user_scoring import user_score
from actions.common.common import get_dp_inmemory_db


class ActionRepeatLastQuest(Action):
    def name(self) -> Text:
        return "action_why_points_badges_stars"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        badges = get_dp_inmemory_db("badges.json")
        entities = tracker.latest_message.get('entities')
        value = []

        try:
            for entity in entities:
                value.append(entity['value'].lower())
        except:
            value = []
            dispatcher.utter_message(
                text="Ich habe dich leider nicht verstanden. Bitte wiederhole deine Eingabe.")
            return [UserUtteranceReverted(), FollowupAction(tracker.active_form.get('latest_action_name'))]

        # Sterne und punkte
        if len(value) == 2:
            if ((value[0] == "sterne" or value[0] == "stars") and value[1] == "punkte") or (value[0] == "punkte" and (value[1] == "sterne" or value[1] == "stars")):
                dispatcher.utter_message(
                    text="Die Punkte zeigen dir an, wie gut du die Aufgabe gelöst hast. Die volle Punktzahl bekommst du, sobald du die Aufgabe auf Anhieb richtig beantwortet hast. Je mehr Fehler du machst, desto weniger Punkte bekommst du.\nDie Sterne zeigen dir an, wie gut du dich in einem bestimmten Bereich geschlagen hast. Sie werden für mittelfristige Erfolge vergeben.")

        elif len(value) == 1:
            if value[0] == "punkte":
                dispatcher.utter_message(
                    text="Die Punkte zeigen dir an, wie gut du die Aufgabe gelöst hast. Die volle Punktzahl bekommst du, sobald du die Aufgabe auf Anhieb richtig beantwortet hast. Je mehr Fehler du machst, desto weniger Punkte bekommst du. ")
            elif value[0] == "abzeichen" or value[0] == "badges":

                if user_score["total_badges"] == 0:
                    dispatcher.utter_message(
                        text="Abzeichen werden dir für besondere Erfolge vergeben. Sie stellen also Errungenschaften dar, wenn du besonders erfolgreich gewesen bist. Zum Beispiel bekommst du ein Abzeichen, wenn du all Aufgaben auf Anhieb richtig gelöst hast.")

                else:
                    user_badges = {k: v for k, v in user_score.items() if k.startswith('badge_')
                                   and v == 1}

                    for k in user_badges.keys():
                        if k.startswith('badge_naturtalent'):
                            dispatcher.utter_message(
                                text='Abzeichen werden dir für besondere Erfolge vergeben. Sie stellen also Errungenschaften dar, wenn du besonders erfolgreich gewesen bist. Zum Beispiel hast du ein Abzeichen dafür bekommen, weil du all Aufgaben auf Anhieb richtig gelöst hast.')
                            dispatcher.utter_message(
                                image=badges['badge_naturtalent'])

                        elif k.startswith('badge_anwendungsaufgabe'):
                            dispatcher.utter_message(
                                text='Abzeichen werden dir für besondere Erfolge vergeben. Sie stellen also Errungenschaften dar, wenn du besonders erfolgreich gewesen bist. Zum Beispiel hast du ein Abzeichen dafür bekommen, weil du die Anwendungsaufgaben gelöst hast.')
                            dispatcher.utter_message(
                                image=badges['badge_anwendungsaufgabe'])

                        elif k.startswith('badge_aufstieg_level_7'):
                            dispatcher.utter_message(text='Abzeichen werden dir für besondere Erfolge vergeben. Sie stellen also Errungenschaften dar, wenn du besonders erfolgreich gewesen bist. Zum Beispiel hast du ein Abzeichen dafür bekommen, weil du das Langzeit-Szenario getestet hast, welches zeigte, sobald du mehrere Aufgaben löst, kannst du in ein höheres Level kommen, was dir duch die Abzeichen dargestellt wird.')
                            dispatcher.utter_message(
                                image=badges['badge_aufstieg_level_7'])
                            dispatcher.utter_message(
                                image=badges['badge_grammatik_basics'])
                        break
            elif value[0] == "sterne" or value[0] == "stars":
                dispatcher.utter_message(
                    text="Die Sterne zeigen dir an, wie gut du dich in einem bestimmten Bereich geschlagen hast. Sie werden für mittelfristige Erfolge vergeben.")

        return [UserUtteranceReverted(), FollowupAction(tracker.active_form.get('latest_action_name'))]
