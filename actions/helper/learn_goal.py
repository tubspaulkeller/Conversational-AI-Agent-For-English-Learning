from actions.common.common import get_dp_inmemory_db, markdown_formatting
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

    return {slot: value}


def is_user_accepting_learn_goal(slot, user_selection, value, dispatcher):
    if value == "affirm":
        if user_selection == 'oberziel':
            dispatcher.utter_message(response="utter_affirm_learn_goal")
        elif user_selection == 'vokabelziel':
            dispatcher.utter_message(
                text="Perfekt, damit hätten wir das Lernziel für die Vokabellektion für dieses Kurses festgelegt! 😁")
        elif user_selection == 'grammatikziel':
            dispatcher.utter_message(
                text="Perfekt, damit hätten wir das Lernziel für die Grammatiklektion für dieses Kurses festgelegt! 😁")
    else:
        dispatcher.utter_message(response="utter_s_dp3_q2/%s" % value)
    return {slot: value}


def customize_learn_goal(slot, get_goal, customize, dispatcher, tracker, user_selection):
    date_picker = "None"
    goal = tracker.get_slot(get_goal)
    custom_goal = " "
    pre_text_accept = "Ich habe dein Lernziel angepasst:\n"
    pre_text_deny = "Ich habe dein Lernziel *nicht* angepasst:\n"
    is_user_accepting = tracker.get_slot(slot)

    # special case for goal "Englisch-Konversation"
    if goal == "Englisch-Konversation" and customize == 'faster':
        return custom_goal_englisch_konversation_faster(dispatcher, slot, is_user_accepting, pre_text_accept, pre_text_deny, custom_goal)
    elif goal == "Englisch-Konversation" and customize == 'need_longer':
        return custom_goal_englisch_konversation_longer(dispatcher, slot, is_user_accepting, pre_text_accept, pre_text_deny, custom_goal)

    # User want change the date
    for event in reversed(tracker.events):
        if event['event'] == 'user' and event['parse_data']['intent']['name'] == 'i_date':
            date_picker = event['parse_data']['text']
            break
    oberziel = tracker.get_slot('s_oberziel')
    print("oberziel: ", oberziel)
    if oberziel is not None:
        print("date_picker: ", oberziel[20:30])
    print("date_picker: ", date_picker)

    if date_picker == "None":
        dispatcher.utter_message(
            text="Bitte wähle ein Datum in der Zukunft aus.")
        return {slot: None}

    today = date.today().strftime("%Y-%m-%d")
    today_date = datetime.strptime(today, "%Y-%m-%d")
    user_date = datetime.strptime(date_picker, "%Y-%m-%d")

    # check if the user wants to learn longer than one year
    if customize == 'need_longer' and (user_date.month < 6 and user_date.year == today_date.year):
        dispatcher.utter_message(
            text="Bitte wähle ein Datum aus, welches später als 'Mitte diesen Jahres' ist, da du dich entschieden hast, dir länger Zeit für dein Ziel zu nehmen.")
        return {slot: None}

    if customize == 'faster' and (user_date.month >= 6 and user_date.year == today_date.year):
        dispatcher.utter_message(
            text="Bitte wähle ein Datum vor Mitte dieses Jahres aus, da du dich entschieden hast, dein Ziel schneller zu erreichen.")
        return {slot: None}
    if user_date <= today_date:
        dispatcher.utter_message(
            text="Bitte wähle ein Datum in der Zukunft aus.")
        return {slot: None}

    if tracker.get_slot('s_oberziel') is not None:
        if get_date_of_upper_goal(tracker.get_slot('s_oberziel')) < date_picker:
            dispatcher.utter_message(
                text="Bitte wähle ein Datum aus, welches vor dem Datum des Oberziels liegt.")
            return {slot: None}

    key, pretext, posttext = get_key_for_json(
        user_selection, tracker)

    custom_goal = utter_learn_goal(key, dispatcher, get_dp_inmemory_db(
        "DP3.json"), goal, 'Ich habe dein Lernziel bezüglich des Datums angepasst:', 'bis zum %s' % datetime.strptime(date_picker, '%Y-%m-%d').strftime('%d.%m.%Y'), '')

    return {slot: custom_goal}


