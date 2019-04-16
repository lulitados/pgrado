import json
import os  # os module imported here
from extract_data_ancora import get_sentences_source
from subprocess import call

location = os.getcwd()  # get present working directory location here
ancora_files_location = location + '/ancora_for_clatex'

for file in os.listdir(ancora_files_location):
    current = os.path.join(ancora_files_location, file)
    if os.path.isfile(current):
        file_sentences = 'ancora_clauses_sources/' + file.split('.')[0] + '.txt'
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
