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
                text="Perfekt, damit hätten wir das Teilziel für die Vokabellektion dieses Kurses festgelegt! 😁")
        elif user_selection == 'grammatikziel':
            dispatcher.utter_message(
                text="Perfekt, damit hätten wir das Teilziel für die Grammatiklektion dieses Kurses festgelegt! 😁")
    else:
        dispatcher.utter_message(
            response="utter_s_dp3_q2/%s" % value)
    return {slot: value}


def customize_learn_goal(slot_value, slot, get_goal, customize, dispatcher, tracker, user_selection):
    goal = tracker.get_slot(get_goal)
    custom_goal = " "

    if user_selection == "oberziel" or user_selection == "s_dp3_q1":
        date_picker = "None"
        pre_text_accept = "Ich habe dein Lernziel angepasst:\n"
        pre_text_deny = "Ich habe dein Lernziel *nicht* angepasst:\n"
        is_user_accepting = tracker.get_slot(slot)

        # User want change the date
        for event in reversed(tracker.events):
            if event['event'] == 'user' and event['parse_data']['intent']['name'] == 'i_date':
                #print("event: ", event)
                date_picker = event['parse_data']['text']
                break

        if date_picker == "None":
            dispatcher.utter_message(
                text="Bitte wähle ein Datum in der Zukunft aus.")
            return {slot: None}

        today = date.today().strftime("%Y-%m-%d")
        today_date = datetime.strptime(today, "%Y-%m-%d")
        user_date = datetime.strptime(date_picker, "%Y-%m-%d")

        if _check_date_range_years(user_date, today_date):
            dispatcher.utter_message(
                text="Bitte wähle ein Datum aus, welches nicht mehr als drei Jahre in der Zukunft liegt.")
            return {slot: None}

        # Oberziel anpassen need longer
        if customize == 'need_longer' and (user_date.year == today_date.year):
            print("Oberziel anpassen need longer")
            dispatcher.utter_message(
                text="Bitte wähle ein Datum aus, welches später als 'Ende diesen Jahres' ist, da du dich entschieden hast, dir länger Zeit für dein Ziel zu nehmen.")
            return {slot: None}
        # Oberziel anpassen faster
        if customize == 'faster' and not _check_date_range_days(user_date, today_date) and user_date.year == today_date.year:
            dispatcher.utter_message(
                text="Erfahrungsgemäß braucht man mehrere Monate für diesen Kurs. Bitte wähle ein Datum, welches mehr als ein Monat in der Zukunft liegt.")
            return {slot: None}
        key, pretext, posttext = get_key_for_json(
            user_selection, tracker)

        custom_goal = utter_learn_goal(key, dispatcher, get_dp_inmemory_db(
            "DP3.json"), goal, 'Ich habe dein Lernziel bezüglich des Datums angepasst:', 'bis zum %s' % datetime.strptime(date_picker, '%Y-%m-%d').strftime('%d.%m.%Y'), '')
    else:
        # Teilziel anpassen
        key, pretext, posttext = get_key_for_json(
            user_selection, tracker)

        custom_goal = utter_learn_goal(key, dispatcher, get_dp_inmemory_db(
            "DP3.json"), goal, 'Ich habe dein Lernziel angepasst:', '%s' % slot_value, '')

    return {slot: custom_goal}


def _check_date_range_days(date1, date2):
    """Check if the difference between two dates is greater than 31 days"""
    delta = abs((date2 - date1).days)
    return delta > 31


def _check_date_range_years(date1, date2):
    """Check if the difference between two dates is greater than 31 days"""
    delta = abs((date2 - date1).days)
    return delta >= 3 * 365


# def custom_goal_englisch_konversation_longer(dispatcher, slot, is_user_accepting, pre_text_accept, pre_text_deny, custom_goal):
#     if is_user_accepting == "confirm":
#         custom_goal = "'Ich möchte meine Gesprächsfähigkeit auf Englisch verbessern, sodass ich nach zwei Lektionen eine 20-minütige Konversation mit einem Muttersprachler führen kann.'"
#         dispatcher.utter_message(
#             json_message=markdown_formatting(pre_text_accept))
#     elif is_user_accepting == "deny":
#         custom_goal = "'Ich möchte meine Gesprächsfähigkeit auf Englisch verbessern, sodass ich nach der Lektion eine 20-minütige Konversation mit einem Muttersprachler führen kann.'"
#         dispatcher.utter_message(
#             json_message=markdown_formatting(pre_text_deny))
#     dispatcher.utter_message(
#         json_message=markdown_formatting("*%s*" % custom_goal))
#     return {slot: custom_goal}


# def custom_goal_englisch_konversation_faster(dispatcher, slot, is_user_accepting, pre_text_accept, pre_text_deny, custom_goal):
#     if is_user_accepting == "confirm":
#         custom_goal = "'Ich möchte meine Gesprächsfähigkeit auf Englisch verbessern, sodass ich nach der hälfte der Lektion eine 20-minütige Konversation mit einem Muttersprachler führen kann.'"
#         dispatcher.utter_message(
#             json_message=markdown_formatting(pre_text_accept))
#     elif is_user_accepting == "deny":
#         custom_goal = "'Ich möchte meine Gesprächsfähigkeit auf Englisch verbessern, sodass ich nach der Lektion eine 20-minütige Konversation mit einem Muttersprachler führen kann.'"
#         dispatcher.utter_message(
#             json_message=markdown_formatting(pre_text_deny))
#     dispatcher.utter_message(
#         json_message=markdown_formatting("*%s*" % custom_goal))
#     return {slot: custom_goal}


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
            deadline = "2000"
    elif user_selection == "grammatikziel" or user_selection == "s_dp3_g_q1":
        key = "s_dp3_g_q1"
        pretext = "Das folgende Ziel basiert auf erfolgreich erreichten Lernzielen von Kommilitonen und ist nach dem bewährten SMART-Konzept formuliert:"
        deadline = "zwei"
    return key, pretext, deadline
