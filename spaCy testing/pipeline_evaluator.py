import json

import spacy
from spacy import Language
from utils import *

spacy.require_cpu()


# custom component for nlp pipeline
@Language.component('set_boundaries')
def set_boundaries(doc):
    boundaries = ['\n', '.\n', '\n\n']
    for token in doc[:-1]:
        if token.text in boundaries:
            doc[token.i + 1].is_sent_start = True
        else:
            doc[token.i + 1].is_sent_start = False

    return doc


nlp = spacy.load("en_core_web_trf")
nlp.add_pipe('set_boundaries', before='parser')

with open('osmand-alt.txt', 'r', encoding='utf-8') as file:
    description_text = file.read()

with open('OsmAnd-features-AlternativeTo.json', 'r', encoding='utf-8') as file:
    raw_expected_results = json.load(file)

dependencies = ['dobj', 'advcl', 'attr', 'appos']

extracted_features = extract_features(description_text, dependencies, nlp)

initial = 0.1
results = {}
positives = {}
for i in range(10):
    threshold = initial*i
    metrics, true_positives = assess_quality(extracted_features, raw_expected_results, 'similarity', threshold=threshold)
    results[f'threshold {i}'] = metrics
    positives[f'threshold {i}'] = true_positives

with open("evaluation.json", 'w', encoding='utf-8') as file:
    print(json.dumps(results,indent=4), file=file)
    print(json.dumps(positives, indent=4), file=file)
