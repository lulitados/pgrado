import json
import re
import sys
import xml.etree.ElementTree

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


relative_pronoun = "PR0"
improper_conjunction = "CS"
proper_conjunction = "CC"
puntation = "F"


def is_finit_verb(tag):
    return (
        tag[0] == "V" and
        not tag[3] == "0" and
        not tag[4] == "0" and
        not tag[5] == "0"
    )


def is_relative_pronoun(tag):
    return tag.startswith(relative_pronoun)


def is_improper_conjunction(tag):
    return tag.startswith(improper_conjunction)


def is_proper_conjunction(tag):
    return tag.startswith(proper_conjunction)


def is_puntation(tag):
    return tag.startswith(puntation)


def is_boundry(tag, verb_is_boundry):
    stop = is_relative_pronoun(tag) or \
        is_improper_conjunction(tag) or \
        is_proper_conjunction(tag) or \
        is_puntation(tag)
    if stop:
        return True
    else:
        if verb_is_boundry:
            return is_finit_verb(tag)
    return False


def clause_feature(sentence):
    if not sentence.endswith("."):
        sentence += "."
    line = tk.tokenize(sentence)
    ls = sp.split(sid, line, False)

    ls = mf.analyze(ls)
    ls = tg.analyze(ls)

    clauses = []
    # output results
    for s in ls:
        ws = s.get_words()

        clause = []
        has_finite_verb = False
        finit_verb_pos = -1
        verb_form = ''
        for word in ws:
            stop = is_boundry(word.get_tag(), has_finite_verb)
            if stop:
                if has_finite_verb:
                    clauses.append(
                        [" ".join(clause), finit_verb_pos, verb_form])
                clause = []
                if not is_puntation(word.get_tag()):
                    clause.append(word.get_form())
                has_finite_verb = False
            else:
                if not has_finite_verb:
                    has_finite_verb = is_finit_verb(word.get_tag())
                    if has_finite_verb:
                        finit_verb_pos = word.get_position()
                        verb_form = word.get_form()
                clause.append(word.get_form())
    return clauses


def process_sentence(corpus_sentence):
    result = " ".join(
        [child.find('text').text for child in corpus_sentence.getchildren()])
    return re.sub(r' (\W)', r'\1', result)


def is_token_finit_verb(token, verb_form):
    subject = token.find('.//tags/subject')
    return token.find('text').text == verb_form and subject is not None


def subject_eval(subject):
    if subject in ['IMPERSONAL', 'IMPERSONAL_SE']:
        return 'IMPERSONAL'
    elif subject in ['SUBJECT', 'SUBJECT_A', 'SUBJECT_NN', 'SUBJECT_NN_PR',
                     'SUBJECT_P', 'SUBJECT_PR']:
        return 'SUBJECT'
    elif subject in ['ZERO', 'ZERO_HEAD', 'ZERO_HEAD_PR', 'ZERO_NN',
                     'ZERO_NN_P', 'ZERO_NN_PR', 'ZERO_P', 'ZERO_PR']:
        return 'ZERO'
    else:
        return 'ERROR'


def get_subject_token(token):
    subject = token.find('.//tags/subject')
    if subject is not None:
        return subject_eval(subject.text)
    return ''


def get_subject_verb(verb_pos, verb_form, corpus_sentence):
    verb_pos -= 5
    if verb_pos < 0:
        verb_pos = 0
    tokens = corpus_sentence.getchildren()[verb_pos:]
    candidates = [
        t for t in tokens
        if is_token_finit_verb(t, verb_form)
    ]
    if len(candidates) > 0:
        return get_subject_token(candidates[0])
    return ''


def get_clauses_source(source):
    parser = xml.etree.ElementTree.XMLParser(encoding='utf-8')
    doc = xml.etree.ElementTree.parse(source, parser).getroot()
    source_clauses = []
    for corpus_sentence in doc.findall('sentence'):
        processed_sentence = process_sentence(corpus_sentence)
        clauses = clause_feature(processed_sentence)
        for c in clauses:
            clause_subj = get_subject_verb(c[1], c[2], corpus_sentence)
            if clause_subj != '':
                # yield (c[0], clause_subj)
                source_clauses.append({
                    'clause': c[0],
                    'subject': clause_subj
                })
    return source_clauses


# input_file = sys.argv[1]
# input_clauses = get_clauses_source(input_file)

# print(json.dumps(input_clauses))
