import json

def get_dp_inmemory_db(json_file):
    with open(json_file, "r") as jsonFile:
        return json.load(jsonFile)

def get_slots_for_dp(slots, slot_dp):
    return {k: v for k, v in slots.items() if k.startswith(slot_dp)}
    