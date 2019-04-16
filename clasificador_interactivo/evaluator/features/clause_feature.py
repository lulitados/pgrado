import sys

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
tg = freeling.hmm_tagger(DATA + LANG + "/tagger.dat", True, 2)


relative_pronoun = "PR0"
improper_conjunction = "CS"
proper_conjunction = "CC"
puntation = "F"


def is_finit_verb(tag):
    return (
        tag[0] is "V" and
        not tag[3] is "0" and
        not tag[4] is "0" and
        not tag[5] is "0"
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
        for w in ws:
            stop = is_boundry(w.get_tag(), has_finite_verb)
            if stop:
                if has_finite_verb:
                    clauses.append(" ".join(clause))
                clause = []
                if not is_puntation(w.get_tag()):
                    clause.append(w.get_form())
                has_finite_verb = False
            else:
                if not has_finite_verb:
                    has_finite_verb = is_finit_verb(w.get_tag())
                clause.append(w.get_form())
    return clauses


# clauses = clause_feature("Aprobada por las Cortes Generales el 31 de octubre de 1978, fue refrendada por el pueblo español el 6 de diciembre; sancionada y promulgada por el Rey el día 27 y publicada el 29 de diciembre de 1978, día que entró en vigor.")

# for c in clauses:
#     print(c)

# clean up
sp.close_session(sid)
