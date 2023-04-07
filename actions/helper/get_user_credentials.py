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
            {'title': "Wofür Belohnungen?", 'payload': '/i_explain_gami_elements{\"e_explain_gami_elements\":\"EXPLAIN_GAMI_ELEMENTS\"}'}]
        if tracker.get_slot("first_name") is None:
            first_name = await get_user(tracker.sender_id, tracker)
            if first_name != None:
                text = "Hi %s! 😊,\n ich bin dein Buddy Ben und ich werde dich während des Englischtrainings mit *Punkten*, *Sternen* und *Abzeichen* belohnen, damit du immer motiviert bleibst und deine Fortschritte feiern kannst. 🎉" % first_name
                dispatcher.utter_message(
                    json_message=markdown_formatting(text))

                dispatcher.utter_message(
                    text=" ", buttons=lets_go_button)

                # FollowupAction("action_set_reminder_set_dp")]
                # SlotSet("s_get_dp_form", None), SlotSet("s_set_next_form", None), FollowupAction("get_dp_form")]
                return [SlotSet("first_name", first_name)]
            else:
                text = "Hi! 😊,\n ich bin dein Buddy Ben und ich werde dich während des Englischtrainings mit *Punkten*, *Sternen* und *Abzeichen* belohnen, damit du immer motiviert bleibst und deine Fortschritte feiern kannst. 🎉"
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
