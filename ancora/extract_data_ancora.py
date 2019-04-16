# import json
# import sys
import xml.etree.ElementTree as ET


def get_verb_pos(result, origin, end):
    for idx, elem in enumerate(result[origin:end]):
        if 'is_verb' in elem and elem['is_verb']:
            return origin + idx
    return -1


def process_sentence(node, result, real_length):
    looking_for_suj = False
    looking_for_verb = False
    verbPos = -1
    suj = {}
    if 'wd' in node.attrib:
        result.append(node.attrib)
        if node.tag == 'v':
            result[-1]['is_verb'] = True

    for child in node.getchildren():
        current_index = len(result) + real_length
        process = process_sentence(child, [], current_index)
        result += process

        # If child is suject
        if ('func' in child.attrib and child.get('func') == 'suj'):
            suj = child.attrib
            if 'elliptic' not in child.attrib:
                suj['begins'] = current_index
                suj['ends'] = len(result) + real_length - 1
            if looking_for_suj:
                result[verbPos]['suj'] = suj
                looking_for_suj = False
            else:
                looking_for_verb = True

        # If child is impersonal
        if ('func' in child.attrib and child.get('func') == 'impers'):
            suj = child.attrib
            if looking_for_suj:
                result[verbPos]['suj'] = suj
                looking_for_suj = False
            else:
                looking_for_verb = True

        # If child is group verb
        if child.tag == 'grup.verb':
            verb_pos = get_verb_pos(result, current_index - real_length, len(result))
            if verb_pos > -1:
                if looking_for_verb:
                    result[verb_pos]['suj'] = suj
                    looking_for_verb = False
                else:
                    looking_for_suj = True
    return result


def get_sentences_source(source):
    parser = ET.XMLParser(encoding='utf-8')
    doc = ET.parse(source, parser).getroot()
    sentences = []
    for sentence in doc.iter('sentence'):
        sentence_data = process_sentence(sentence, [], 0)
        sentences.append(sentence_data)
    return sentences


# input_file = sys.argv[1]
# input_clauses = get_sentences_source(input_file)

# print(json.dumps(input_clauses))
