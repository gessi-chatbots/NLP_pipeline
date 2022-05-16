import json
from collections import Counter

import spacy
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy import displacy

nlp = spacy.load("en_core_web_trf")
stop_words = nlp.Defaults.stop_words


def clean_text(text_to_clean):
    new_data = []
    for individual_text in text_to_clean:
        doc = nlp(individual_text)
        result = [token for token in doc if not token.is_punct and token not in stop_words]
        result = [word for word in result if word.text not in stop_words]
        new_data.append(' '.join(token.text for token in result))
    return new_data


def get_keywords(text_to_analyze):
    results = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN']
    doc = nlp(text_to_analyze.lower())
    for token in doc:
        if token.text in nlp.Defaults.stop_words or token.is_punct:
            continue
        if token.pos_ in pos_tag:
            results.append(token.text)
    return results


with open("nlp.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

text = []
reviews = {}
for item in data:
    text.append(item['description'])
    reviews[item['app_name']] = []
    for comments in item['reviews']:
        reviews[item['app_name']].append(comments['review'])

trimmed_revs = {}
for i, app in enumerate(reviews.keys()):
    trimmed_revs[i] = []
    for element in reviews[app]:
        aux = element.split()
        if len(aux) > 5:
            trimmed_revs[i].append(element)

kw = get_keywords(text[0])

document = nlp(text[0])
chunks = []
for chunk in document.noun_chunks:
    if chunk.root.dep_ == 'dobj' or chunk.root.dep_ == 'advcl' or chunk.root.dep_ == 'attr':
        chunks.append(chunk.text)


# displacy.serve(document.sents.__next__(), style='dep')

important_kw = [x for x in Counter(kw).most_common(10)]

print(chunks)
print(important_kw)

