
import json
import re
import sys, os
from subprocess import call, STDOUT


sys.path.append(os.environ['FREELING_API'])
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
# tg=freeling.hmm_tagger( DATA + LANG + "/tagger.dat", True, 2)
# Changes tagger options as per
# https://talp-upc.gitbooks.io/freeling-user-manual/content/modules/tagger.html
# to avoid the tagged word to be split in several ones.
tg=freeling.hmm_tagger( DATA + LANG + "/tagger.dat", False, 2)
sen=freeling.senses(DATA + LANG + "/senses.dat")
parser= freeling.chart_parser(DATA + LANG + "/chunker/grammar-chunk.dat")
dep=freeling.dep_txala(
    DATA + LANG + "/dep_txala/dependences.dat", parser.get_start_symbol())



'''
Metodos para encontrar el verbo principal de cada clausula
'''
def _is_finit_verb(tag):
    return (
        tag[0] == "V" and
        not tag[3] == "0" and
        not tag[4] == "0" and
        not tag[5] == "0"
    )


def _finit_verb_clause(words):
    for word in words:
        if _is_finit_verb(word.get_tag()):
            return word
    return ""


def _find_main_verb_position(clause):
    global sp
    global sid
    sp.close_session(sid)
    sid = sp.open_session()

    if not clause.endswith("."):
        clause += "."
    line = tk.tokenize(clause.replace("\"", ""))
    ls = sp.split(sid, line, False)

    ls = mf.analyze(ls)
    ls = tg.analyze(ls)
    # COMENTAR PARA SACAR EL PARSER
    ls = sen.analyze(ls)
    ls = parser.analyze(ls)
    ls = dep.analyze(ls)

    # output results
    for s in ls:
        # COMENTAR PARA SACAR EL PARSER
        dp = s.get_dep_tree()

        words = s.get_words()
        main_verb = _finit_verb_clause(words)
        if main_verb:
            return main_verb, main_verb.get_position()
        else:
            return None, -1
    return None, -1

# ************************************************************************


'''
Metodos para procesar la salida de Clatex y obtener las clausulas.
'''

CLAUSES_REGEXP = re.compile(
    r'\w*\[(\w*) (\w*)/(?P<clause>.*)/\1 \2]', flags=re.DOTALL)
SENTENCE_END_REGEXP = re.compile(r'/enonce en\d]\s*$', flags=re.DOTALL)

TAG_OPEN = re.compile(r'\[\w* \w*/', flags=re.DOTALL)
TAG_CLOSE = re.compile(r'/\w+ \w+\]', flags=re.DOTALL)

TAG_CONTENT_TO_DELETE = re.compile(r'\[\w* \w*/(?P<para_eliminar>.*)/\w+ \w+\]', flags=re.DOTALL)


def _remove_clatex_tags(clause):
    new_clause = TAG_OPEN.sub('', clause)
    new_clause = TAG_CLOSE.sub('', new_clause)
    return new_clause


def _get_verb_object(verb):
    return {
        'form': verb.get_form(),
        'lemma': verb.get_lemma(),
        'tag': verb.get_tag(),
    }


def _get_clauses(sentence):
    # Always add the full sentence as a clause
    clauses = []
    matches = CLAUSES_REGEXP.finditer(sentence)
    main_verb, main_verb_position = _find_main_verb_position(_remove_clatex_tags(sentence))
    if main_verb is not None:
        clauses += [(_remove_clatex_tags(sentence), _get_verb_object(main_verb))]

    for match in matches:
        new_clause = TAG_CONTENT_TO_DELETE.sub('', match.string)
        # Si new_clause tiene verbo, entonces
        main_verb, main_verb_position = _find_main_verb_position(new_clause)
        if main_verb is not None:
            clauses += [(_remove_clatex_tags(match.string), _get_verb_object(main_verb))]

        clauses += _get_clauses(match.group('clause'))
    return clauses


def _same_verb(original, verb):
    return original['form'] == verb['form'] \
        and original['lemma'] == verb['lemma'] \
        and original['tag'] == verb['tag']


def _already_seen_for_verb(clause, verb, clauses_list):
    same_verb_clauses = [c for c, v in clauses_list if _same_verb(verb, v)]
    for c in same_verb_clauses:
        if c in clause:
            return True
    return False


def _cleanup_duplicates(clauses):
    seen_clauses = []
    seen_clauses_with_verb = []
    cleaned_clauses = []
    clauses.reverse()
    for clause, verb in clauses:
        # Simplify clause by removing all spaces and
        # the end period (if present)
        simplified_clause = clause.replace(' ', '')
        if simplified_clause.endswith('.'):
            simplified_clause = simplified_clause[:-1]
        if simplified_clause in seen_clauses:
            continue
        elif _already_seen_for_verb(simplified_clause, verb, seen_clauses_with_verb):
            continue
        else:
            if clause.endswith('.'):
                cleaned_clauses.append((clause[:-1], verb))
            else:
                cleaned_clauses.append((clause, verb))
            seen_clauses_with_verb.append((simplified_clause, verb))
            seen_clauses.append(simplified_clause)
    return cleaned_clauses


def _extract_caluses():
    clauses = []
    with open('clatex_output.tmp', 'r') as in_file:
        sentence = ''
        for line in in_file:
            sentence += line.replace('\n', '')
            if SENTENCE_END_REGEXP.search(sentence) is not None:
                clauses += _get_clauses(sentence)
                sentence = ''

    return _cleanup_duplicates(clauses)


def _get_clatex_clauses():
    FNULL = open(os.devnull, 'w')
    call([
        'swipl',
        '-s',
        '../../clatex2015/controlEn.pl',
        '-g',
        "proceso('{}','{}'),halt".format(
            'clatex_source.tmp',
            'clatex_output.tmp')
    ], stdout=FNULL, stderr=STDOUT)
    with open('clatex_output.tmp', 'r') as f:
            data = f.read().splitlines(True)
    with open('clatex_output.tmp', 'w') as f:
        f.writelines(data[3:])


def _process_text_for_clatex(text):
    with open('clatex_source.tmp', 'w') as o_file:
        if not text.endswith("."):
            text += "."
        l = tk.tokenize(text)
        ls = sp.split(sid, l, False);

        ls = mf.analyze(ls)
        ls = tg.analyze(ls)
        ls = sen.analyze(ls)
        ls = parser.analyze(ls)
        ls = dep.analyze(ls)
        for s in ls:
            ws = s.get_words();
            for w in ws :
                o_file.write("{word} {lemma} {tag} {prob}\n".format(
                    word=w.get_form(),
                    lemma=w.get_lemma(),
                    tag=w.get_tag(),
                    prob=str(w.get_analysis()[0].get_prob())
                ))

def get_clauses(text):
    _process_text_for_clatex(text)
    _get_clatex_clauses()

    return _extract_caluses()
