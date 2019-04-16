import os  # os module imported here

from extract_clatex_clauses import extract_caluses

location = os.getcwd()  # get present working directory location here
ancora_files_location = location + '/../ancora/ancora_clauses_sources'

for file in os.listdir(ancora_files_location):
    current = os.path.join(ancora_files_location, file)
    if os.path.isfile(current):
        file_sentences = '../ancora/ancora_clauses/' + file.split('.')[0] + '.json'
        extract_caluses(current, file_sentences)

# Extraer clausulas de corpus Corin
# location = os.getcwd()  # get present working directory location here
# corin_files_location = location + '/../textos_corin/corin_clauses_sources'

# for file in os.listdir(corin_files_location):
#     current = os.path.join(corin_files_location, file)
#     if os.path.isfile(current):
#         file_sentences = '../textos_corin/corin_clauses/' + file.split('.')[0] + '.json'
#         extract_caluses(current, file_sentences)


# # Extraer de clausulas de corpus Elliphant
# location = os.getcwd()  # get present working directory location here
# ancora_files_location = location + '/../elliphant/extracted_clauses'

# for file in os.listdir(ancora_files_location):
#     current = os.path.join(ancora_files_location, file)
#     if os.path.isfile(current):
#         file_sentences = '../elliphant/new_extracted_clauses/' + file.split('.')[0] + '.json'
#         extract_caluses(current, file_sentences)
