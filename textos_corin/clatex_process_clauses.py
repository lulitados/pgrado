import json
import os
from subprocess import call

location = os.getcwd()  # get present working directory location here
corin_files_location = location + '/corin_for_clatex'

for file in os.listdir(corin_files_location):
    current = os.path.join(corin_files_location, file)
    if os.path.isfile(current):
        file_sentences = 'corin_clauses_sources/' + file.split('.')[0] + '.txt'
        call([
            'swipl',
            '-s',
            '../../clatex2015/controlEn.pl',
            '-g',
            "proceso('{}','{}'),halt".format(current, file_sentences)
        ])
        with open(file_sentences, 'r') as f:
            data = f.read().splitlines(True)
        with open(file_sentences, 'w') as f:
            f.writelines(data[3:])
