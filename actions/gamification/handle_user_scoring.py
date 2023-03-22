###########################################################################################################
##### Methods for user_scoring #####
############################################################################################################

""" These methods are used by DP1, DP2 and DP3"""

user_score = {
    "total_points": 0,
    "stars": 0,
    "total_badges": 0,

    "badge_grammatik_profi": 0,
    "badge_60_prozent": 0,
    "badge_naturtalent": 0,
    "badge_anwendungsaufgabe": 0,
    "badge_aufstieg_level_7": 0,
    "badge_grammatik_basics": 0,

    "tries": 0,  # nach jedem DP auf null setzen
    "last_question_correct": 0,
    "not_first_attempt": 0,
    "DP1_q_points": 0,
    "DP2_q_points": 0,
    "DP2_a_points": 0,
    "DP3_g_points": 0,
    "DP3_v_points": 0,
    "DP4_q_points": 0,
    "s_dp4_q1A": 0,
    "s_dp4_q1B": 0,
    "s_dp4_q2A": 0,
    "s_dp4_q2B": 0,
    "s_dp4_q3A": 0,
    "s_dp4_q3B": 0,
    "call_anwendungsaufgabe": 0,
    "s_dp2_at_q2": 0,
    "s_dp2_at_q3": 0,
    "s_dp2_at_q4": 0,
}

user_score_simple_past = {
    "s_dp1_q1": 0,
    "s_dp1_q2": 0,
    "s_dp1_q3": 0,
    # "s_dp1_q4": 0,
    "s_dp1_q5": 0,
    "s_dp1_q6": 0,
    "s_dp1_q7": 0,
    # "s_dp1_q8": 0,
    "s_dp1_q9": 0,
    # "s_dp1_q10": 0,
    "s_dp1_q11": 0,
    # "s_dp1_q12": 0,
}

user_score_present_progressive = {
    "s_dp1_q4": 0,
    "s_dp1_q8": 0,
    "s_dp1_q10": 0,
    "s_dp1_q12": 0,
}


def get_tries():
    """ returns the number of tries the user has done """
    return user_score["tries"]


def set_points(points, dp):
    """ sets the points of the user """
    user_score["total_points"] += points
    user_score['DP'+dp+'_points'] += points
    user_score["last_question_correct"] = 1


def increase_tries():
    """ increases the number of tries the user has done """
    user_score["tries"] += 1


def increase_badges(badge):
    user_score["total_badges"] += 1
    user_score[badge] += 1


def increase_stars():
    user_score["stars"] += 1


def resetTries():
    """ resets the number of tries the user has done """
    user_score["tries"] = 0
