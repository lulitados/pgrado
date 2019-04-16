import time

import numpy as np
from sklearn import cross_validation
from sklearn.preprocessing import CategoricalEncoder
from sklearn.svm import SVC
from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score

# from elliphant.elliphant import ElliphantCorpus
from ancora.ancora_corpus import AncoraCorpus

from utils.evaluator import evaluate_clause

from collections import defaultdict

start_time = time.clock()


class bcolors:
    """
    Colores para destacar el output.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'



# clauses = ElliphantCorpus()
clauses = AncoraCorpus()
dt = np.dtype('object,object')
clauses_list = np.array(list(clauses), dtype=dt)

# http://stackoverflow.com/questions/24147278/how-do-i-create-test-and-train-samples-from-one-dataframe-with-pandas
np.random.seed(42)
msk = np.random.rand(clauses.total_clauses) < 0.8
training_clauses = clauses_list[msk]
testing_clauses = clauses_list[~msk]


def eval_features(clause):
    if not clause:
        return {}
    features_values = evaluate_clause(clause)
    if features_values is None:
        return None
    return features_values


# Evaluacion del feature

new_result = {}
new_result['accuracy'] = []
new_result['precision'] = []
new_result['recall'] = []
new_result['f_measure'] = []
cv = cross_validation.KFold(
    len(training_clauses), n_folds=5, shuffle=True, random_state=None)

print("SVC Classifier")
# print("Maxent Classifier")
# print("NaiveBayes Classifier")

for traincv, evalcv in cv:

    cv_training = training_clauses.take(traincv)
    cv_testing = training_clauses.take(evalcv)

    training_set = [
        (eval_features(clause), subject) for (clause, subject) in cv_training]
    testing_set = [
        (eval_features(clause), subject) for (clause, subject) in cv_testing]

    training_set_features, training_set_values = zip(*[
        train_value
        for train_value
        in training_set
        if train_value[0] is not None
    ])
    testing_set_features, testing_set_values = zip(*[
        test_value
        for test_value
        in testing_set
        if test_value[0] is not None
    ])

    training_data = np.array(training_set_features)

    enc = CategoricalEncoder(handle_unknown='ignore')
    enc.fit(training_data[:, :19])

    training_CE = enc.transform(training_data[:, :19]).toarray()

    classifier = SVC()
    training_full_data = np.concatenate(
        (np.array(training_CE), training_data[:, 20:]), axis=1)
    classifier.fit(training_full_data, np.array(training_set_values))

    testing_data = np.array(testing_set_features)
    testing_CE = enc.transform(testing_data[:, :19]).toarray()

    testing_full_data = np.concatenate(
        (testing_CE, testing_data[:, 20:]), axis=1)
    testing_set_predicted = classifier.predict(testing_full_data)

    labels = ['SUBJECT', 'ZERO', 'IMPERSONAL', 'ERROR']
    accuracy = accuracy_score(
        testing_set_values,
        testing_set_predicted)
    new_result['accuracy'].append(accuracy)

    precision = precision_score(
        testing_set_values,
        testing_set_predicted,
        labels=labels,
        average=None)
    new_result['precision'].append(list(zip(labels, precision)))

    recall = recall_score(
        testing_set_values,
        testing_set_predicted,
        labels=labels,
        average=None)
    new_result['recall'].append(list(zip(labels, recall)))

    f_measure = f1_score(
        testing_set_values,
        testing_set_predicted,
        labels=labels,
        average=None)
    new_result['f_measure'].append(list(zip(labels, f_measure)))

    print(new_result)
    # print(classifier.show_most_informative_features(5))

new_result['AVG'] = {
    "accuracy": 0.0,
    "f_measure": {
        "ERROR": 0.0,
        "IMPERSONAL": 0.0,
        "SUBJECT": 0.0,
        "ZERO": 0.0
    },
    "precision": {
        "ERROR": 0.0,
        "IMPERSONAL": 0.0,
        "SUBJECT": 0.0,
        "ZERO": 0.0
    },
    "recall": {
        "ERROR": 0.0,
        "IMPERSONAL": 0.0,
        "SUBJECT": 0.0,
        "ZERO": 0.0
    }
}
for result in new_result['accuracy']:
    new_result["AVG"]["accuracy"] += result

for result in new_result['precision']:
    for (subj, val) in result:
        new_result["AVG"]["precision"][subj] += val

for result in new_result['recall']:
    for (subj, val) in result:
        new_result["AVG"]["recall"][subj] += val

for result in new_result['f_measure']:
    for (subj, val) in result:
        new_result["AVG"]["f_measure"][subj] += val

new_result["AVG"]["accuracy"] = new_result["AVG"]["accuracy"] / 5
for subj in ['SUBJECT', 'ZERO', 'IMPERSONAL', 'ERROR']:
    new_result["AVG"]["recall"][subj] = (
        new_result["AVG"]["recall"][subj] / 5)

    new_result["AVG"]["precision"][subj] = (
        new_result["AVG"]["precision"][subj] / 5)

    new_result["AVG"]["f_measure"][subj] = (
        new_result["AVG"]["f_measure"][subj] / 5)

print(new_result)

elapsed_time = time.clock() - start_time
print("Tiempo de ejecucion: {1}{0:.5f}{2} segundos".format(
                elapsed_time, bcolors.OKGREEN, bcolors.ENDC))
