
def pos_feature(verb_pos, words, total_words, pre=False):
    pos_tags = ["", "", "", ""]
    if pre:
        count = 3
        position = verb_pos - 1
        while count >= 0 and position >= 0:
            node = words[position]
            tag = node.get_tag()
            if tag and tag[0] == 'F':
                # We ignore punctuation marks
                position -= 1
                continue
            elif tag and tag[0] == 'V':
                # Remove Type and Mode from Verb tag
                tag = tag[:2] + tag[4:]
            pos_tags[count] = tag
            position -= 1
            count -= 1
    else:
        count = 0
        position = verb_pos + 1
        while count < 4 and position < total_words:
            node = words[position]
            tag = node.get_tag()
            if tag and tag[0] == 'F':
                # We ignore punctuation marks
                position += 1
                continue
            elif tag and tag[0] == 'V':
                # Remove Type and Mode from Verb tag
                tag = tag[:2] + tag[4:]
            pos_tags[count] = tag
            position += 1
            count += 1

    return pos_tags
