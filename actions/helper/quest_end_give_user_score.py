from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
from actions.helper.debug import debug
from actions.gamification.handle_user_scoring import user_score


class ActionEndDPs(Action):
    def name(self) -> Text:
        return "action_quest_end_give_user_score"

    def run(self, dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """ total points are given to the user """
        try:

            if tracker.get_slot("first_name") is None:

                dispatcher.utter_message(response="utter_quest_end_give_user_score_2",
                                         total_points__end_game=user_score["total_points"], name="Buddy")
            else:
                dispatcher.utter_message(response="utter_quest_end_give_user_score_2",
                                         total_points__end_game=user_score["total_points"], name=tracker.get_slot("first_name"))
            # dispatcher.utter_message(
            #   text="Du hast insgesamt: {} Punkte erreicht. 🎉\nAls nächstes werden wir eine gemeinsame Lern-Session durchführen, da dies eine gute Möglichkeit ist, dein neu erlerntes Englisch-Wissen mit anderen Kommilitonen auszuprobieren!\nDafür wirst du einem Team mit Lern-Partnern, die auf dem gleichen Lern-Level sind wie du, zugeteilt.\nAllerdings, müssen wir dafür in einen Gruppenchat wechseln. Wir sehen uns gleich im anderen Channel {}! 😊".format(user_score["total_points"], tracker.get_slot("first_name")))
        except Exception as e:
            print("Error in action_quest_end_give_user_score: ", e)
        return []
