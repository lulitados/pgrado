
def agrees(noun_tag, verb_tag):
    return ((noun_tag[0] == 'n' and noun_tag[3] == verb_tag[5]) or (
        noun_tag[0] == 'p' and noun_tag[2] == verb_tag[4] and
        noun_tag[4] == verb_tag[5]))

def get_noun_phrases(tree, verb_pos, pre, main_verb_tag):
    noun_phrases = []
    node = tree.begin()
    word = node.get_info().get_word()

    info = node.get_info().get_link().get_info()
    if info.get_label()[:2].lower() == 'sn':
        if not (pre and word.get_position() > verb_pos):
            if main_verb_tag and agrees(
                    node.get_info().get_word().get_tag().lower(),
                    main_verb_tag.lower()):
                noun_phrases.append(node)
            elif main_verb_tag is None:
                noun_phrases.append(node)

    nch = node.num_children()
    if nch > 0:
        for i in range(nch):
            d = node.nth_child_ref(i)
            if not d.begin().get_info().is_chunk():
                new_nh = get_noun_phrases(d, verb_pos, pre, main_verb_tag)
                if new_nh:
                    noun_phrases += new_nh
        ch = {}
        for i in range(nch):
            d = node.nth_child_ref(i)
            if (d.begin().get_info().is_chunk()):
                ch[d.begin().get_info().get_chunk_ord()] = d

        for i in sorted(ch.keys()):
            new_nh = get_noun_phrases(ch[i], verb_pos, pre, main_verb_tag)
            if new_nh:
                noun_phrases += new_nh

    return noun_phrases


def nh_feature(tree, verb_pos, pre=False, main_verb_tag=None):
    noun_phrases = get_noun_phrases(tree, verb_pos, pre, main_verb_tag)
    return len(noun_phrases) if len(noun_phrases) < 10 else 10
