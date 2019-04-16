import json
import os
import xml.etree.ElementTree


def getTaggedClauses(file):
    location = os.getcwd()  # get present working directory location here
    corin_files_location = location + '/../anotadas/'
    current = os.path.join(corin_files_location, file)
    clauses = []
    if os.path.isfile(current):
        with open(current) as data_file:
            parser = xml.etree.ElementTree.XMLParser(encoding='utf-8')
            doc = xml.etree.ElementTree.parse(current, parser).getroot()
            for clause in doc.findall('clausula'):
                clauses.append([
                    "".join([t for t in clause.itertext()]),
                    clause.find('verbo').attrib['subject'].upper()])
    return clauses


def getVerbClauses(file):
    location = os.getcwd()  # get present working directory location here
    corin_files_location = location + '/corin_clauses/'
    current = os.path.join(corin_files_location, file)
    clauses = []
    if os.path.isfile(current):
        with open(current) as data_file:
            clauses = json.load(data_file)
    return clauses


def getSubjectClause(tagged_clauses, clause):
    for c in tagged_clauses:
        clean_clause = clause.lstrip()
        clean_clause = clean_clause.replace("\"", "")
        clean_clause = clean_clause.replace('&', '&amp;')
        if "".join(c[0].split()) == "".join(clean_clause.split()):
            return c[1]
    return None


def getFinalClauses(tagged_clauses, verb_clauses):
    clauses = []
    for c in verb_clauses:
        subject = getSubjectClause(tagged_clauses, c[0])
        if (subject is not None):
            clauses.append({
                'subject': subject,
                'verb': c[1],
                'clause': c[0]
            })
    return clauses


location = os.getcwd()  # get present working directory location here
corin_files_location = location + '/../anotadas/'
for file in os.listdir(corin_files_location):
    tagged_clauses = getTaggedClauses(file)
    verb_clauses = getVerbClauses(file.split('.')[0] + '.json')
    location = os.getcwd()
    file_clauses = location + '/corin_clauses_dict/' + file.split('.')[0] + '.json'
    clauses = getFinalClauses(tagged_clauses, verb_clauses)
    with open(file_clauses, 'w') as f:
            json.dump(clauses, f, ensure_ascii=False)
