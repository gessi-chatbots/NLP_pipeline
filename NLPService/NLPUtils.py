from spacy import Language, displacy


class NLPUtils:

    def __init__(self, nlp: Language):
        self.nlp = nlp

    def extract_features(self, text: str, relevant_dependencies: list) -> list:
        document = self.nlp(text)
        features = []
        for syntactic_dependency in relevant_dependencies:
            for chunk in document.noun_chunks:
                # if "lots" in chunk.text:
                #     displacy.serve(document, style="dep")
                if chunk.root.dep_ in syntactic_dependency and chunk.root.pos_ not in ['PRON']:
                    head = chunk.root.head
                    print(f'{head.text} is in {head.morph}')
                    features.append(f'{chunk.root.head.text.lower()} {chunk.text.lower()}')

        return features

    def analyze_sentiment(self, text: str) -> tuple:
        self.nlp.add_pipe('spacytextblob')
        doc = self.nlp(text)
        polarity = doc._.blob.polarity
        subjectivity = doc._.blob.subjectivity

        return polarity, subjectivity
