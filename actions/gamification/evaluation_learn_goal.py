

def give_user_feedback_on_learn_goal_if_he_changes(slot_value, goal_slot_value, overall_goal_slot_value, dp_n, tracker, dispatcher):
    learn_goal = dp_n[slot_value][tracker.get_slot(
        goal_slot_value)]
    dispatcher.utter_message(
        text="Alles klar, %s" % learn_goal)
    dispatcher.utter_message(
        text="Auch mit dieser Anpassung befindest du dich weiterhin auf einem guten Weg, dein übergeordnetes Lernziel dieses Kurses zu erreichen! Weiter so!")
    overall_learn_goal = get_overall_learn_goal(
        dp_n, overall_goal_slot_value, tracker)
    dispatcher.utter_message(json_message=overall_learn_goal)


def get_overall_learn_goal(dp_n, overall_goal_slot_value, tracker):
    # TODO OVERALL GOAL ANPASSEN
    oberziel = tracker.get_slot("s_oberziel")
    print("oberziel: ", oberziel)
    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "text": "*Hauptziel: %s*" % oberziel,
                    "type": "mrkdwn"
                }
            }
        ]
    }


def give_user_feedback_on_learn_goal_with_no_change(overall_goal_slot_value, dp_n, tracker, dispatcher):
    dispatcher.utter_message(
        text="Du befindest dich weiterhin auf einem guten Weg, dein übergeordnetes Lernziel dieses Kurses zu erreichen! Weiter so!")
    overall_learn_goal = get_overall_learn_goal(
        dp_n, overall_goal_slot_value, tracker)
    dispatcher.utter_message(json_message=overall_learn_goal)
