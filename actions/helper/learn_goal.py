from actions.common.common import get_dp_inmemory_db
from datetime import datetime, date


def utter_learn_goal(dispatcher, dp_n, value, pre_text, deadline, post_text):
    text = dp_n['s_dp3_q1']["goal"][value] % deadline
    learn_goal = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "text": pre_text + "\n *%s*" % text + post_text,
                    "type": "mrkdwn"
                }
            }
        ]
    }
    dispatcher.utter_message(
        json_message=learn_goal)


def generate_learn_goal(slot, dispatcher, value, pre_text, deadline, post_text):
    utter_learn_goal(dispatcher, get_dp_inmemory_db(
        'DP3.json'), value, pre_text, deadline, post_text)
    return {slot: value}


def is_user_accepting_learn_goal(slot, value, dispatcher):
    if value == "affirm":
        dispatcher.utter_message(response="utter_affirm_learn_goal")
    else:
        dispatcher.utter_message(response="utter_s_dp3_q2/%s" % value)
    return {slot: value}


def customize_learn_goal(slot, goal, customize, dispatcher, tracker):
    date_picker = None
    goal = tracker.get_slot(goal)
    for event in reversed(tracker.events):
        if event['event'] == 'user' and event['parse_data']['intent']['name'] == 'i_date':
            date_picker = event['parse_data']['text']
            break
    if date_picker == None:
        dispatcher.utter_message(
            text="Bitte wähle ein Datum in der Zukunft aus.")
        return {slot: None}

    today = date.today().strftime("%Y-%m-%d")
    today_date = datetime.strptime(today, "%Y-%m-%d")
    user_date = datetime.strptime(date_picker, "%Y-%m-%d")

    # check if the user wants to learn longer than one year
    if tracker.get_slot(customize) == 'need_longer' and user_date.year == today_date.year:
        dispatcher.utter_message(
            text="Bitte wähle ein Datum aus, welches später als 'Ende dieses Jahres ist', da du dich entschieden hast, dir länger Zeit für dein Ziel zu nehmen.")
        return {slot: None}
    print("test", user_date, today_date)
    if user_date <= today_date:
        dispatcher.utter_message(
            text="Bitte wähle ein Datum in der Zukunft aus.")
        return {slot: None}

    utter_learn_goal(dispatcher, get_dp_inmemory_db("DP3.json"), goal, 'Ich habe dein Lernziel bezüglich des Datums angepasst:', 'zum %s' % datetime.strptime(
        date_picker, '%Y-%m-%d').strftime('%d.%m.%Y'), '\nKlicke auf den Button, um fortzufahren.')
    return {slot: date_picker}
