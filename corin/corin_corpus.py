import os
import json


class CorinCorpus:
    def __init__(self):
        self.total_clauses = 623

    def __iter__(self):
        location = os.getcwd()  # get present working directory location here
        corin_files_location = location + '/textos_corin/corin_clauses_dict'
        for file in os.listdir(corin_files_location):
            current = os.path.join(corin_files_location, file)
            if os.path.isfile(current):
                with open(current) as data_file:
                    print(current)
                    data = json.load(data_file)
                    for clause in data:
                        yield(clause['clause'], clause['verb'], clause['subject'])
