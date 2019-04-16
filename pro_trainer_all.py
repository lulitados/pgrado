import time
import sys
import numpy as np
from sklearn.preprocessing import CategoricalEncoder
from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score, confusion_matrix

from sklearn.svm import SVC, LinearSVC

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.externals import joblib

from elliphant.elliphant import ElliphantCorpus
from ancora.ancora_corpus import AncoraCorpus
from corin.corin_corpus import CorinCorpus

start_time = time.clock()


def print_cm(cm, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    """pretty print for confusion matrixes"""
    columnwidth = max([len(x) for x in labels] + [5])  # 5 is value length
    empty_cell = " " * columnwidth
    # Print header
    print("    " + empty_cell, end=" ")
    for label in labels:
        print("%{0}s".format(columnwidth) % label, end=" ")
    print()
    # Print rows
    for i, label1 in enumerate(labels):
        print("    %{0}s".format(columnwidth) % label1, end=" ")
        for j in range(len(labels)):
            cell = "%{0}.1f".format(columnwidth) % cm[i, j]
            if hide_zeroes:
                cell = cell if float(cm[i, j]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if i != j else empty_cell
            if hide_threshold:
                cell = cell if cm[i, j] > hide_threshold else empty_cell
            print(cell, end=" ")
        print()


corpus_name = sys.argv[1] if len(sys.argv) > 1 else "ancora"
if corpus_name == "elliphant":
    clauses = ElliphantCorpus()
else:
    clauses = AncoraCorpus()

classifier_data = {}

print("Trabajando con el corpus de " + corpus_name)

training_values_file = np.memmap(
    corpus_name + '_training_values.memmap',
    dtype='U50',
    mode='r')

training_data_file = np.memmap(
    corpus_name + '_training_data.memmap',
    dtype='U50',
    mode='r',
    shape=(training_values_file.shape[0], 322))

enc = CategoricalEncoder(handle_unknown='ignore')
enc.fit(training_data_file[:, :22])

training_CE = enc.transform(training_data_file[:, :22]).toarray()

training_full_data = np.memmap(
    corpus_name + '_training_full_data.memmap',
    dtype='float32',
    mode='r',
    shape=(training_CE.shape[0], training_CE.shape[1] + 300))


# corpus_name = 'corin'
testing_values_file = np.memmap(
    corpus_name + '_testing_values.memmap',
    dtype='U50',
    mode='r')

testing_data_file = np.memmap(
    corpus_name + '_testing_data.memmap',
    dtype='U50',
    mode='r',
    shape=(testing_values_file.shape[0], 322))

testing_CE = enc.transform(testing_data_file[:, :22]).toarray()

testing_full_data = np.memmap(
    corpus_name + '_testing_full_data.memmap',
    dtype='float32',
    mode='r',
    shape=(testing_CE.shape[0], testing_CE.shape[1] + 300))

print("Empiezo a clasificar!")


def train_test_classifier(clf_label, classifier):
    # XXX: Para generar los clasificadores a giardar
    # classifier.fit(training_full_data, training_values_file)
    # joblib.dump(classifier, '{}.pkl'.format(clf_label))
    #

    # XXX: Para usar el clasificador guardado.
    # Cuando este creado, eliminar el parametro classifier de la funcion
    # classifier = joblib.load('{}.pkl'.format(clf_label))

    testing_set_predicted = classifier.predict(testing_full_data)

    classifier_data[clf_label] = {}

    labels = ['SUBJECT', 'ZERO', 'IMPERSONAL', 'ERROR']
    accuracy = accuracy_score(
        testing_values_file,
        testing_set_predicted)
    classifier_data[clf_label]['accuracy'] = accuracy

    precision = precision_score(
        testing_values_file,
        testing_set_predicted,
        labels=labels,
        average=None)
    classifier_data[clf_label]['precision'] = dict(zip(labels, precision))

    recall = recall_score(
        testing_values_file,
        testing_set_predicted,
        labels=labels,
        average=None)
    classifier_data[clf_label]['recall'] = dict(zip(labels, recall))

    f_measure = f1_score(
        testing_values_file,
        testing_set_predicted,
        labels=labels,
        average=None)
    classifier_data[clf_label]['f_measure'] = dict(zip(labels, f_measure))

    c_matrix = confusion_matrix(
        testing_values_file,
        testing_set_predicted,
        labels=labels)
    classifier_data[clf_label]['c_matrix'] = c_matrix

    print_cm(c_matrix, labels)


voting_classifier = VotingClassifier(
    estimators=[
        ('LogisticRegression', LogisticRegression(random_state=1)),
        ('SGDClassifier', SGDClassifier()),
        # ('GaussianNB', GaussianNB()),
        # ('BernoulliNB', BernoulliNB()),
        ('SVC', SVC()),
        ('LinearSVC', LinearSVC()),
        ('RandomForestClassifier', RandomForestClassifier(random_state=1))
    ],
    voting='hard'
)

classifier_list = [
    ('LogisticRegression', LogisticRegression(random_state=1)),
    ('SGDClassifier', SGDClassifier()),
    # ('GaussianNB', GaussianNB()),
    # ('MultinomialNB', MultinomialNB()),
    # ('BernoulliNB', BernoulliNB()),
    ('SVC', SVC()),
    ('LinearSVC', LinearSVC()),
    ('RandomForestClassifier', RandomForestClassifier(random_state=1)),
    ('VotingClassifier', voting_classifier)
]

for clf in classifier_list:
    # XXX: Usar este cuando se quieran guardar los clasificadores
    train_test_classifier(*clf)
    # XXX: Usar este para cuando se usen los guardados
    # train_test_classifier(clf[0])
    print(classifier_data)


elapsed_time = time.clock() - start_time
classifier_data['exec_time'] = elapsed_time

print(classifier_data)
