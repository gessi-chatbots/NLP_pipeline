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


nlp_model = PipelineBuilder()
nlp = NLPUtils(nlp_model.get_model())


def create_app():
    app = flask.Flask(__name__)

    @app.route('/extract-features', methods=['POST'])
    def get_features():
        data = None

        ignore_verbs = 'ignore-verbs' in request.json.keys()
        received_dependencies = 'dependencies' in request.json.keys()

        if 'text' not in request.json.keys():
            return "Lacking textual data in proper tag.", 400

        try:
            data = request.get_json()
        except BadRequest:
            return "Input data has a formatting error.", 400

        to_return = []

        verbs_to_ignore = data['ignore-verbs'] if ignore_verbs else [
            "love", "hate", "enjoy", "admire", "adore", "despise", "cherish", "regret",
            "forgive", "fear", "crave", "miss", "appreciate", "expect", "hope", "wish",
            "remember", "forget", "imagine", "understand", "believe", "doubt", "assume",
            "realize", "care", "complain", "worry", "trust", "wonder", "surprise", 
            "amaze", "astonish", "fascinate", "impress", "bore", "annoy", "irritate", 
            "anger", "confuse", "disappoint", "excite", "inspire", "motivate", "amuse",
            "entertain", "satisfy", "please", "frustrate", "overwhelm", "reassure", 
            "relax", "stress", "scare", "shock", "startle", "terrify", "oppose", 
            "encourage", "discourage", "criticize", "praise", "thank", "apologize"]

        dependencies = data['dependencies'] if received_dependencies else ['dobj', 'advcl', 'appos', 'ROOT']

        for text in data['text']:
            if type(text) != dict or 'id' not in text.keys() or 'text' not in text.keys():
                return "Formatting error.", 400
            features = nlp.extract_features(text['text'], dependencies, verbs_to_ignore)
            to_return.append({'id': text['id'], 'features': features})

        return json.dumps(to_return, indent=4)
    
    @app.route('/extract-features-aux', methods=['POST'])
    def get_features_without_sentence_id():
        data = None
        ignore_verbs = 'ignore-verbs' in request.json.keys()
        received_dependencies = 'dependencies' in request.json.keys()
        if 'text' not in request.json.keys():
            return "Lacking textual data in proper tag.", 400
        try:
            data = request.get_json()
        except BadRequest:
            return "Input data has a formatting error.", 400
        
        try:
            verbs_to_ignore = []
            if 'ignore-verbs' in data: 
                verbs_to_ignore = data['ignore-verbs'] if ignore_verbs else []
            dependencies = ['dobj', 'advcl', 'appos', 'ROOT']
            if 'dependencies' in data:
                dependencies = data['dependencies'] if received_dependencies else ['dobj', 'advcl', 'appos', 'ROOT']
            if 'text' in data: 
                features = nlp.extract_features(data['text'], dependencies, verbs_to_ignore)
                print(features)
                return json.dumps(features, indent=4)
            else: 
                return "Input data has a formatting error.", 400
        except Exception as e:
            return json.dumps([], indent=4)

    @app.route('/review-extraction', methods=['POST'])
    def process_reviews():
        min_subj = request.json['minSubj'] if 'minSubj' in request.json.keys() else 0
        max_subj = request.json['maxSubj'] if 'maxSubj' in request.json.keys() else 1
        min_pol = request.json['minPol'] if 'minPol' in request.json.keys() else -1
        max_pol = request.json['maxPol'] if 'maxPol' in request.json.keys() else 1

        if 'text' not in request.json.keys():
            return "Lacking textual data in proper tag.", 400

        ignore_verbs = 'ignore-verbs' in request.json.keys()
        received_dependencies = 'dependencies' in request.json.keys()

        verbs_to_ignore = request.json['ignore-verbs'] if ignore_verbs else []

        dependencies = request.json['dependencies'] if received_dependencies else ['dobj', 'advcl', 'appos', 'ROOT']

        reviews = request.json['text']

        to_return = []

        for review in reviews:
            pol, subj = nlp.analyze_sentiment(review['text'])
            if min_pol <= pol <= max_pol and min_subj <= subj <= max_subj:
                features = nlp.extract_features(review['text'], dependencies, verbs_to_ignore)
                to_return.append({'id': review['id'], 'features': features})

        return to_return

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host='0.0.0.0', port = '5000')
