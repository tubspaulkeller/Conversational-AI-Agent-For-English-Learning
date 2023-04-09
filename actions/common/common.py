
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


def get_skills_text():
    return "Frage mich gerne jeder Zeit zu deinen:\n- erzielten Punkten 🎯\n- gesammelten Sternen 🌟\n- verdienten Abzeichen 🎖\n\nAußerdem erkläre ich dir gerne, *wofür du Punkte, Abzeichen und Sterne erhältst*, damit du genau weißt, welche Leistungen ich belohne und wie du noch besser werden kannst, frag mich einfach nach dem jeweiligen Element z.B. _Wofür stehen Sterne?_\nEbenfalls kannst du mich immer nach der Bildung bestimmter Zeitformen fragen, wie z.B. _Wie wird das *Simple Past* gebildet_.\n\nFalls wir während deinen Fragen in einem Quiz stecken, kannst du jederzeit zur *letzten Quiz-Frage oder zur DP-Auswahl zurückkehren*, frag mich einfach nach der letzten Frage bzw. nach dem Menü.\n\nUnd wenn du dein *Lernziel anpassen* möchtest, weil du vielleicht noch intensiver lernen möchtest oder dein Tempo verändern willst, dann ist das überhaupt kein Problem! Sag mir einfach bescheid, dass du dein Lernziel anpassen möchtest.\n\nFalls du mich neustarten willst, schreib mir ein einfaches *restart*. 😎"
