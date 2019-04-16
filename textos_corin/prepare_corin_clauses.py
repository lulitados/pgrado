import os
import sys
import json

from lxml import etree

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
tg = freeling.hmm_tagger(DATA + LANG + "/tagger.dat", False, 2)

# COMENTAR PARA SACAR EL PARSER
sen = freeling.senses(DATA + LANG + "/senses.dat")
parser = freeling.chart_parser(DATA + LANG + "/chunker/grammar-chunk.dat")
dep = freeling.dep_txala(
    DATA + LANG + "/dep_txala/dependences.dat", parser.get_start_symbol())


def finit_verb_clause(words, verb_info):
    for word in words:
        if (word.get_tag() == verb_info['tag'] and
                word.get_form() == verb_info['form'] and
                word.get_lemma() == verb_info['lemma']):
            return word
    return ""


def find_main_verb_position(clause, verb_info):
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
        main_verb = finit_verb_clause(words, verb_info)
        if main_verb:
            return main_verb, main_verb.get_position()
        else:
            return None, -1
    return None, -1


location = os.getcwd()  # get present working directory location here
corin_files_location = location + '/corin_clauses'

for file in os.listdir(corin_files_location):
    current = os.path.join(corin_files_location, file)
    if os.path.isfile(current):
        file_sentences = '../textos_corin/corin_final_clauses/' + file.split('.')[0] + '.xml'
        with open(current, 'r') as data_file:
            with open(file_sentences, 'w') as output_file:
                data = json.load(data_file)
                # output_file.write("<?xml version='1.0' encoding='utf-8'?>")
                output_file.write("<article>")
                for clause, verb_info in data:
                    clean_clause = clause.lstrip()
                    clean_clause = clean_clause.replace("\"", "")
                    main_verb, position = find_main_verb_position(clean_clause, verb_info)
                    clean_clause = clean_clause.replace('&', '&amp;')
                    if main_verb == None:
                        # Discard clause if it has no main verb
                        continue
                    # Get clause tokens removing empty spaces
                    clause_tokens = [
                        token for token in clean_clause.split(' ') if token != '']
                    if clause_tokens[position] == main_verb.get_form():
                        clause_tokens[position] = "<verbo subject='' tag='{}' form='{}' lemma='{}'>{}</verbo>".format(
                            main_verb.get_tag(), main_verb.get_form(), main_verb.get_lemma(), main_verb.get_form())
                    else:
                        try:
                            idx = clause_tokens.index(main_verb.get_form())
                        except ValueError:
                            print('No se encontro verbo "{}" en clausula "{}"'.format(
                                main_verb.get_form(), clean_clause))
                            continue
                        clause_tokens[idx] = "<verbo subject=''>{}</verbo>".format(
                            main_verb.get_form())

                    output_file.write("<clausula>{}</clausula>".format(
                        " ".join(clause_tokens)))
                output_file.write("</article>")
        xml_parser = etree.XMLParser(remove_blank_text=True, encoding='utf-8')
        doc = etree.parse(file_sentences, xml_parser)
        doc.write(file_sentences, pretty_print=True, encoding='utf-8')
