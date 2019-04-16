from ev.features_results import FEATURE_RESULTS

feature_names = [
    'PARSER',
    'LEMMA',
    'NUMBER',
    'PERSON',
    'INF',
    'POS_PRE_0',
    'POS_PRE_1',
    'POS_PRE_2',
    'POS_PRE_3',
    'POS_POS_0',
    'POS_POS_1',
    'POS_POS_2',
    'POS_POS_3',
    'SE',
    'A',
    'NH_TOT',
    'NH_PREV'
]


def create_vector(result, subject):
    vector = []
    for feature in feature_names:
        if feature in result and result[feature] in FEATURE_RESULTS[feature]:
            vector.append(FEATURE_RESULTS[feature].index(result[feature]))
        else:
            vector.append(0)
    return (dict(zip(feature_names, vector)), subject)
