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


dependencies = ['dobj', 'advcl', 'appos', 'ROOT']

app = flask.Flask(__name__)
app.config['DEBUG'] = True

nlp_model = PipelineBuilder()
nlp = NLPUtils(nlp_model.get_model())


@app.route('/extract-features', methods=['POST'])
def get_features():
    data = None

    ignore_verbs = 'ignore-verbs' in request.json.keys()
    if 'text' not in request.json.keys():
        return "Lacking textual data in proper tag.", 400

    try:
        data = request.get_json()
    except BadRequest:
        return "Input data has a formatting error.", 400

    to_return = []

    if ignore_verbs:
        verbs_to_ignore = data['ignore-verbs']
    else:
        verbs_to_ignore = []

    for text in data['text']:
        features = nlp.extract_features(text['text'], dependencies, verbs_to_ignore)
        to_return.append({'id': text['id'], 'features': features})

    return json.dumps(to_return, indent=4)


@app.route('/review-extraction', methods=['POST'])
def process_reviews():
    min_subj = request.json['minSubj'] if 'minSubj' in request.json.keys() else 0
    max_subj = request.json['maxSubj'] if 'maxSubj' in request.json.keys() else 1
    min_pol = request.json['minPol'] if 'minPol' in request.json.keys() else -1
    max_pol = request.json['maxPol'] if 'maxPol' in request.json.keys() else 1

    if 'text' not in request.json.keys():
        return "Lacking textual data in proper tag.", 400

    ignore_verbs = 'ignore-verbs' in request.json.keys()

    if ignore_verbs:
        verbs_to_ignore = request.json['ignore-verbs']
    else:
        verbs_to_ignore = []

    reviews = request.json['text']

    to_return = []

    for review in reviews:
        pol, subj = nlp.analyze_sentiment(review['text'])
        if min_pol <= pol <= max_pol and min_subj <= subj <= max_subj:
            features = nlp.extract_features(review['text'], dependencies, verbs_to_ignore)
            to_return.append({'id': review['id'], 'features': features})

    return to_return


app.run()
