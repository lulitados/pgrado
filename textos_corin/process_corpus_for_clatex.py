import json
import re
import sys
import os

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

tg=freeling.hmm_tagger( DATA + LANG + "/tagger.dat", False, 2)
sen=freeling.senses(DATA + LANG + "/senses.dat")
parser= freeling.chart_parser(DATA + LANG + "/chunker/grammar-chunk.dat")
dep=freeling.dep_txala(
    DATA + LANG + "/dep_txala/dependences.dat", parser.get_start_symbol())


location = os.getcwd()  # get present working directory location here
corin_sources_location = location + '/corin_sources'

for file in os.listdir(corin_sources_location):
    current = os.path.join(corin_sources_location, file)
    if os.path.isfile(current):
        output_file = 'corin_for_clatex/' + file.split('.')[0] + '.txt'
        with open(current, 'r') as data_file:
            # Open output file
            with open(output_file, 'w+') as o_file:
                for line in data_file:
                    if line.startswith('*') or line.rstrip() == '':
                        # Skip lines with metadata and empty lines
                        continue
                    if not line.endswith("."):
                        l = tk.tokenize(line + ".")
                    else:
                        l = tk.tokenize(line)

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

sp.close_session(sid);
