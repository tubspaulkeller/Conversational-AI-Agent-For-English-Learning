from actions.common.common import get_dp_inmemory_db
from datetime import datetime, date


def utter_learn_goal(key, dispatcher, dp_n, value, pre_text, deadline, post_text):
    text = dp_n[key]["goal"][value] % deadline
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
    return text


def generate_learn_goal(key, slot, dispatcher, value, pre_text, deadline, post_text):
    goal = utter_learn_goal(key, dispatcher, get_dp_inmemory_db(
        'DP3.json'), value, pre_text, deadline, post_text)
    return {slot: goal}


def is_user_accepting_learn_goal(slot, user_selection, value, dispatcher):
    if value == "affirm":
        if user_selection == 'oberziel':
            dispatcher.utter_message(response="utter_affirm_learn_goal")
        elif user_selection == 'vokabelziel':
            dispatcher.utter_message(
                text="Perfekt, damit hätten wir das Lernziel für die Vokabellektion für diesen Kurs festgelegt! 😁")
        elif user_selection == 'grammatikziel':
            dispatcher.utter_message(
                text="Perfekt, damit hätten wir das Lernziel für die Grammatiklektion für diesen Kurs festgelegt! 😁")
    else:
        dispatcher.utter_message(response="utter_s_dp3_q2/%s" % value)
    return {slot: value}


def customize_learn_goal(slot, goal, customize, dispatcher, tracker):
    # TODO CHECK OB DAS NONE HIER FUNKTIONIERT
    date_picker = "None"
    goal = tracker.get_slot(goal)
    for event in reversed(tracker.events):
        if event['event'] == 'user' and event['parse_data']['intent']['name'] == 'i_date':
            date_picker = event['parse_data']['text']
            break
    if date_picker == "None":
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
    key, pretext, posttext = get_key_for_json(
        tracker.slots.get("s_lg_intro"), tracker)
    goal = utter_learn_goal(key, dispatcher, get_dp_inmemory_db("DP3.json"), goal, 'Ich habe dein Lernziel bezüglich des Datums angepasst:', 'bis zum %s' % datetime.strptime(
        date_picker, '%Y-%m-%d').strftime('%d.%m.%Y'), '')
    return {slot: goal}


def get_key_for_json(user_selection, tracker):
    key = ""
    pretext = ""
    posttext = ""
    if user_selection == "oberziel":
        key = "s_dp3_q1"
        pretext = "Das klingt interessant! Ich würde daraus folgendes Lernziel forumlieren:"
        posttext = "Ende des Jahres"
    elif user_selection == "vokabelziel":
        key = "s_dp3_v_q1"
        pretext = "Das folgende Ziel basiert auf erfolgreich erreichten Lernzielen von Kommilitonen und ist nach dem bewährten SMART-Konzept formuliert:"

        if tracker.slots.get("s_lg_0") == 'Englisch-Konversation':
            posttext = "am Ende der Lektion"
        else:
            posttext = "bis zum Ende des Jahres"
    elif user_selection == "grammatikziel":
        key = "s_dp3_g_q1"
        pretext = "Das folgende Ziel basiert auf erfolgreich erreichten Lernzielen von Kommilitonen und ist nach dem bewährten SMART-Konzept formuliert:"
        posttext = "bis zum Ende des Jahres"
    return key, pretext, posttext
