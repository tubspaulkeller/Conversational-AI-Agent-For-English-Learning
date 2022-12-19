from actions.common.slack import get_user
from typing import (Text)
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, UserUtteranceReverted
##########################################################################################
# Get user credentials
##########################################################################################

greeting = ["hi", "hallo", "moin", "hey", "guten tag", "na", "good day"]


class ActionGetUserCredentials(Action):
    def name(self) -> Text:
        return "action_get_user_credentials"

    async def run(self, dispatcher, tracker, domain):
        """ get user credentials """
        if tracker.get_slot("first_name") is None:
            first_name = await get_user(tracker.sender_id, tracker)
            if first_name != None:
                dispatcher.utter_message(
                    f"Hey {first_name}! 😊\nMein Name ist Ben und ich bin dein persönlicher Assistent. Ich helfe dir dabei, deine Englisch-Fähigkeiten zu verbessern. 🤖\nFrage mich gerne jeder Zeit zu deinen:\n- erzielten Punkten 🎯\n- gesammelten Sterne 🌟\n- verdienten Abzeichen 🎖\n\n Mit 'Was war die letzte Frage' o.ä. kehren wir anschließend zur Quiz-Frage zurück.\nUm mich neuzustarten, tippe bitte 'restart' o.ä. ein. 😎")
                return [SlotSet("first_name", first_name), FollowupAction("action_set_reminder_set_dp")]
            else:
                dispatcher.utter_message(
                    f"Hey Buddy! 😊\nMein Name ist Ben und ich bin dein persönlicher Assistent. Ich helfe dir dabei, deine Englisch-Fähigkeiten zu verbessern. 🤖\nFrage mich gerne jeder Zeit zu deinen:\n- erzielten Punkte 🎯\n- gesammelten Sterne 🌟\n- verdienten Abzeichen 🎖\n\n Mit 'Was war die letzte Frage' o.ä. kehren wir anschließend zur Quiz-Frage zurück.\nUm mich neuzustarten, tippe bitte 'restart' o.ä. ein. 😎")
                return [SlotSet("first_name", "Buddy"), FollowupAction("action_set_reminder_set_dp")]
        else:
            print("DEBUG: USER CREDENTIALS ALREADY SET",
                  tracker.latest_message['text'].lower())

            if tracker.latest_message['text'].lower() in greeting:
                dispatcher.utter_message(
                    text="Wir haben bereits die Begrüßung durchgeführt. Frage mich einfach nach der letzen Frage, um fortzufahren.")
                return [UserUtteranceReverted()]
            else:
                print("HERE")
                return [FollowupAction("action_repeat_last_quest")]
