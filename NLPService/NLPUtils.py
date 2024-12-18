from spacy import Language
from spacy.tokens import Span
from spacytextblob.spacytextblob import SpacyTextBlob


class NLPUtils:

    def __init__(self, nlp: Language):
        self.nlp = nlp
        # todo move this to the appropriate place
        self.nlp.add_pipe('spacytextblob')

    @staticmethod
    def clean_text(text: Span) -> str:
        words = []
        pos = text.root.head.pos_
        for token in text:
            # remove filler stopwords
            if token.dep_ not in ["poss", "det", "punct"]:
                words.append(token.lemma_.lower())
        final_text = " ".join(words)
        # for now, omitting noun chunks whose head isn't a verb
        if pos == "VERB":
            feature_text = f'{text.root.head.lemma_} {final_text}'
            return feature_text
        if text.root.head == text.root:
            feature_text = f'{final_text}'
            return feature_text
        return ""

    def extract_features(self, text: str, relevant_dependencies: list, ignore_verbs: list) -> list:
        document = self.nlp(text)
        features = []
        for chunk in document.noun_chunks:
            lemma = chunk.root.head.lemma_
            if chunk.root.dep_ in relevant_dependencies and \
                    chunk.root.pos_ not in ['PRON'] and \
                    lemma not in ignore_verbs:

                feature = self.clean_text(chunk)
                if feature and feature not in features:
                    features.append(feature)

        return features

    def analyze_sentiment(self, text: str) -> tuple:
        doc = self.nlp(text)
        polarity = doc._.blob.polarity
        subjectivity = doc._.blob.subjectivity

        return polarity, subjectivity
