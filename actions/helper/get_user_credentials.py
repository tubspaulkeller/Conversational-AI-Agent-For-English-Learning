from actions.common.common import markdown_formatting
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
        lets_go_button = [
            {'title': "Let's go! 🚀", 'payload': '/i_lets_go{\"e_lets_go\":\"LETS_GO\"}'}]
        if tracker.get_slot("first_name") is None:
            first_name = await get_user(tracker.sender_id, tracker)
            if first_name != None:
                text = "Hi %s! 😊,\n ich bin dein Buddy Ben und ich werde dich während des Englischtrainings mit *Punkten*, *Sternen* und *Abzeichen* belohnen, damit du immer motiviert bleibst und deine Fortschritte feiern kannst. 🎉\n\n Jedes Mal, wenn du eine Frage richtig beantwortest oder eine Lektion abschließt, wirst du Punkte sammeln und Sterne verdienen, um zu zeigen, wie gut du dich schlägst. Wenn du bestimmte Ziele erreichst, wirst du außerdem Abzeichen freischalten, die deine Leistungen noch weiter unterstreichen.\nVor jeder Übung werde ich dir die jeweiligen *Spielregeln* erläutern, da diese sich *bei jeder Übung ändern können*.\n\nEgal ob du gerade erst anfängst oder schon ein fortgeschrittener Englischlerner bist - meine Belohnungen werden dir helfen, motiviert und engagiert zu bleiben. Und wenn du mal eine Frage verpasst oder Hilfe brauchst, stehe ich dir immer zur Seite.\n\nLass uns gemeinsam dein Englisch verbessern und dabei auch noch jede Menge Spaß haben!" % first_name
                dispatcher.utter_message(
                    json_message=markdown_formatting(text))

                dispatcher.utter_message(
                    text=" ", buttons=lets_go_button)

                # FollowupAction("action_set_reminder_set_dp")]
                # SlotSet("s_get_dp_form", None), SlotSet("s_set_next_form", None), FollowupAction("get_dp_form")]
                return [SlotSet("first_name", first_name)]
            else:
                text = "Hi,\n ich bin dein Buddy Ben und ich werde dich während des Englischtrainings mit *Punkten*, *Sternen* und *Abzeichen* belohnen, damit du immer motiviert bleibst und deine Fortschritte feiern kannst. 🎉\n\n Jedes Mal, wenn du eine Frage richtig beantwortest oder eine Lektion abschließt, wirst du Punkte sammeln und Sterne verdienen, um zu zeigen, wie gut du dich schlägst. Wenn du bestimmte Ziele erreichst, wirst du außerdem Abzeichen freischalten, die deine Leistungen noch weiter unterstreichen.\nVor jeder Übung werde ich dir die jeweiligen *Spielregeln* erläutern, da diese sich *bei jeder Übung ändern können*.\n\nEgal ob du gerade erst anfängst oder schon ein fortgeschrittener Englischlerner bist - meine Belohnungen werden dir helfen, motiviert und engagiert zu bleiben. Und wenn du mal eine Frage verpasst oder Hilfe brauchst, stehe ich dir immer zur Seite.\n\nLass uns gemeinsam dein Englisch verbessern und dabei auch noch jede Menge Spaß haben! Let's go! 🚀"
                dispatcher.utter_message(
                    json_message=markdown_formatting(text))
                dispatcher.utter_message(
                    text=" ", buttons=lets_go_button)
                return [SlotSet("first_name", first_name)]
                # return [SlotSet("first_name", "Buddy"), FollowupAction("action_set_reminder_set_dp")]
        else:
            print("DEBUG: USER CREDENTIALS ALREADY SET",
                  tracker.latest_message['text'].lower())

            if tracker.latest_message['text'].lower() in greeting:
                dispatcher.utter_message(
                    text="Wir haben bereits die Begrüßung durchgeführt. Frage mich einfach nach der letzen Frage, um fortzufahren.")
                return [UserUtteranceReverted()]
            else:
                print("IN USER CREDENTIALS")
               # return [FollowupAction("action_repeat_last_quest")]
                return []
