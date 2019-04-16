import numpy as np
import json

from ancora.ancora_corpus import AncoraCorpus

from utils import evaluator

clauses = AncoraCorpus()


dt = np.dtype('object,object,object')
clauses_list = np.array(list(clauses), dtype=dt)


def eval_features(clause, verb):
    if not clause:
        return None
    features_values = evaluator.evaluate_clause(clause, verb)
    if features_values is None:
        return None
    return features_values


def get_testing_clauses():
    np.random.seed(42)
    msk = np.random.rand(clauses.total_clauses) < 0.8
    testing_clauses = clauses_list[~msk]

    testing_set_features, sentences = zip(*[
        test_value
        for test_value
        in [
            (eval_features(clause, verb), clause)
            for (clause, verb, subject)
            in testing_clauses
        ]
        if test_value[0] is not None
    ])

    with open('testing_clauses.json', 'w') as f:
    	json.dump(sentences, f, ensure_ascii=False)



get_testing_clauses()
