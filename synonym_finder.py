#!/usr/local/bin/python3

##################################################################################
# “AS-IS” Clause
#
# Except as represented in this agreement, all work produced by Developer is
# provided ​“AS IS”. Other than as provided in this agreement, Developer makes no
# other warranties, express or implied, and hereby disclaims all implied warranties,
# including any warranty of merchantability and warranty of fitness for a particular
# purpose.
##################################################################################

##################################################################################
#
# Date Completed: September 15, 2020
# Author: John Bumgarner
#
# Date Revised:
# Revised by:
#
# This Python script is designed to query multiple sources to obtain synonyms
# related to a string variable (e.g., mother). The output is an aggregated
# list of synonyms for the specific variable.
#
# Modules used:
# 1. BeautifulSoup
# 2. collections
# 3. NLTK
# 4. requests
# 5. re
#
# Module References:
# https://www.crummy.com/software/BeautifulSoup
# https://docs.python.org/3/library/collections.html
# https://www.nltk.org
# https://requests.readthedocs.io/en/master/
# https://docs.python.org/3/library/re.html
#
##################################################################################

################################################
# Python imports required for basic operations
################################################
import re
import requests
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from collections import defaultdict

# Internal utilities
from utilities import basic_soup


def query_collins_dictionary_synonym(word):
    """
    This function queries collinsdictionary.com for synonyms
    related to the 'word' parameter.

    :param word: string variable to search for
    :return: list of synonyms
    """
    synonyms = []
    results_synonym = basic_soup.get_single_page_html(f'https://www.collinsdictionary.com/dictionary/english-thesaurus/{word}')
    query_results = basic_soup.query_html(results_synonym, 'div', 'class', 'blockSyn')
    content_descendants = query_results.descendants
    for item in content_descendants:
        if item.name == 'div' and item.get('class', 'form type-syn orth'):
            children = item.findChild('span', {'class': 'orth'})
            if children is not None:
                synonyms.append(children.text)
    return synonyms


def query_synonym_com(word):
    """
    This function queries synonym.com for synonyms
    related to the 'word' parameter.

    :param word: string variable to search for
    :return: list of synonyms
    """
    results_synonym = basic_soup.get_single_page_html(f'https://www.synonym.com/synonyms/{word}')
    soup = BeautifulSoup(results_synonym, "html.parser")
    description_tag = soup.find("meta", property="og:description")
    find_synonyms = re.split(r'\|', description_tag['content'])
    synonyms = find_synonyms[2].lower().replace('synonyms:', '').split(',')
    return synonyms


def query_thesaurus_com(word):
    """
    This function queries thesaurus.com for synonyms
    related to the 'word' parameter.

    :param word: string variable to search for
    :return: list of synonyms
    """
    req = requests.get(f'https://tuna.thesaurus.com/pageData/{word}', headers=basic_soup.http_headers,
                       allow_redirects=True, verify=True, timeout=30)
    dict_synonyms = req.json()['data']['definitionData']['definitions'][0]['synonyms']
    synonyms = [r["term"] for r in dict_synonyms]
    return synonyms


def query_wordnet_synonyms(word):
    """
    This function queries NLTK wordnet for synonyms
    related to the 'word' parameter.

    :param word: string variable to search for
    :return: list of synonyms
    """
    synonyms = []
    for synonym in wn.synsets(word, wn.NOUN):
        if word != synonym.name() and len(synonym.lemma_names()) > 1:
            for item in synonym.lemmas():
                if word != item.name():
                    synonyms.append(item.name().lower())
    return synonyms


def query_all_sources(word):
    """
    This function calls the functions:
     - query_collins_dictionary_synonym
     - query_synonym_com
     - query_thesaurus_com
     - query_wordnet_synonyms

    :param word: string variable to search for with the other functions
    :return: aggregated list of synonyms
    """
    collins_results = query_collins_dictionary_synonym(f'{word}')
    synonym_results = query_synonym_com(f'{word}')
    thesaurus_results = query_thesaurus_com(f'{word}')
    wordnet_results = query_wordnet_synonyms(f'{word}')
    results = deduplicated_synonyms(collins_results, synonym_results, thesaurus_results, wordnet_results)
    return results


def key_exist_verification(values, search_term):
    """
    This function searches through the values a dictionary for a search_term.

    :param values: dictionary
    :param search_term: the value to look for in the dictionary's values.
    :return: key or none
    """
    for k in values:
        for v in values[k]:
            if search_term in v:
                return k
    return None


def deduplicated_synonyms(collins_synonyms, synonym_synonyms, thesaurus_synonyms, wordnet_synonyms):
    """
    This function combines multiple lists into a single list, which has been
    deduplicated and turned into a list of tuples.

    :param collins_synonyms: list of synonyms for a specific string variable
    :param synonym_synonyms: list of synonyms for a specific string variable
    :param thesaurus_synonyms: list of synonyms for a specific string variable
    :param wordnet_synonyms: list of synonyms for a specific string variable
    :return: aggregated list of synonyms
    """
    combined_results = list(set(collins_synonyms) | set(synonym_synonyms)
                            | set(thesaurus_synonyms) | set(wordnet_synonyms))
    deduplicated_results = sorted(set(map(str.strip, combined_results)))
    return deduplicated_results


all_synonyms = defaultdict(list)
sample_words = ['mother', 'mom', 'father']

for item in sample_words:
    value_exist = key_exist_verification(all_synonyms, item)
    if not value_exist:
        final_results = query_all_sources(f'{item}')
        all_synonyms[item].append(final_results)
    else:
        final_results = query_all_sources(f'{item}')
        all_synonyms[value_exist].extend(final_results)


for k, v in all_synonyms.items():
    print(k, v)



