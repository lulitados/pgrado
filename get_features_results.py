from ancora.ancora_corpus import AncoraCorpus
from elliphant.elliphant import ElliphantCorpus
import json
from utils.evaluator import evaluate_clause


def eval_features(clause):
    if not clause:
        return None
    features_values = evaluate_clause(clause.replace("\"", ''))
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
        'VERB_TYPE'
    ]
    if not features_values:
        return None
    return dict(zip(feature_names, list(features_values)))


features_results = []

elliphant_clauses = ElliphantCorpus()
for (clause, subject) in elliphant_clauses:
    clause_features = eval_features(clause)
    if clause_features is not None:
        features_results.append(clause_features)


ancora_clauses = AncoraCorpus()
for (clause, subject) in ancora_clauses:
    clause_features = eval_features(clause)
    if clause_features is not None:
        features_results.append(clause_features)


results_per_feature = {}
results_per_feature["PARSER"] = list(set([result["PARSER"] for result in features_results if "PARSER" in result])),
results_per_feature["LEMMA"] = list(set([result["LEMMA"] for result in features_results if "LEMMA" in result])),
results_per_feature["NUMBER"] = list(set([result["NUMBER"] for result in features_results if "NUMBER" in result])),
results_per_feature["PERSON"] = list(set([result["PERSON"] for result in features_results if "PERSON" in result])),
results_per_feature["INF"] = list(set([result["INF"] for result in features_results if "INF" in result])),
results_per_feature["POS_PRE_0"] = list(set([result["POS_PRE_0"] for result in features_results if "POS_PRE_0" in result])),
results_per_feature["POS_PRE_1"] = list(set([result["POS_PRE_1"] for result in features_results if "POS_PRE_1" in result])),
results_per_feature["POS_PRE_2"] = list(set([result["POS_PRE_2"] for result in features_results if "POS_PRE_2" in result])),
results_per_feature["POS_PRE_3"] = list(set([result["POS_PRE_3"] for result in features_results if "POS_PRE_3" in result])),
results_per_feature["POS_POS_0"] = list(set([result["POS_POS_0"] for result in features_results if "POS_POS_0" in result])),
results_per_feature["POS_POS_1"] = list(set([result["POS_POS_1"] for result in features_results if "POS_POS_1" in result])),
results_per_feature["POS_POS_2"] = list(set([result["POS_POS_2"] for result in features_results if "POS_POS_2" in result])),
results_per_feature["POS_POS_3"] = list(set([result["POS_POS_3"] for result in features_results if "POS_POS_3" in result])),
results_per_feature["SE"] = list(set([result["SE"] for result in features_results if "SE" in result])),
results_per_feature["A"] = list(set([result["A"] for result in features_results if "A" in result])),
results_per_feature["NH_TOT"] = list(set([result["NH_TOT"] for result in features_results if "NH_TOT" in result])),
results_per_feature["NH_PREV"] = list(set([result["NH_PREV"] for result in features_results if "NH_PREV" in result]))
results_per_feature["NH_TOT_AGREE"] = list(set([result["NH_TOT_AGREE"] for result in features_results if "NH_TOT_AGREE" in result])),
results_per_feature["NH_PREV_AGREE"] = list(set([result["NH_PREV_AGREE"] for result in features_results if "NH_PREV_AGREE" in result]))
results_per_feature["VERB_TYPE"] = list(set([result["VERB_TYPE"] for result in features_results if "VERB_TYPE" in result]))


features_results_file = 'ev/features_results.json'
with open(features_results_file, 'w') as f:
    json.dump(results_per_feature, f, ensure_ascii=False, indent=2)
