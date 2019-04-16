
def infs_feature(words):
    infs_words = [word for word in words
                  if word.get_tag()[0] == 'V' and word.get_tag()[2] == 'N']
    return len(infs_words) if len(infs_words) < 10 else 10
