
import json
from dotenv import load_dotenv
import os
load_dotenv()


def get_dp_inmemory_db(json_file):
    """ load the inmemory db from json file """
    with open(json_file, "r") as jsonFile:
        return json.load(jsonFile)


def get_slots_for_dp(slots, slot_dp):
    """ get the slots for a specific dp """
    return {k: v for k, v in slots.items() if k.startswith(slot_dp)}


def get_credentials(keyname):
    try:
        return (
            os.environ[keyname]
            if os.environ[keyname] is not None
            else os.getenv(keyname)
        )
    except:
        return os.getenv(keyname)


def markdown_formatting(text):
    """ format the text to markdown """
    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "text": text,
                    "type": "mrkdwn"
                }
            }
        ]
    }


def update_required_slots(updated_slots, tracker, domain, dp_name):
    last_requested_slot = None
    # print(tracker.latest_message['intent']['name'])
    # if tracker.latest_message['intent']['name'] == 'i_ask_back_navigation':
    #   print("Called from back navigation")
    for event in reversed(tracker.events):
        if event['event'] == 'slot' and event['name'] == 'requested_slot' and event['value'] != 's_set_next_form' and event['value'] != 's_get_dp_form':
            last_requested_slot = event['value']
            if last_requested_slot != None:
                break

    for slot in domain['forms'][dp_name].get("required_slots"):
        value_of_slot = tracker.get_slot(slot)
        if value_of_slot != None and slot != last_requested_slot:
            updated_slots.remove(slot)
    return updated_slots
