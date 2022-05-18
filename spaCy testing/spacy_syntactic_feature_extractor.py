import json

import spacy
from spacy import Language


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

# loading text to extract features from
with open('osmand-alt.txt', 'r', encoding='utf-8') as alt_osmand:
    text = alt_osmand.read()

# load features to compare
with open('OsmAnd-features-Description(AlternativeTo).json', 'r', encoding='utf-8') as file:
    raw_expected_results = json.load(file)

expected_results = [x.lower() for x in raw_expected_results]

syntactic_dependencies = ['dobj', 'advcl', 'attr']
additional_dependencies = ['appos', 'conj', '']

alt_document = nlp(text)
for sent in alt_document.sents:
    print(sent)
alt_chunks = []

chunks = {}
for i in range(3):
    alt_chunks = []
    for chunk in alt_document.noun_chunks:
        if chunk.root.dep_ in syntactic_dependencies:
            # alt_chunks.append((chunk.root.head.text, chunk.text))
            alt_chunks.append(f'{chunk.root.head.text.lower()} {chunk.text.lower()}')
    chunks[i] = alt_chunks
    with open('osmand_alt_automatic_features.txt', 'a', encoding='utf-8') as file:
        print(syntactic_dependencies, file=file)
        for chunk in alt_chunks:
            print(chunk, file=file)
    syntactic_dependencies.append(additional_dependencies[i])

intersections = {}
differences = {}
metrics = []
for i in range(3):
    true_positives = []
    for chunk in chunks[i]:
        for expected in expected_results:
            if expected in chunk or chunk in expected:
                true_positives.append(chunk)
    # true_positives = [x for x in chunks[i] if x in [y for y in expected_results if y in x]]
    precision = round(len(true_positives) / len(chunks[i]), 3)
    recall = round(len(true_positives) / len(expected_results), 3)
    fscore = round(2 * (precision * recall) / (precision + recall), 3)
    metrics.append((precision, recall, fscore))
    for j in range(3):
        if i != j:
            inters = [x for x in chunks[i] if x in chunks[j]]
            intersections[f'{i} inters {j}'] = inters
            diff = [x for x in chunks[i] if x not in chunks[j]]
            if diff:
                differences[f'{i} minus {j}'] = diff

with open('metrics.txt', 'w', encoding='utf-8') as file:
    print(f'precision\trecall\tfscore', file=file)
    for metric in metrics:
        print(f'{metric[0]}\t{metric[1]}\t{metric[2]}', file=file)

with open('differences.txt', 'w', encoding='utf-8') as file:
    for k, element in differences.items():
        print(k, file=file)
        for new_item in element:
            print(new_item, file=file)
        print('\n', file=file)
