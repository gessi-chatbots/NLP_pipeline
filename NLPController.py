import json

import flask
from flask import request
from spacy import Language
from werkzeug.exceptions import BadRequest

from NLPService.NLPUtils import NLPUtils
from NLPService.PipelineBuilder import PipelineBuilder


@Language.component('set_boundaries')
def set_boundaries(doc):
    boundaries = ['\n', '.\n', '\n\n']
    for token in doc[:-1]:
        if token.text in boundaries:
            doc[token.i + 1].is_sent_start = True
        else:
            doc[token.i + 1].is_sent_start = False

    return doc


dependencies = ['dobj', 'advcl', 'appos']

app = flask.Flask(__name__)
app.config['DEBUG'] = True

nlp_model = PipelineBuilder()
nlp = NLPUtils(nlp_model.get_model())


@app.route('/extract-features', methods=['POST'])
def get_features():
    if request.args.get('text', default='true'):
        try:
            data = request.get_json()
        except BadRequest:
            return "Input data has a formatting error. The service expects a JSON array of textual data.", 400
        to_return = []
        for text in data:
            features = nlp.extract_features(text, dependencies)
            to_return.extend(features)
        return json.dumps(to_return)
    return 0


app.run()