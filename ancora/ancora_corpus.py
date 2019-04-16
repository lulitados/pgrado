import os
import json


class AncoraCorpus:
    def __init__(self):
        # Clauses without impersonal
        # self.total_clauses = 38074
        # Clauses with impersonal
        self.total_clauses = 26505

    # Total sentences: 57830 (before matching subject)
    def __iter__(self):
        location = os.getcwd()  # get present working directory location here
        ancora_files_location = location + '/ancora/ancora_clauses_dict'
        for file in os.listdir(ancora_files_location):
            current = os.path.join(ancora_files_location, file)
            if os.path.isfile(current):
                with open(current) as data_file:
                    data = json.load(data_file)
                    for clause in data:
                        yield(clause['clause'], clause['verb'], clause['subject'])
