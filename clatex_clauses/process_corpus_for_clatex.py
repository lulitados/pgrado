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
# tg=freeling.hmm_tagger( DATA + LANG + "/tagger.dat", True, 2)
# Changes tagger options as per
# https://talp-upc.gitbooks.io/freeling-user-manual/content/modules/tagger.html
# to avoid the tagged word to be split in several ones.
tg=freeling.hmm_tagger( DATA + LANG + "/tagger.dat", False, 2)
sen=freeling.senses(DATA + LANG + "/senses.dat")
parser= freeling.chart_parser(DATA + LANG + "/chunker/grammar-chunk.dat")
dep=freeling.dep_txala(
    DATA + LANG + "/dep_txala/dependences.dat", parser.get_start_symbol())


def process_sentence(corpus_sentence):
    result = " ".join(
        [child.find('text').text for child in corpus_sentence.getchildren()])
    return re.sub(r' (\W)', r'\1', result)


def process_source(source, output_file):
    xml_parser = xml.etree.ElementTree.XMLParser(encoding='utf-8')
    doc = xml.etree.ElementTree.parse(source, xml_parser).getroot()
    sentences = []
    # Open output file
    with open(output_file, 'w+') as o_file:
        for corpus_sentence in doc.findall('sentence'):
            processed_sentence = process_sentence(corpus_sentence)
            if not processed_sentence.endswith("."):
                processed_sentence += "."
            l = tk.tokenize(processed_sentence)
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
        o_file.close()


input_file = sys.argv[1]
output_file = sys.argv[2]

process_source(input_file, output_file)

sp.close_session(sid);
