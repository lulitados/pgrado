import json
import os  # os module imported here
from extract_data_ancora import get_sentences_source


location = os.getcwd()  # get present working directory location here
ancora_files_location = location + '/ancora_raw'

for file in os.listdir(ancora_files_location):
    current = os.path.join(ancora_files_location, file)
    if os.path.isfile(current):
        file_sentences = 'ancora_processed/' + file.split('.')[0] + '.json'
        sentences = get_sentences_source(current)
        with open(file_sentences, 'w') as f:
            json.dump(sentences, f, ensure_ascii=False)
