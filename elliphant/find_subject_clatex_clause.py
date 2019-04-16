import json
import sys
import collections

import xml.etree.ElementTree

from main_verb_feature import finit_verb_clause
from elliphant_clauses import get_subject_verb

sys.path.append('/home/veronica/git/FreeLing/APIs/python')
# sys.path.append('/Users/lucia/fing/proyecto/FreeLing/APIs/python')
import freeling


"""
Freeling settings
"""
FREELINGDIR = "/usr/local"

DATA = FREELINGDIR + "/share/freeling/"
LANG = "es"

freeling.util_init_locale("default")

# create language analyzer
la = freeling.lang_ident(DATA + "common/lang_ident/ident.dat")

# create options set for maco analyzer.
# Default values are Ok, except for data files.
op = freeling.maco_options("es")
op.set_data_files("",
                  DATA + "common/punct.dat",
                  DATA + LANG + "/dicc.src",
                  DATA + LANG + "/afixos.dat",
                  "",
                  DATA + LANG + "/locucions.dat",
                  DATA + LANG + "/np.dat",
                  DATA + LANG + "/quantities.dat",
                  DATA + LANG + "/probabilitats.dat")

# create analyzers
tk = freeling.tokenizer(DATA + LANG + "/tokenizer.dat")
sp = freeling.splitter(DATA + LANG + "/splitter.dat")
sid = sp.open_session()
mf = freeling.maco(op)

# activate mmorpho odules to be used in next call
mf.set_active_options(
    False,  # umap
    True,   # num
    True,   # pun
    True,  # dat
    True,   # dic
    True,   # aff
    False,   # comp
    True,  # rtk
    True,  # mw
    True,  # ner
    True,   # qt
    True    # prb
)

# create tagger, sense anotator, and parsers
tg = freeling.hmm_tagger(DATA + LANG + "/tagger.dat", True, 2)


ELLIPHANT_SOURCES = [
    'elliphant_raw/elliphant_eszic_es_health_1.xml',
    'elliphant_raw/elliphant_eszic_es_health_2.xml',
    'elliphant_raw/elliphant_eszic_es_health_3.xml',
    'elliphant_raw/elliphant_eszic_es_health_4.xml',
    'elliphant_raw/elliphant_eszic_es_health_5.xml',
    'elliphant_raw/elliphant_eszic_es_health_6.xml',
    'elliphant_raw/elliphant_eszic_es_health_7.xml',
    'elliphant_raw/elliphant_eszic_es_health_8.xml',
    'elliphant_raw/elliphant_eszic_es_health_9.xml',
    'elliphant_raw/elliphant_eszic_es_legal_1.xml',
    'elliphant_raw/elliphant_eszic_es_legal_2.xml',
    'elliphant_raw/elliphant_eszic_es_legal_3.xml',
    'elliphant_raw/elliphant_eszic_es_legal_4.xml',
    'elliphant_raw/elliphant_eszic_es_legal_5.xml',
    'elliphant_raw/elliphant_eszic_es_legal_6.xml',
    'elliphant_raw/elliphant_eszic_es_legal_7.xml',
    'elliphant_raw/elliphant_eszic_es_legal_8.xml'
]

SOURCES = [
    'new_extracted_clauses/elliphant_eszic_es_health_1_result.json',
    'new_extracted_clauses/elliphant_eszic_es_health_2_result.json',
    'new_extracted_clauses/elliphant_eszic_es_health_3_result.json',
    'new_extracted_clauses/elliphant_eszic_es_health_4_result.json',
    'new_extracted_clauses/elliphant_eszic_es_health_5_result.json',
    'new_extracted_clauses/elliphant_eszic_es_health_6_result.json',
    'new_extracted_clauses/elliphant_eszic_es_health_7_result.json',
    'new_extracted_clauses/elliphant_eszic_es_health_8_result.json',
    'new_extracted_clauses/elliphant_eszic_es_health_9_result.json',
    'new_extracted_clauses/elliphant_eszic_es_legal_1_result.json',
    'new_extracted_clauses/elliphant_eszic_es_legal_2_result.json',
    'new_extracted_clauses/elliphant_eszic_es_legal_3_result.json',
    'new_extracted_clauses/elliphant_eszic_es_legal_4_result.json',
    'new_extracted_clauses/elliphant_eszic_es_legal_5_result.json',
    'new_extracted_clauses/elliphant_eszic_es_legal_6_result.json',
    'new_extracted_clauses/elliphant_eszic_es_legal_7_result.json',
    'new_extracted_clauses/elliphant_eszic_es_legal_8_result.json'
]

DESTINATIONS = [
    'new_extracted_clauses_dict/elliphant_eszic_es_health_1_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_health_2_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_health_3_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_health_4_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_health_5_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_health_6_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_health_7_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_health_8_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_health_9_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_legal_1_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_legal_2_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_legal_3_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_legal_4_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_legal_5_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_legal_6_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_legal_7_clauses.json',
    'new_extracted_clauses_dict/elliphant_eszic_es_legal_8_clauses.json'
]
#


