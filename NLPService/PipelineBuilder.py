import spacy
from spacy import Language


@Language.component('set_boundaries')
def set_boundaries(doc):
    boundaries = ['\n', '.\n', '\n\n']
    for token in doc[:-1]:
        if token.text in boundaries:
            doc[token.i + 1].is_sent_start = True
        else:
            doc[token.i + 1].is_sent_start = False

    return doc


class PipelineBuilder:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_trf")
        self.nlp.add_pipe('set_boundaries', before='parser')

    def get_model(self):
        return self.nlp