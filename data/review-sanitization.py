import json

import spacy
from spacy import Language
from spacy_language_detection import LanguageDetector


def get_lang_detector(nlp, name):
    return LanguageDetector(seed=42)


nlp_model = spacy.load("en_core_web_trf")
Language.factory("language_detector", func=get_lang_detector)
nlp_model.add_pipe('language_detector', last=True)

with open('complete-data-set.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

reviews = {'text': []}

for app in data:
    for review in app['reviews']:
        if review['review']:
            doc = nlp_model(review['review'])
            language = doc._.language
            if len(review['review']) > 50:
                doc = nlp_model(review['review'])
                language = doc._.language
                if language['language'] == 'en':
                    reviews['text'].append({'id': app['package_name'] + review['reviewId'], 'text': review['review']})
    with open('first_review_cleaning.json', 'w', encoding='utf-8') as file:
        print(json.dumps(reviews, indent=4), file=file)