def get_date_of_upper_goal(goal):
    if "Ende des Jahres" in goal:
        return "2023-12-31"
    else:
        return _format_date(goal[20:30])


def _format_date(date):

    print("date: ", date)
    parts = date.split('.')

    print("parts: ", parts)
    return parts[2] + '-' + parts[1] + '-' + parts[0]


def custom_goal_englisch_konversation_longer(dispatcher, slot, is_user_accepting, pre_text_accept, pre_text_deny, custom_goal):
    if is_user_accepting == "confirm":
        custom_goal = "'Ich möchte meine Gesprächsfähigkeit auf Englisch verbessern, sodass ich nach zwei Lektionen eine 20-minütige Konversation mit einem Muttersprachler führen kann.'"
        dispatcher.utter_message(
            json_message=markdown_formatting(pre_text_accept))
    elif is_user_accepting == "deny":
        custom_goal = "'Ich möchte meine Gesprächsfähigkeit auf Englisch verbessern, sodass ich nach der Lektion eine 20-minütige Konversation mit einem Muttersprachler führen kann.'"
        dispatcher.utter_message(
            json_message=markdown_formatting(pre_text_deny))
    dispatcher.utter_message(
        json_message=markdown_formatting("*%s*" % custom_goal))
    return {slot: custom_goal}


def custom_goal_englisch_konversation_faster(dispatcher, slot, is_user_accepting, pre_text_accept, pre_text_deny, custom_goal):
    if is_user_accepting == "confirm":
        custom_goal = "'Ich möchte meine Gesprächsfähigkeit auf Englisch verbessern, sodass ich nach der hälfte der Lektion eine 20-minütige Konversation mit einem Muttersprachler führen kann.'"
        dispatcher.utter_message(
            json_message=markdown_formatting(pre_text_accept))
    elif is_user_accepting == "deny":
        custom_goal = "'Ich möchte meine Gesprächsfähigkeit auf Englisch verbessern, sodass ich nach der Lektion eine 20-minütige Konversation mit einem Muttersprachler führen kann.'"
        dispatcher.utter_message(
            json_message=markdown_formatting(pre_text_deny))
    dispatcher.utter_message(
        json_message=markdown_formatting("*%s*" % custom_goal))
    return {slot: custom_goal}


def get_key_for_json(user_selection, tracker):
    key = ""
    pretext = ""
    deadline = ""
    if user_selection == "oberziel" or user_selection == "s_dp3_q1":
        key = "s_dp3_q1"
        pretext = "Das klingt interessant! Ich würde daraus folgendes Lernziel forumlieren:"
        deadline = "Ende des Jahres"
    elif user_selection == "vokabelziel" or user_selection == "s_dp3_v_q1":
        key = "s_dp3_v_q1"
        pretext = "Das folgende Ziel basiert auf erfolgreich erreichten Lernzielen von Kommilitonen und ist nach dem bewährten SMART-Konzept formuliert:"

        if tracker.slots.get("s_lg_0") == 'Englisch-Konversation' or tracker.slots.get("s_dp3_v_q1") == 'Englisch-Konversation':
            deadline = "am Ende der Lektion"
        else:
            deadline = "bis Mitte diesen Jahres"
    elif user_selection == "grammatikziel" or user_selection == "s_dp3_g_q1":
        key = "s_dp3_g_q1"
        pretext = "Das folgende Ziel basiert auf erfolgreich erreichten Lernzielen von Kommilitonen und ist nach dem bewährten SMART-Konzept formuliert:"
        deadline = "bis Mitte diesen Jahres"
    return key, pretext, deadline
