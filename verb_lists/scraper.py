import re
# import logging
# import urllib
# import html
# import time
import os
import json

import requests

from bs4 import BeautifulSoup


def get_verbs_from_page(soup):
    verb_list = []
    letter_verbs = soup.find_all('div','mw-category-group')
    for letter in letter_verbs:
        verbs = letter.find_all('li')

        for verb in verbs:
            verb_list.append(verb.text)

    return verb_list


def scrape_verb_lists():
    lists_to_scrape = [
        ('pronominal_verbs.json', 'https://es.wiktionary.org/wiki/Categor%C3%ADa:ES:Verbos_pronominales'),
        ('transitive_verbs.json', 'https://es.wiktionary.org/wiki/Categor%C3%ADa:ES:Verbos_transitivos'),
        ('intransitive_verbs.json', 'https://es.wiktionary.org/wiki/Categor%C3%ADa:ES:Verbos_intransitivos'),
        ('impersonal_verbs.json', 'https://es.wiktionary.org/wiki/Categor%C3%ADa:ES:Verbos_impersonales'),
        ('pronominal_only_verbs.json', 'https://es.wiktionary.org/wiki/Categor%C3%ADa:ES:Verbos_solo_pronominales'),
        ('pronominal_use_verbs.json', 'https://es.wiktionary.org/wiki/Categor%C3%ADa:ES:Verbos_con_uso_pronominal')
    ]
    base_url = 'https://es.wiktionary.org'

    for output_file, resource_url in lists_to_scrape:
        verb_list = []
        verb_list_page = requests.get(resource_url).text
        soup = BeautifulSoup(verb_list_page, "lxml")

        verb_list += get_verbs_from_page(soup)

        next_page = soup.find('a', text=re.compile('página siguiente'))
        while next_page is not None:
            verb_list_page = requests.get(
                base_url + next_page.attrs['href']).text
            soup = BeautifulSoup(verb_list_page, "lxml")

            verb_list += get_verbs_from_page(soup)
            next_page = soup.find('a', text=re.compile('página siguiente'))

        with open(output_file, 'w') as f:
            json.dump(verb_list, f, ensure_ascii=False)


scrape_verb_lists()
