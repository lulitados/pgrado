import json


def get_feature_distribution(title, file):
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
        'NH_PREV',
        'NH_TOT_AGREE',
        'NH_PREV_AGREE',
        'IMPERSONAL_VERBS',
        'PRONOMINAL_ONLY_VERBS',
        'PRONOMINAL_USE_VERBS'
    ]
    result_dict = {}
    result_dict[title] = { feature: {} for feature in feature_names}

    with open(file, 'r') as in_file:
        clauses = json.load(in_file)
        for clause in clauses:
            feature_values  = clause[0]
            for name, value in zip(feature_names, feature_values):
                str_value = str(value)
                if str_value in result_dict[title][name]:
                    result_dict[title][name][str_value] += 1
                else:
                    result_dict[title][name][str_value] = 1

        for feature_keys in feature_names:
            for feature_value in result_dict[title][feature_keys].keys():
                result_dict[title][feature_keys][feature_value] /= len(clauses)
                result_dict[title][feature_keys][feature_value] = round(result_dict[title][feature_keys][feature_value], 2)

    # print("\n\n\n")
    # print(result_dict)
    # print("\n\n\n")

    return result_dict


files = [
    ('Impersonal Correct (LSVC)', './classification_errors/new_clauses/LinearSVC_imp_as_imp_3.json'),
    ('Impersonal As Subject (LSVC)', './classification_errors/new_clauses/LinearSVC_imp_as_subj_3.json'),

    ('Impersonal Correct (LR)', './classification_errors/new_clauses/LogisticRegression_imp_as_imp_3.json'),
    ('Impersonal As Subject (LR)', './classification_errors/new_clauses/LogisticRegression_imp_as_subj_3.json'),

    ('Zero Correct (LSVC)', './classification_errors/new_clauses/LinearSVC_zero_as_zero_3.json'),
    ('Zero As Subject (LSVC)', './classification_errors/new_clauses/LinearSVC_zero_as_subj_3.json'),

    ('Zero Correct (LR)', './classification_errors/new_clauses/LogisticRegression_zero_as_zero_3.json'),
    ('Zero As Subject (LR)', './classification_errors/new_clauses/LogisticRegression_zero_as_subj_3.json'),
]

all_dict = {}
for file in files:
    all_dict.update(get_feature_distribution(*file))

with open('feature_distribution_3.json', 'w') as o_file:
    o_file.write(json.dumps(all_dict, indent=4, ensure_ascii=False))
