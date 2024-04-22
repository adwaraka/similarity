# Cosine Similarity Template
from numpy import dot
from numpy.linalg import norm
from pyinflect import getInflection
import re

ADDITIONAL_DELIMITERS = r'\-|\!|\.|,|\`|\?|\“|\”|\:|\;|>|<'
# possibly use an NLP library here; this was a specific use-case
EXCLUDED_WORDS = ["the",
                  "a",
                  "this",
                  "an",
                  "err",
                  "um",
                  "hi",
                  "page",
                  "link",
                  "instance",
                  "site",
                  "url",
                  "hello",
                  "team",
                  "everyone",
                  "someone",
                  "somebody",
                  "kindly",
                  "need",
                  "me",
                  "myself",
                  "to",
                  "please",
                  "help",
                  "plz",
                  "assist",
                  "assistance",
                  "i",
                  "thx",
                  ]


def remove_filler_words(query_stmt):
    refined_query = ""
    for word in query_stmt.split():
        if word.rstrip(",.") not in EXCLUDED_WORDS:
            refined_query = " ".join([refined_query, word.lower()])
    return refined_query.lstrip()


def wc_count(text, search_term):
    count = 0
    for sentence in re.split(ADDITIONAL_DELIMITERS, text):
        for word in sentence.split():
            if word == search_term:
                count += 1
    return count


def return_words(text):
    distinct_words = set()
    for sentence in re.split(ADDITIONAL_DELIMITERS, text):
        for word in sentence.split():
            distinct_words.add(word)
    return distinct_words


def detect_inflection(word_set):
    word_list = list(word_set)
    for word in word_list:
        try:
            inflected_word = getInflection(word, tag='VBG')[0]
            word_list.remove(inflected_word)
        except TypeError:
            pass
        except ValueError:
            pass
    return set(word_list)


def calculate_similarity(doc_1, curr_doc):
    doc_1, curr_doc = doc_1.lower(), curr_doc.lower()
    doc_1, curr_doc = remove_filler_words(doc_1), remove_filler_words(curr_doc)
    existing_stmt_vector, curr_stmt_vector = [], []
    word_set = return_words(doc_1) | return_words(curr_doc)

    fresh_word_set = detect_inflection(word_set)

    for word in fresh_word_set:
        existing_stmt_vector.append(wc_count(doc_1, word))
        curr_stmt_vector.append(wc_count(curr_doc, word))
    print(fresh_word_set)
    # print(existing_stmt_vector)
    # print(curr_stmt_vector)
    return(
        dot(existing_stmt_vector, curr_stmt_vector)/(
          norm(existing_stmt_vector) * norm(curr_stmt_vector)))



doc_1 = "Can somebody help me install p4v? Thx."
curr_doc = "I need help installing p4v. Please assist."
print(calculate_similarity(doc_1, curr_doc))

doc_2 = "can someone assist me with creating a github repo?"
curr_doc = "I need to create a github repo. Plz assist."
print(calculate_similarity(doc_2, curr_doc))

doc_3 = "I need help accessing panos repo. Can someone please help?"
curr_doc = "I request to access PANOS repo"
print(calculate_similarity(doc_3, curr_doc))

