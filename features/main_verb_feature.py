
def finit_verb_clause(words, verb_info):
    for word in words:
        if (word.get_tag() == verb_info['tag'] and
                word.get_form() == verb_info['form'] and
                word.get_lemma() == verb_info['lemma']):
            return word
    return ""
