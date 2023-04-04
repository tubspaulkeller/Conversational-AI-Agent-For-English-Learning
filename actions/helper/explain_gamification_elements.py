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
        return "action_explain_gamification_elements"

    async def run(self, dispatcher, tracker, domain):
        """ get user credentials """
        lets_go_button = [
            {'title': "Hinweis zu den Spielregeln", 'payload': '/i_hint_rules{\"e_hint_rules\":\"HINT_FOR_RULES\"}'}]

        text = "Jedes Mal, wenn du eine Frage richtig beantwortest oder eine Lektion abschließt, wirst du *Punkte* sammeln und *Sterne* verdienen, um zu zeigen, wie gut du dich schlägst. Wenn du bestimmte Ziele erreichst, wirst du außerdem *Abzeichen* freischalten, die deine Leistungen noch weiter unterstreichen."
        dispatcher.utter_message(
            json_message=markdown_formatting(text))

        dispatcher.utter_message(
            text=" ", buttons=lets_go_button)

        return []
