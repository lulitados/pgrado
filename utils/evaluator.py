import sys
import numpy as np

from utils.decoder import decode_tag
from features.pos_feature import pos_feature
from features.se_feature import se_feature
from features.a_feature import a_feature
from features.nh_feature import nh_feature
from features.main_verb_feature import finit_verb_clause
from features.subject_feature import has_subject
from features.infs_feature import infs_feature
from features.verb_type import verb_type

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

global sp
global sid

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

# COMENTAR PARA SACAR EL PARSER
sen = freeling.senses(DATA + LANG + "/senses.dat")
parser = freeling.chart_parser(DATA + LANG + "/chunker/grammar-chunk.dat")
dep = freeling.dep_txala(
    DATA + LANG + "/dep_txala/dependences.dat", parser.get_start_symbol())


# Cargo los vectores
vecs = np.load("./embeddings/emb39-word2vec.npy")

# Obtenemos la lista de palabras
with open("./embeddings/emb39-word2vec.txt") as f:
    words = [w.strip() for w in f]


def get_word_embeddings(word):
    if word.lower() in words:
        return vecs[words.index(word.lower()), :]
    else:
        return vecs[words.index("unknown"), :]


def evaluate_clause(clause, verb_info):
    """
    This method returns the following features for a clause, in order.

    * PARSER
    * LEMMA
    * NUMBER
    * PERSON
    * INF
    * POS_PRE_0
    * POS_PRE_1
    * POS_PRE_2
    * POS_PRE_3
    * POS_POS_0
    * POS_POS_1
    * POS_POS_2
    * POS_POS_3
    * SE
    * A
    * NH_TOT
    * NH_PREV
    * NH_TOT_AGREE
    * NH_PREV_AGREE
    * MAIN_VERB_VECTOR
    * VERB_TYPE (x3)

    """

    # Cleanup splitter before evaluating a new clause
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

        found_subject = False
        pos_pre = ["", "", "", ""]
        pos_pos = ["", "", "", ""]
        has_se = False
        words = s.get_words()
        main_verb = finit_verb_clause(words, verb_info)
        has_a = a_feature(words)
        nhtot = 0
        nhprev = 0
        nhtot_agree = 0
        nhprev_agree = 0
        if main_verb:
            pos_pre = pos_feature(
                main_verb.get_position(), words, len(words), pre=True)
            pos_pos = pos_feature(
                main_verb.get_position(), words, len(words), pre=False)
            infs = infs_feature(words)
            decoded_tag = decode_tag(main_verb.get_tag())
            has_se = se_feature(
                words,
                main_verb.get_position(),
                len(words))

            main_verb_vector = get_word_embeddings(main_verb.get_form())

            # COMENTAR PARA SACAR EL PARSER
            found_subject, tag = has_subject(
                dp.get_node_by_pos(main_verb.get_position()).begin())
            nhtot = nh_feature(
                dp,
                main_verb.get_position(),
                pre=False)
            nhprev = nh_feature(
                dp,
                main_verb.get_position(),
                pre=True)

            nhtot_agree = nh_feature(
                dp,
                main_verb.get_position(),
                pre=False,
                main_verb_tag=main_verb.get_tag())
            nhprev_agree = nh_feature(
                dp,
                main_verb.get_position(),
                pre=True,
                main_verb_tag=main_verb.get_tag())

            return (found_subject, main_verb.get_lemma(), decoded_tag[5],
                    decoded_tag[4], infs,
                    pos_pre[0], pos_pre[1], pos_pre[2], pos_pre[3],
                    pos_pos[0], pos_pos[1], pos_pos[2], pos_pos[3],
                    has_se, has_a, nhtot, nhprev, nhtot_agree,
                    nhprev_agree) + verb_type(main_verb.get_lemma()) + tuple(main_verb_vector)
        else:
            return None
