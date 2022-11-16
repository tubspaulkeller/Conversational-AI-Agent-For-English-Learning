from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted
from fuzzywuzzy import process
from datetime import datetime


class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_get_dp_form"

    def validate_s_get_dp_form(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {"s_get_dp_form": slot_value}
