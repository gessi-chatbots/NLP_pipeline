from spacy import displacy

from NLPService.NLPUtils import NLPUtils
from NLPService.PipelineBuilder import PipelineBuilder


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
                span = (chunk.root.head.idx, chunk.end_char)
                spans.append(span)
                features.append(feature)

    return features, spans


# edit to provide different input texts.
with open('osmand-alt.txt', 'r', encoding='utf-8') as alt_osmand:
    alt_text = alt_osmand.read()

nlp_model = PipelineBuilder()
nlp = NLPUtils(nlp_model.get_model())
nlp.extract_features = custom_extract_features

osmand_doc = nlp.nlp(alt_text)
ft, sp = nlp.extract_features(nlp, alt_text, ['dobj', 'advcl', 'appos', 'ROOT'], [])

entities = []
for f, s in zip(ft, sp):
    aux = osmand_doc.char_span(s[0], s[1], "feature")
    entities.append(aux)

osmand_doc.ents = entities

displacy.serve(osmand_doc, style="ent", options={"colors": {"feature": 'purple'}})