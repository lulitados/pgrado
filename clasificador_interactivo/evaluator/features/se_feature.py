def se_feature(words, verb_position, total_words):
    se_positions = [
        verb_position - 2,
        verb_position - 1,
        verb_position + 1,
        verb_position + 2
    ]
    for pos in se_positions:
        if pos < total_words and pos >= 0:
            word = words[pos]
            if word.get_form().lower() == 'se':
                return True
    return False
