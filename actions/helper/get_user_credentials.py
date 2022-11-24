from pathlib import Path
import json
from actions.common.slack import slackitems
from slack_sdk.web.async_client import AsyncWebClient
#from slack import WebClient
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.domain import Domain, State
from rasa.shared.core.slots import AnySlot, Slot
from rasa.shared.core.events import (
    UserUttered,
    ActionExecuted,
    Event,
    Restarted,
    ActionReverted,
    UserUtteranceReverted,
    BotUttered,
    ActiveLoop,
    SessionStarted,
    ActionExecutionRejected,
    DefinePrevUserUtteredFeaturization,
)
from typing import (
    Dict,
    Text,
    Any,
    Optional,
    Iterator,
    Generator,
    Type,
    TypeVar,
    List,
    Deque,
    Iterable,
    Union,
    FrozenSet,
    Tuple,
    TYPE_CHECKING,
    cast,
)
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, FollowupAction, AllSlotsReset, Restarted, SlotSet, EventType
# from rasa_core.trackers import DialogueStateTracker
# from rasa_core.domain import Domain
from rasa.shared.core import events
from rasa.shared.core.constants import (
    ACTION_LISTEN_NAME,
    LOOP_NAME,
    SHOULD_NOT_BE_SET,
    PREVIOUS_ACTION,
    ACTIVE_LOOP,
    ACTION_SESSION_START_NAME,
    FOLLOWUP_ACTION,
)
from rasa.core.tracker_store import TrackerStore
from actions.helper.rephrase import ActionRephrase

import os
from dotenv import load_dotenv
load_dotenv()
##########################################################################################
# Get user credentials
##########################################################################################


class ActionGetUserCredentials(Action):
    def name(self) -> Text:
        return "action_get_user_credentials"

    @staticmethod
    async def update():
        # Tracker.update_conversation_with_events(new_tracker)
        here = Path(__file__).parent.resolve()
        return Tracker.from_dict(json.load(open(here / "./new_tracker.json")))

    async def run(self, dispatcher, tracker, domain):
        """ get user credentials """
        user_id, first_name, channel_id = await slackitems(tracker)
        # TODO SAVE CHANNEL ID INTO SLOT
        print("channelID", channel_id)
        print("tracker_id", tracker.sender_id)

        # here = Path(__file__).parent.resolve()

        # NEW_TRACKER = Tracker.from_dict(
        #     json.load(open(here / "./new_tracker.json")))

        # new_tracker = await self.update()

        # print(tracker.current_state())
        # tracker.sender_id = channel_id

        # t1 = DialogueStateTracker(sender_id, domain.slots)

        #tracker_child = TrackerChild(channel_id, None)

        # await tracker_child.from_events()

        #tracker_store_child = TrackerStoreChild(domain)
        # await tracker_store_child.create_tracker(channel_id)

        # tracker2 = TrackerStore.init_tracker(
        #     self, sender_id=channel_id)
        # print(tracker2)
       # slots = self.fetch_slots(tracker)
        #updated_slots = domain_slots.copy()
        #print("slots: ", slots)
        #tr = DialogueStateTracker(sender_id=channel_id, slots=slots)
        #print("tr.id", tr.sender_id)

        # action = ActionRephrase()
        # events = await action.run(dispatcher, tr, domain)
        # print("test", events)
        if first_name != None:
            # TODO replace with utter_greet
            dispatcher.utter_message(f"Hey {first_name}! 😊")
            return [SlotSet("user_id", user_id), SlotSet("first_name", first_name)]
        else:
            # TODO replace with utter_greet/no_username
            dispatcher.utter_message(f"Hey Buddy! 😊")
            return [SlotSet("user_id", user_id), SlotSet("first_name", "Buddy")]

    @staticmethod
    def fetch_slots(tracker):
        slots = []
        slots_to_keep = []

        for slot_name in slots_to_keep:
            slot_value = tracker.get_slot(slot_name)
            if slot_value is not None:
                slots.append(SlotSet(key=slot_name, value=slot_value))

        return slots


class TrackerStoreChild(TrackerStore):
    print("TrackerStroeChild")

    async def create_tracker(
        self, sender_id: Text, append_action_listen: bool = True
    ) -> DialogueStateTracker:
        """Creates a new tracker for `sender_id`.

        The tracker begins with a `SessionStarted` event and is initially listening.

        Args:
            sender_id: Conversation ID associated with the tracker.
            append_action_listen: Whether or not to append an initial `action_listen`.

        Returns:
            The newly created tracker for `sender_id`.
        """

        tracker = self.init_tracker(sender_id)
        print("tracker", tracker)
        if append_action_listen:
            tracker.update(ActionExecuted(ACTION_LISTEN_NAME))

        await self.save(tracker)

        return tracker


class TrackerChild(DialogueStateTracker):

    def __init__(self, *args: Any, **kwds: Any) -> Any:
        return super().__init__(*args, **kwds)

    def __call__(*args, **kwargs):
        print("TrackerChild called")

    async def from_events(
        cls,
        sender_id: Text = None,
        evts: List[Event] = None,
        slots: Optional[Iterable[Slot]] = None,
        max_event_history: Optional[int] = None,
        sender_source: Optional[Text] = None,
        domain: Optional[Domain] = None,
    ) -> "DialogueStateTracker":
        """Creates tracker from existing events.

        Args:
            sender_id: The ID of the conversation.
            evts: Existing events which should be applied to the new tracker.
            slots: Slots which can be set.
            max_event_history: Maximum number of events which should be stored.
            sender_source: File source of the messages.
            domain: The current model domain.

        Returns:
            Instantiated tracker with its state updated according to the given
            events.
        """
        print("HERE")
        sender_id = await get_channel()

        tracker = cls(sender_id, slots, max_event_history, sender_source)

        print(tracker)  # still none

        # for e in evts:
        #     tracker.update(e, domain)

        return tracker


client = AsyncWebClient(
    token=os.getenv('SLACK_TOKEN'))


async def get_channel():
    channel = await client.users_conversations()
    for channel in channel['channels']:
        return channel['id']
