import time

import nltk
import numpy as np
from sklearn import cross_validation
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.metrics import recall_score, precision_score, f1_score
from sklearn.ensemble import VotingClassifier

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.ensemble import RandomForestClassifier

# from elliphant.elliphant import ElliphantCorpus
from ancora.ancora_corpus import AncoraCorpus

from utils import evaluator
from utils.vectorize import create_vector

start_time = time.clock()

# clauses = ElliphantCorpus()
clauses = AncoraCorpus()
dt = np.dtype('object,object')
clauses_list = np.array(list(clauses), dtype=dt)

# http://stackoverflow.com/questions/24147278/how-do-i-create-test-and-train-samples-from-one-dataframe-with-pandas
np.random.seed(42)
msk = np.random.rand(clauses.total_clauses) < 0.8
training_clauses = clauses_list[msk]
testing_clauses = clauses_list[~msk]


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



def eval_features(clause):
    if not clause:
        return {}
    features_values = evaluator.evaluate_clause(clause)
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
        'NH_PREV_AGREE'
    ]
    if not features_values:
        return {}
    return dict(zip(feature_names, list(features_values)))


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
        create_vector(eval_features(clause), subject) for (clause, subject) in cv_training]
    testing_set = [
        create_vector(eval_features(clause), subject) for (clause, subject) in cv_testing]

    # training_set = [
    #     (eval_features(clause), subject) for (clause, subject) in cv_training]
    # testing_set = [
    #     (eval_features(clause), subject) for (clause, subject) in cv_testing]

    # maxent_classifier = nltk.MaxentClassifier.train(training_set)
    # bayes_classifier = nltk.classify.NaiveBayesClassifier.train(training_set)
    # svc_classifier = nltk.classify.SklearnClassifier(
    #     SVC(), sparse=False).train(training_set)

    linear_clf_1 = LogisticRegression(random_state=1)
    linear_clf_2 = SGDClassifier()

    nb_clf_1 = GaussianNB()
    nb_clf_2 = MultinomialNB()
    nb_clf_3 = BernoulliNB()

    svm_clf_1 = SVC()
    svm_clf_2 = LinearSVC()
    # svm_clf_3 = NuSVC()

    ensemble_clf_1 = RandomForestClassifier(random_state=1)

    skl_voting_classifier = VotingClassifier(
        estimators=[
            ('linear_clf_1', linear_clf_1),
            ('linear_clf_2', linear_clf_2),
            ('nb_clf_1', nb_clf_1),
            ('nb_clf_2', nb_clf_2),
            ('nb_clf_3', nb_clf_3),
            ('svm_clf_1', svm_clf_1),
            ('svm_clf_2', svm_clf_2),
            # ('svm_clf_3', svm_clf_3),
            ('ensemble_clf_1', ensemble_clf_1)
        ],
        voting='hard'
    )
    voting_classifier = nltk.classify.SklearnClassifier(
        skl_voting_classifier, sparse=False).train(training_set)

    new_result['accuracy'].append(
        nltk.classify.util.accuracy(voting_classifier, testing_set))

    testing_set_features, testing_set_values = zip(*testing_set)
    testing_set_predicted = voting_classifier.classify_many(testing_set_features)

    labels = ['SUBJECT', 'ZERO', 'IMPERSONAL', 'ERROR']
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
