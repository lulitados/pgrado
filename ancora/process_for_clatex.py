import json
import os  # os module imported here


def get_attribute(word, attr):
    if attr in word:
        if attr == 'pos':
            if word[attr].startswith('f'):
                return word[attr].capitalize()
            return word[attr].upper()
        return word[attr]
    return ''


location = os.getcwd()  # get present working directory location here
ancora_files_location = location + '/ancora_processed'

for file in os.listdir(ancora_files_location):
    current = os.path.join(ancora_files_location, file)
    if os.path.isfile(current):
        file_sentences = 'ancora_for_clatex/' + file.split('.')[0] + '.txt'
        with open(current) as data_file:
            data = json.load(data_file)
            with open(file_sentences, 'w+') as o_file:
                for sentence in data:
                    for word in sentence:
                        o_file.write("{text} {lemma} {tag} {prob}\n".format(
                            text=get_attribute(word, 'wd'),
                            lemma=get_attribute(word, 'lem'),
                            tag=get_attribute(word, 'pos'),
                            prob='1.0'
                        ))
                    if len(sentence) > 0 and sentence[-1]['wd'] != '.':
                        o_file.write("{text} {lemma} {tag} {prob}\n".format(
                            text='.',
                            lemma='.',
                            tag='fp',
                            prob='1.0'
                        ))
                o_file.close()
