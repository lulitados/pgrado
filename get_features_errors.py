from ancora.ancora_corpus import AncoraCorpus
from elliphant.elliphant import ElliphantCorpus
import json
from utils.evaluator import evaluate_clause


def eval_features(clause):
    if not clause:
        return None
    features_values = evaluate_clause(clause)
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
    if not features_values:
        return None
    return dict(zip(feature_names, list(features_values)))


inf_clauses = []
nh_prev_clauses = []
nh_tot_clauses = []

elliphant_count = 0
elliphant_clauses = ElliphantCorpus()
total_clauses_elliphant = elliphant_clauses.total_clauses
for (clause, subject) in elliphant_clauses:
    print(str(elliphant_count) + ' of ' + str(total_clauses_elliphant))
    elliphant_count += 1
    evaluation = eval_features(clause)
    if evaluation is None:
        continue
    if 'INF' in evaluation and evaluation['INF'] > 5:
        inf_clauses.append({
            'corpus': 'elliphant',
            'clause': clause,
            'value': evaluation['INF']
        })
    if 'NH_PREV' in evaluation and evaluation['NH_PREV'] > 5:
        nh_prev_clauses.append({
            'corpus': 'elliphant',
            'clause': clause,
            'value': evaluation['NH_PREV']
        })
    if 'NH_TOT' in evaluation and evaluation['NH_TOT'] > 5:
        nh_tot_clauses.append({
            'corpus': 'elliphant',
            'clause': clause,
            'value': evaluation['NH_TOT']
        })


ancora_count = 0
ancora_clauses = AncoraCorpus()
total_clauses_ancora = ancora_clauses.total_clauses
for (clause, subject) in ancora_clauses:
    print(str(ancora_count) + ' of ' + str(total_clauses_ancora))
    ancora_count += 1
    evaluation = eval_features(clause)
    if evaluation is None:
        continue
    if 'INF' in evaluation and evaluation['INF'] > 5:
        inf_clauses.append({
            'corpus': 'ancora',
            'clause': clause,
            'value': evaluation['INF']
        })
    if 'NH_PREV' in evaluation and evaluation['NH_PREV'] > 5:
        nh_prev_clauses.append({
            'corpus': 'ancora',
            'clause': clause,
            'value': evaluation['NH_PREV']
        })
    if 'NH_TOT' in evaluation and evaluation['NH_TOT'] > 5:
        nh_tot_clauses.append({
            'corpus': 'ancora',
            'clause': clause,
            'value': evaluation['NH_TOT']
        })

inf_results = {
    'inf_clauses': inf_clauses,
}

nh_prev_results = {
    'nh_prev_clauses': nh_prev_clauses,
}


nh_tot_results = {
    'nh_tot_clauses': nh_tot_clauses,
}


inf_results_file = 'ev/errors_inf_results.json'
nh_prev_results_file = 'ev/errors_nh_prev_results.json'
nh_tot_results_file = 'ev/errors_nh_tot_results.json'
with open(inf_results_file, 'w') as f:
    json.dump(inf_results, f, ensure_ascii=False, indent=2)
with open(nh_prev_results_file, 'w') as f:
    json.dump(nh_prev_results, f, ensure_ascii=False, indent=2)
with open(nh_tot_results_file, 'w') as f:
    json.dump(nh_tot_results, f, ensure_ascii=False, indent=2)
