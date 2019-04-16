# import xml.etree.ElementTree
# import re
import os
import json


class ElliphantCorpus:
    # OLD CORPUS
    # def __init__(self, source_mode=None):
    #     self._health_sources = [
    #         'elliphant_raw/elliphant_eszic_es_health_1.xml',
    #         'elliphant_raw/elliphant_eszic_es_health_2.xml',
    #         'elliphant_raw/elliphant_eszic_es_health_3.xml',
    #         'elliphant_raw/elliphant_eszic_es_health_4.xml',
    #         'elliphant_raw/elliphant_eszic_es_health_5.xml',
    #         'elliphant_raw/elliphant_eszic_es_health_6.xml',
    #         'elliphant_raw/elliphant_eszic_es_health_7.xml',
    #         'elliphant_raw/elliphant_eszic_es_health_8.xml',
    #         'elliphant_raw/elliphant_eszic_es_health_9.xml'
    #     ]
    #     self._health_sentences = 1702
    #     self._legal_sources = [
    #         'elliphant_raw/elliphant_eszic_es_legal_1.xml',
    #         'elliphant_raw/elliphant_eszic_es_legal_2.xml',
    #         'elliphant_raw/elliphant_eszic_es_legal_3.xml',
    #         'elliphant_raw/elliphant_eszic_es_legal_4.xml',
    #         'elliphant_raw/elliphant_eszic_es_legal_5.xml',
    #         'elliphant_raw/elliphant_eszic_es_legal_6.xml',
    #         'elliphant_raw/elliphant_eszic_es_legal_7.xml',
    #         'elliphant_raw/elliphant_eszic_es_legal_8.xml'
    #     ]
    #     self._legal_sentences = 3510

    #     if source_mode == 1:
    #         self.sources = self._health_sources
    #         self.total_sentences = self._health_sentences
    #     elif source_mode == 2:
    #         self.sources = self._legal_sources
    #         self.total_sentences = self._legal_sentences
    #     else:
    #         self.sources = self._health_sources + self._legal_sources
    #         self.total_sentences = (
    #             self._health_sentences + self._legal_sentences)

    # def _process_sentence(self, sentence):
    #     result = " ".join(
    #         [child.find('text').text for child in sentence.getchildren()])
    #     return re.sub(r' (\W)', r'\1', result)

    # def __iter__(self):
    #     for source in self.sources:
    #         parser = xml.etree.ElementTree.XMLParser(encoding='utf-8')
    #         doc = xml.etree.ElementTree.parse(source, parser).getroot()
    #         for sentence in doc.findall('sentence'):
    #             yield (self._process_sentence(sentence),
    #                    source,
    #                    sentence.get('id'))
    def __init__(self):
        self.total_clauses = 5496

    def __iter__(self):
        location = os.getcwd()  # get present working directory location here
        elliphant_files_location = location + '/elliphant/new_extracted_clauses_dict'
        for file in os.listdir(elliphant_files_location):
            current = os.path.join(elliphant_files_location, file)
            if os.path.isfile(current):
                with open(current) as data_file:
                    data = json.load(data_file)
                    for clause in data:
                        yield(clause['clause'], clause['verb'], clause['subject'])
