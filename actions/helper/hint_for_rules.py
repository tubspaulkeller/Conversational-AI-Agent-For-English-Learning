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
        return "action_hint_for_rules"

    async def run(self, dispatcher, tracker, domain):
        """ get user credentials """
        lets_go_button = [
            {'title': "Let's go! 🚀", 'payload': '/i_lets_go{\"e_lets_go\":\"LETS_GO\"}'}]
        text = "Vor jeder Übung werde ich dir die jeweiligen *Spielregeln* erläutern, da diese sich *bei jeder Übung ändern können*.\n\nLass uns gemeinsam dein Englisch verbessern und dabei auch noch jede Menge Spaß haben!"
        dispatcher.utter_message(
            json_message=markdown_formatting(text))

        dispatcher.utter_message(
            text=" ", buttons=lets_go_button)
