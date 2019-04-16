import re
import json


class ElliphantCorpus:
    def __init__(self, source_mode=None):
        # self._health_sources = [
        #     'elliphant_clauses/health_1_clauses.json',
        #     'elliphant_clauses/health_2_clauses.json',
        #     'elliphant_clauses/health_3_clauses.json',
        #     'elliphant_clauses/health_4_clauses.json',
        #     'elliphant_clauses/health_5_clauses.json',
        #     'elliphant_clauses/health_6_clauses.json',
        #     'elliphant_clauses/health_7_clauses.json',
        #     'elliphant_clauses/health_8_clauses.json',
        #     'elliphant_clauses/health_9_clauses.json'
        # ]
        self._health_sources = [
            'elliphant/clauses_dict/elliphant_eszic_es_health_1_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_2_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_3_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_4_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_5_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_6_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_7_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_8_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_9_clauses.txt'
        ]
        # Custom clauses count
        # self._health_clauses = 3187
        # Old Clatex clauses count
        # self._health_clauses = 2034
        # Corrected Clatex clauses
        # self._health_clauses = 3468
        self._health_clauses = 3688
        # self._legal_sources = [
        #     'elliphant_clauses/legal_1_clauses.json',
        #     'elliphant_clauses/legal_2_clauses.json',
        #     'elliphant_clauses/legal_3_clauses.json',
        #     'elliphant_clauses/legal_4_clauses.json',
        #     'elliphant_clauses/legal_5_clauses.json',
        #     'elliphant_clauses/legal_6_clauses.json',
        #     'elliphant_clauses/legal_7_clauses.json',
        #     'elliphant_clauses/legal_8_clauses.json'
        # ]
        self._legal_sources = [
            'elliphant/clauses_dict/elliphant_eszic_es_health_1_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_2_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_3_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_4_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_5_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_6_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_7_clauses.txt',
            'elliphant/clauses_dict/elliphant_eszic_es_health_8_clauses.txt'
        ]
        # Custom clauses count
        # self._legal_clauses = 3310
        # Old Clatex clauses count
        # self._legal_clauses = 1734
        # Corrected Clatex clauses
        # self._legal_clauses = 2129
        self._legal_clauses = 2262

        # total = 5800
        if source_mode == 1:
            self.sources = self._health_sources
            self.total_clauses = self._health_clauses
        elif source_mode == 2:
            self.sources = self._legal_sources
            self.total_clauses = self._legal_clauses
        else:
            self.sources = self._health_sources + self._legal_sources
            self.total_clauses = (
                self._health_clauses + self._legal_clauses)

    def __iter__(self):
        for source in self.sources:
            with open(source) as data_file:
                data = json.load(data_file)
                for clause in data:
                    yield(clause['clause'], clause['subject'])
