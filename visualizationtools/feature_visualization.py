import argparse

from spacy import displacy

from NLPService.NLPUtils import NLPUtils
from NLPService.PipelineBuilder import PipelineBuilder

import sys


def custom_extract_features(self, text: str, relevant_dependencies: list, ignore_verbs: list):
    document = self.nlp(text)
    features = []
    spans = []
    for chunk in document.noun_chunks:
        lemma = chunk.root.head.lemma_
        if chunk.root.dep_ in relevant_dependencies and \
                chunk.root.pos_ not in ['PRON'] and \
                lemma not in ignore_verbs:

            feature = self.clean_text(chunk)
            if feature:
                span = (min(chunk.root.head.idx, chunk.start_char), chunk.end_char)
                spans.append(span)
                features.append(feature)

    return features, spans


ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', required=True, help="The file containing the text to process.")
ap.add_argument('-c', '--configuration', required=True, help="File with the customization parameters.")

args = vars(ap.parse_args())

with open(args['file'], 'r', encoding='utf-8') as source_file:
    text_to_process = source_file.read()

config = {}

with open(args['configuration'], 'r', encoding='utf-8') as config_file:
    aux = config_file.read()
    aux = aux.split('\n')
    for item in aux:
        data = item.split('=')
        config[data[0]] = [x.strip() for x in data[1].split(',')]

nlp_model = PipelineBuilder()
nlp = NLPUtils(nlp_model.get_model())
nlp.extract_features = custom_extract_features

osmand_doc = nlp.nlp(text_to_process)


ft, sp = nlp.extract_features(nlp, text_to_process, config['dependencies'], config['ignore-verbs'])

entities = []
for f, s in zip(ft, sp):
    aux = osmand_doc.char_span(s[0], s[1], "feature")
    entities.append(aux)

osmand_doc.ents = entities

displacy.serve(osmand_doc, style="ent", host='localhost', options={"colors": {"feature": '#CBC3E3'}})
