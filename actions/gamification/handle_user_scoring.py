###########################################################################################################
##### Methods for user_scoring #####
############################################################################################################

""" These methods are used by DP1, DP2 and DP3""" 

user_score = {
"points": 0,
"stars": 0,
"total_badges": 0,
"tries": 0,  # nach jedem DP auf null setzen
"last_question_correct": 0,
"not_first_attempt": 0,
}

def get_tries():
    """ returns the number of tries the user has done """
    return user_score["tries"]


def set_points(points):
    """ sets the points of the user """
    user_score["points"] += points
    user_score["last_question_correct"] = 1


def increase_tries():
    """ increases the number of tries the user has done """
    user_score["tries"] += 1


def resetTries():
    """ resets the number of tries the user has done """
    user_score["tries"] = 0


def reset_user_score():
    """ resets the user score when the user finished a quiz """
    user_score.update({}.fromkeys(user_score, 0))