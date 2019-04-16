import sys
import numpy as np
from sklearn.preprocessing import CategoricalEncoder

from elliphant.elliphant_corpus import ElliphantCorpus
from ancora.ancora_corpus import AncoraCorpus
from corin.corin_corpus import CorinCorpus

from utils import evaluator

dev_corpus = ["elliphant", "ancora"]

corpus_name = sys.argv[1] if len(sys.argv) > 1 else "ancora"
if corpus_name == "elliphant":
    clauses = ElliphantCorpus()
elif corpus_name == 'corin':
    clauses = CorinCorpus()
else:
    clauses = AncoraCorpus()

print("Trabajando con el corpus de " + corpus_name)

dt = np.dtype('object,object,object')
clauses_list = np.array(list(clauses), dtype=dt)


def eval_features(clause, verb):
    if not clause:
        return None
    features_values = evaluator.evaluate_clause(clause, verb)
    if features_values is None:
        return None
    return features_values


if corpus_name in dev_corpus:
    np.random.seed(42)
    msk = np.random.rand(clauses.total_clauses) < 0.8
    training_clauses = clauses_list[msk]
    testing_clauses = clauses_list[~msk]

    training_set_features, training_set_values = zip(*[
        train_value
        for train_value
        in [
            (eval_features(clause, verb), subject)
            for (clause, verb, subject)
            in training_clauses
        ]
        if train_value[0] is not None
    ])
    testing_set_features, testing_set_values = zip(*[
        test_value
        for test_value
        in [
            (eval_features(clause, verb), subject)
            for (clause, verb, subject)
            in testing_clauses
        ]
        if test_value[0] is not None
    ])

    training_values_file = np.memmap(
        corpus_name + '_training_values.memmap',
        dtype='U50',
        mode='w+',
        shape=(len(training_set_values)))
    training_values_file[:] = np.array(training_set_values)[:]

    testing_values_file = np.memmap(
        corpus_name + '_testing_values.memmap',
        dtype='U50',
        mode='w+',
        shape=(len(testing_set_values)))
    testing_values_file[:] = np.array(testing_set_values)[:]

    training_data = np.array(training_set_features)
    training_data_file = np.memmap(
        corpus_name + '_training_data.memmap',
        dtype='U50',
        mode='w+',
        shape=(training_data.shape[0], training_data.shape[1]))
    training_data_file[:] = training_data[:]
    del training_data

    enc = CategoricalEncoder(handle_unknown='ignore')
    enc.fit(training_data_file[:, :22])

    training_CE = enc.transform(training_data_file[:, :22]).toarray()

    training_full_data = np.memmap(
        corpus_name + '_training_full_data.memmap',
        dtype='float32',
        mode='w+',
        shape=(training_CE.shape[0], training_CE.shape[1] + 300))
    # Copies encoded data into the training matrix
    training_full_data[:, 0:training_CE.shape[1]] = training_CE
    # Copies vector data into training matrix
    training_full_data[:, training_CE.shape[1]:] = training_data_file[:, 22:]

    testing_data = np.array(testing_set_features)
    testing_data_file = np.memmap(
        corpus_name + '_testing_data.memmap',
        dtype='U50',
        mode='w+',
        shape=(testing_data.shape[0], testing_data.shape[1]))
    testing_data_file[:] = testing_data[:]
    del testing_data

    testing_CE = enc.transform(testing_data_file[:, :22]).toarray()

    testing_full_data = np.memmap(
        corpus_name + '_testing_full_data.memmap',
        dtype='float32',
        mode='w+',
        shape=(testing_CE.shape[0], testing_CE.shape[1] + 300))
    # Copies encoded data into the testing matrix
    testing_full_data[0:testing_CE.shape[0], 0:testing_CE.shape[1]] = testing_CE
    # Copies vector data into testing matrix
    testing_full_data[:, testing_CE.shape[1]:] = testing_data_file[:, 22:]

else:
    # No se entrena con Corin, solo para evaluacion
    all_clauses = clauses_list

    training_values_file = np.memmap(
        'ancora_training_values.memmap',
        dtype='U50',
        mode='r')

    training_data_file = np.memmap(
        'ancora_training_data.memmap',
        dtype='U50',
        mode='r',
        shape=(training_values_file.shape[0], 322))

    enc = CategoricalEncoder(handle_unknown='ignore')
    enc.fit(training_data_file[:, :22])

    training_CE = enc.transform(training_data_file[:, :22]).toarray()

    testing_set_features, testing_set_values = zip(*[
        test_value
        for test_value
        in [
            (eval_features(clause, verb), subject)
            for (clause, verb, subject)
            in all_clauses
        ]
        if test_value[0] is not None
    ])

    testing_values_file = np.memmap(
        corpus_name + '_testing_values.memmap',
        dtype='U50',
        mode='w+',
        shape=(len(testing_set_values)))
    testing_values_file[:] = np.array(testing_set_values)[:]

    testing_data = np.array(testing_set_features)
    testing_data_file = np.memmap(
        corpus_name + '_testing_data.memmap',
        dtype='U50',
        mode='w+',
        shape=(testing_data.shape[0], testing_data.shape[1]))
    testing_data_file[:] = testing_data[:]
    del testing_data

    testing_CE = enc.transform(testing_data_file[:, :22]).toarray()

    testing_full_data = np.memmap(
        corpus_name + '_testing_full_data.memmap',
        dtype='float32',
        mode='w+',
        shape=(testing_CE.shape[0], testing_CE.shape[1] + 300))
    # Copies encoded data into the testing matrix
    testing_full_data[0:testing_CE.shape[0], 0:testing_CE.shape[1]] = testing_CE
    # Copies vector data into testing matrix
    testing_full_data[:, testing_CE.shape[1]:] = testing_data_file[:, 22:]

print("Creados los memmaps para el corpus de " + corpus_name)
