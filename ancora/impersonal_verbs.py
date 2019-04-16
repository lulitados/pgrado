import json
import os  # os module imported here


def get_verbs_sentence(sentence):
    return [
        word for word in sentence
        if 'is_verb' in word and
        'suj' in word and
        word['suj']['func'] == 'impers'
    ]


location = os.getcwd()  # get present working directory location here
ancora_files_location = location + '/ancora_processed'
impersonal_verbs = []

for file in os.listdir(ancora_files_location):
    current = os.path.join(ancora_files_location, file)
    if os.path.isfile(current):
        with open(current) as data_file:
            data = json.load(data_file)
            for sentence in data:
                impersonal_verbs += get_verbs_sentence(sentence)

words = sorted(list(set([word['wd'] for word in impersonal_verbs])))
lemmas = sorted(list(set([word['lem'] for word in impersonal_verbs])))

result = {
    'counts': {
        'words': len(words),
        'lemmas': len(lemmas)
    },
    'words': words,
    'lemmas': lemmas,
}

with open('impersonal_verbs.json', 'w+') as o_file:
    json.dump(result, o_file, ensure_ascii=False)
