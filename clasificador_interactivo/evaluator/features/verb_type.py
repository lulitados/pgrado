from .verb_lists import impersonal_verbs, pronominal_only_verbs, pronominal_use_verbs

def verb_type(verb):

    # print(verb)
    return (
        True if verb in impersonal_verbs.IMPERSONAL_VERBS else False,
        True if verb in pronominal_only_verbs.PRONOMINAL_ONLY_VERBS else False,
        True if verb in pronominal_use_verbs.PRONOMINAL_USE_VERBS else False
    )