class OrderedSet(collections.Set):

    def __init__(self, iterable=()):
        self.d = collections.OrderedDict.fromkeys(iterable)

    def __len__(self):
        return len(self.d)

    def __contains__(self, element):
        return element in self.d

    def __iter__(self):
        return iter(self.d)


def clause_is_contained(clause_tokens, sentence_tokens):
    """Both must be OrderedSet instances"""
    clause_tokens_set = OrderedSet(clause_tokens)
    sentence_tokens_set = OrderedSet(sentence_tokens)
    clause_diff = list(clause_tokens_set - sentence_tokens_set)
    # If the difference of tokens in the clause that are not in the sentence
    # is less than a quarter of the clause's total tokens, we assume that the
    # clause belongs to the sentence.
    # This was done out of convenience, and appears to work well. OrderedSet is
    # not needed in this implementation.
    # print("Source: {}".format(clause_tokens))
    # print("Elliphant: {}".format(sentence_tokens))
    # print(len(clause_diff) <= round(len(clause_tokens) / 4))
    # print('--------------------------------------')
    return len(clause_diff) <= round(len(clause_tokens) / 4)


def get_words(sentence):
    if not sentence.endswith("."):
        sentence += "."
    line = tk.tokenize(sentence)
    ls = sp.split(sid, line, False)

    ls = mf.analyze(ls)
    ls = tg.analyze(ls)

    ws = None
    for s in ls:
        ws = s.get_words()

    return ws


def add_subject_to_clause(source, dest, elliphant_source):
    print('Starting: {}'.format(source))
    parser = xml.etree.ElementTree.XMLParser(encoding='utf-8')
    doc = xml.etree.ElementTree.parse(elliphant_source, parser).getroot()
    elliphant_sentences = iter(doc.findall('sentence'))

    clauses_dict = []

    elliphant_sentence = next(elliphant_sentences)
    elliphant_tokens = [
        t.find('text').text for t in elliphant_sentence.findall('token')]
    with open(source, 'r') as in_file:
        clauses = json.load(in_file)
        clauses.reverse()
        for clause_info in clauses:
            clause = clause_info[0]
            print('-----------------------------')
            # For each clause extracted with Clatex, we try to find the
            # sentence of the corpus it came from. For that check if the clause
            # belongs to the current sentence of the corpus checking the tokens
            # in both (more info in method description).
            clause_tokens = [t for t in clause.split(' ') if t != '']
            while not clause_is_contained(
                    clause_tokens, elliphant_tokens):
                # If the currente sentece does not contain the clause, the we
                # advance and check again, until we either find the source, or
                # have no more sentences in the corpus.
                # This sometimes causes problemas, as some sentences get mixed
                # after processing. Some had to be manually adjusted.
                elliphant_sentence = next(elliphant_sentences, None)
                if elliphant_sentence is None:
                    print('No more clauses: {}'.format(clause))
                    break
                elliphant_tokens = [
                    t.find('text').text for t in
                        elliphant_sentence.findall('token')]
            else:
                # If we found the source sentence for the clause, we find the
                # clause's verb's subject.
                ws = get_words(clause)
                if elliphant_sentence is None or ws is None:
                    print(("No clause or no words:\nSentence: {}"
                                  "\nWS: {}").format(elliphant_sentence, ws))
                    continue
                finit_verb = finit_verb_clause(ws, clause_info[1])
                if finit_verb is None or finit_verb == '':
                    print(('No finit verb:\n'
                                  'Clause: {}\n'
                                  'WS: {}\n'
                                  'INFO: {}').format(
                                    clause,
                                    ' '.join([w.get_form() for w in ws]),
                                    clause_info[1]))
                    continue
                verb_form = finit_verb.get_form()
                try:
                    finit_verb_pos = elliphant_tokens.index(verb_form)
                except ValueError:
                    print(('No finit verb pos:\n'
                                  'Clause: {}\n'
                                  'WS: {}\n'
                                  'INFO: {}').format(
                                    clause,
                                    ' '.join([w.get_form() for w in ws]),
                                    clause_info[1]))
                    continue
                clause_subj = get_subject_verb(
                    finit_verb_pos, verb_form, elliphant_sentence)
                if clause_subj != '':
                    new_clause = {
                        'clause': clause,
                        'subject': clause_subj,
                        'verb': {
                            'lemma': clause_info[1]['lemma'],
                            'form': clause_info[1]['form'],
                            'tag': clause_info[1]['tag']
                        }
                    }
                    clauses_dict.append(new_clause)
        in_file.close()
    # with open(dest, 'w+') as dest_file:
    #     dest_file.write(json.dumps(clauses_dict, indent=4))
    #     dest_file.close()


for source, dest, elliphant_source in zip(
        SOURCES, DESTINATIONS, ELLIPHANT_SOURCES):
    add_subject_to_clause(source, dest, elliphant_source)
