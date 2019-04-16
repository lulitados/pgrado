import time
import json

import numpy as np
from sklearn import cross_validation
from sklearn.preprocessing import CategoricalEncoder
from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score, confusion_matrix

from sklearn.svm import SVC, LinearSVC

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier

# from elliphant.elliphant import ElliphantCorpus
from ancora.ancora_corpus import AncoraCorpus


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
dt = np.dtype('object,object,object')
clauses_list = np.array(list(clauses), dtype=dt)

# http://stackoverflow.com/questions/24147278/how-do-i-create-test-and-train-samples-from-one-dataframe-with-pandas
np.random.seed(42)
msk = np.random.rand(clauses.total_clauses) < 0.8
training_clauses = clauses_list[msk]
testing_clauses = clauses_list[~msk]

classifier_data = {}


training_values_file = np.memmap(
    'ancora_training_values.memmap',
    dtype='U50',
    mode='r')

testing_values_file = np.memmap(
    'ancora_testing_values.memmap',
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

training_full_data = np.memmap(
    'ancora_training_full_data.memmap',
    dtype='float32',
    mode='r',
    shape=(training_CE.shape[0], training_CE.shape[1] + 300))
testing_data_file = np.memmap(
    'ancora_testing_data.memmap',
    dtype='U50',
    mode='r',
    shape=(testing_values_file.shape[0], 322))

testing_CE = enc.transform(testing_data_file[:, :22]).toarray()

testing_full_data = np.memmap(
    'ancora_testing_full_data.memmap',
    dtype='float32',
    # mode='w+',
    mode='r',
    shape=(testing_CE.shape[0], testing_CE.shape[1] + 300))


with open('classification_errors/testing_clauses.json') as f:
    testing_eval_clauses = json.load(f)


def train_test_classifier(clf_label, classifier):
    classifier.fit(training_full_data, training_values_file)

    # testing_full_data = np.concatenate(
    #     (testing_CE, testing_data), axis=1)
    testing_set_predicted = classifier.predict(testing_full_data)

    classifier_data[clf_label] = {}

    labels = ['SUBJECT', 'ZERO', 'IMPERSONAL', 'ERROR']

    imp_as_subj_list = []
    zero_as_subj_list = []
    imp_as_imp_list = []
    zero_as_zero_list = []
    for idx, (real, predicted) in enumerate(zip(
            testing_values_file, testing_set_predicted)):
        if real != predicted:
            if real == 'IMPERSONAL' and predicted == 'SUBJECT':
                imp_as_subj_list.append(
                    (testing_data_file[idx, :22].tolist(), testing_eval_clauses[idx]))
            if real == 'ZERO' and predicted == 'SUBJECT':
                zero_as_subj_list.append(
                    (testing_data_file[idx, :22].tolist(), testing_eval_clauses[idx]))
        else:
            if real == 'IMPERSONAL':
                imp_as_imp_list.append(
                    (testing_data_file[idx, :22].tolist(), testing_eval_clauses[idx]))
            elif real == 'ZERO':
                zero_as_zero_list.append(
                    (testing_data_file[idx, :22].tolist(), testing_eval_clauses[idx]))

    with open('{}_imp_as_subj_3.json'.format(clf_label), 'w') as imp_as_subj:
        json.dump(imp_as_subj_list, imp_as_subj, ensure_ascii=False)
    with open('{}_zero_as_subj_3.json'.format(clf_label), 'w') as zero_as_subj:
        json.dump(zero_as_subj_list, zero_as_subj, ensure_ascii=False)
    with open('{}_imp_as_imp_3.json'.format(clf_label), 'w') as imp_as_imp:
        json.dump(imp_as_imp_list, imp_as_imp, ensure_ascii=False)
    with open('{}_zero_as_zero_3.json'.format(clf_label), 'w') as zero_as_zero:
        json.dump(zero_as_zero_list, zero_as_zero, ensure_ascii=False)


# voting_classifier = VotingClassifier(
#     estimators=[
#         ('LogisticRegression', LogisticRegression(random_state=1)),
#         ('SGDClassifier', SGDClassifier()),
#         ('GaussianNB', GaussianNB()),
#         ('BernoulliNB', BernoulliNB()),
#         ('SVC', SVC()),
#         ('LinearSVC', LinearSVC()),
#         ('RandomForestClassifier', RandomForestClassifier(random_state=1))
#     ],
#     voting='hard'
# )

classifier_list = [
    ('LogisticRegression', LogisticRegression(random_state=1)),
    # ('SGDClassifier', SGDClassifier()),
    # ('GaussianNB', GaussianNB()),
    # # ('MultinomialNB', MultinomialNB()),
    # ('BernoulliNB', BernoulliNB()),
    # ('SVC', SVC()),
    ('LinearSVC', LinearSVC()),
    # ('RandomForestClassifier', RandomForestClassifier(random_state=1)),
    # ('VotingClassifier', voting_classifier)
]

for clf in classifier_list:
    train_test_classifier(*clf)
    print("\n")
    print(clf[0])
    print(classifier_data)
    print("\n")


elapsed_time = time.clock() - start_time
# print("Tiempo de ejecucion: {1}{0:.5f}{2} segundos".format(
#                 elapsed_time, bcolors.OKGREEN, bcolors.ENDC))
classifier_data['exec_time'] = elapsed_time

print(classifier_data)
