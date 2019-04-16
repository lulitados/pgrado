def has_subject(node):
    info = node.get_info()

    word = node.get_info().get_word()
    found_subject = False
    tag = None
    if 'subj' in info.get_label():
        found_subject, tag = (True, word.get_tag())

    nch = node.num_children()
    if not found_subject and nch > 0:
        for i in range(nch):
            d = node.nth_child_ref(i)
            if (not d.begin().get_info().is_chunk()):
                found_subject, tag = has_subject(d.begin())
                if found_subject:
                    break

    if not found_subject and nch > 0:
        ch = {}
        for i in range(nch):
            d = node.nth_child_ref(i)
            if (d.begin().get_info().is_chunk()):
                ch[d.begin().get_info().get_chunk_ord()] = d

        for i in sorted(ch.keys()):
            found_subject, tag = has_subject(ch[i].begin())
            if found_subject:
                break

    return found_subject, tag
