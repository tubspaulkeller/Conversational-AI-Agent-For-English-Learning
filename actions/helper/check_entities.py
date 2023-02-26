

NO_PRESENT_PERFECT_EN = "That was very good already, but try to use the Present Perfect. Try to keep in mind the forming by 'have/has' + 'third form of the verb.\nGive it another shot. :)"
NO_PRESENT_PERFECT_DE = "Das war schonmal sehr gut, aber versuche das Present Perfect zu benutzen. Versuche dir die Bildung durch 'have/has' + 'dritte Form des Verbs vor Auge zu führen.\nProbiere es nochmal. :)"
NO_ALL_PARTS_OF_QUEST_EN = "You might have a typo or you didn't answer all parts of the question, unfortunately. Try to make your answer a bit more detailed.\nGive it another shot. :)"
NO_ALL_PARTS_OF_QUEST_DE = "Du hast einen Rechtschreibfehler gemacht oder du hast leider nicht alle Teile der Frage beantwortet. Versuche deine Antwort etwas ausführlicher zu machen.\nProbiere es nochmal. :)"
NO_ALL_PARTS_OF_QUEST_DE_DP2 = "Du hast leider nicht alle Teile der Frage beantwortet. Versuche in deiner Antwort alle aufgeführten Wörter zu nutzen.\nProbiere es nochmal. :)"


def exist_present_perfect(name_of_slot, entities, entities_list, dispatcher):
    print("entities: ", entities)
    for entity in entities:
        if entity in entities_list[name_of_slot]["present_perfect"]:
            return True
    message = NO_PRESENT_PERFECT_EN if name_of_slot[4] == '4' else NO_PRESENT_PERFECT_DE
    dispatcher.utter_message(text=message)
    return False


def exist_all_parts_of_question(number_of_entities, name_of_slot, entities, entities_list, dispatcher):
    if number_of_entities < entities_list[name_of_slot]["quantity"] or _check_wrong_entities(name_of_slot, entities, entities_list):
        message = NO_ALL_PARTS_OF_QUEST_EN if name_of_slot[4] == '4' else NO_ALL_PARTS_OF_QUEST_DE_DP2
        dispatcher.utter_message(text=message)
        return False
    else:
        return True


def _check_wrong_entities(name_of_slot, entities, entities_list):
    for entity in entities:
        if entity not in entities_list[name_of_slot]["entities"]:
            return True
    return False
