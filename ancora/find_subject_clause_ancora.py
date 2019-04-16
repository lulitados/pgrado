import json
import os  # os module imported here

location = os.getcwd()  # get present working directory location here

CLAUSES_DIR = location + '/ancora_clauses/'
DATA_DIR = location + '/ancora_processed/'


def get_sentence_from_data(data):
    sentence = []
    for word in data:
        sentence += word['wd'].split('_')
    return ' '.join(sentence)


def get_clause(clause):
    clause = clause.split()
    new_clause = []
    for word in clause:
        new_clause += word.split('_')
    return ' '.join(new_clause)


def get_clause_data(clause, sentence):
    clause_words = clause.split()
    clause_pos = 0
    sentence_start = 0
    sentence_pos = 0
    while clause_pos < len(clause_words) and \
            (sentence_start + sentence_pos) < len(sentence):
        token = sentence[sentence_start + sentence_pos]
        words_in_token = token['wd'].split('_')
        for word in words_in_token:
            if word == clause_words[clause_pos]:
                clause_pos += 1
            else:
                clause_pos = 0
                sentence_pos = -1
                sentence_start += 1
                break
        sentence_pos += 1
    if clause_pos == len(clause_words):
        return sentence[sentence_start:sentence_start + sentence_pos]
    return []


def get_suj_clause(clause_data, verb):
    for token in clause_data:
        if 'suj' in token and token['wd'] == verb:
            if 'elliptic' in token['suj']:
                return 'ZERO'
            elif 'func' in token['suj'] and token['suj']['func'] == 'impers':
                return 'IMPERSONAL'
            else:
                return 'SUBJECT'
    return None


def find_subjects_clauses(clauses_source, data_source):
    file_clauses = []
    discarded_clauses = []
    with open(clauses_source, 'r') as in_file:
        clauses = json.load(in_file)
    with open(data_source, 'r') as in_file:
        data = json.load(in_file)
    clauses.reverse()
    sentence_idx = 0
    clause_idx = 0
    cant_sentences = len(data)
    while clause_idx < len(clauses) and sentence_idx < cant_sentences:
        clause = get_clause(clauses[clause_idx][0])
        if clause in get_sentence_from_data(data[sentence_idx]):
            # Clausula esta en la oracion
            clause_data = get_clause_data(clause, data[sentence_idx])
            clause_suj = get_suj_clause(clause_data, clauses[clause_idx][1]['form'])
            if clause_suj is not None:
                file_clauses.append({
                    'clause': clause,
                    'subject': clause_suj,
                    'verb': {
                        'lemma': clauses[clause_idx][1]['lemma'],
                        'form': clauses[clause_idx][1]['form'],
                        'tag': clauses[clause_idx][1]['tag']
                    }
                })
            else:
                # print("Discarded: {}\n\n\n".format(clause))
                discarded_clauses.append(clause)
            clause_idx += 1
        else:
            sentence_idx += 1
    return file_clauses, discarded_clauses


# for file in ['10017_20000413.json']:
for file in os.listdir(CLAUSES_DIR):
    current_clauses = os.path.join(CLAUSES_DIR, file)
    current_data = os.path.join(DATA_DIR, file)
    if os.path.isfile(current_clauses) and os.path.isfile(current_data):
        clauses_file = 'ancora_clauses_dict/' + file
        discarded_clauses = 'discarded_ancora_clauses_dict/' + file
        clauses, discarded = find_subjects_clauses(current_clauses, current_data)
        # print(clauses)
        with open(clauses_file, 'w') as f:
            json.dump(clauses, f, ensure_ascii=False)
        with open(discarded_clauses, 'w') as f:
            json.dump(discarded, f, ensure_ascii=False)

