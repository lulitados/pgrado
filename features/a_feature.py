
def a_feature(words):
    for word in words:
        if word.get_tag() == 'SP' and word.get_lemma().lower() == 'a':
            return True
    return False
