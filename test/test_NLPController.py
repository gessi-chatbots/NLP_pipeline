import json
from unittest.mock import MagicMock

import pytest as pytest

from NLPController import create_app, nlp

test_default_dependencies = ['dobj', 'advcl', 'appos', 'ROOT']

test_dependencies = ["dep1", "dep2"]

test_textual_data = "some text"

test_ignore_verbs = ["verb-to-ignore-in-infitive-form1", "verb-to-ignore-in-infitive-form1"]

test_complete_data = {
    "text":
        [
            {
                "id": "some id",
                "text": test_textual_data
            }
        ],
    "ignore-verbs":
        test_ignore_verbs,
    "dependencies":
        test_dependencies
}

test_no_dep_data = {
    "text":
        [
            {
                "id": "some id",
                "text": test_textual_data
            }
        ],
    "ignore-verbs":
        test_ignore_verbs
}

expected_mock_result = [{"id": "some id", "features": ["feature1", "feature2"]}]

nlp.extract_features = MagicMock(return_value=["feature1", "feature2"])


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_extract_features_all_info(app, client):
    response = client.post("/extract-features", json=test_complete_data)
    assert response.status_code == 200 and json.loads(response.text) == expected_mock_result
    nlp.extract_features.assert_called_with(test_textual_data, test_dependencies, test_ignore_verbs)


def test_extract_features_missing_dep(app, client):
    response = client.post("/extract-features", json=test_no_dep_data)
    assert response.status_code == 200 and json.loads(response.text) == expected_mock_result
    nlp.extract_features.assert_called_with(test_textual_data, test_default_dependencies, test_ignore_verbs)


def test_extract_features_bad_req(app, client):
    response = client.post("/extract-features", json={'not': 'good'})
    assert response.status_code == 400 and "Lacking textual data in proper tag" in response.text


def test_extract_features_bad_text_keys(app, client):
    response = client.post("/extract-features", json={'text': 'bad'})
    assert response.status_code == 400 and "Formatting error" in response.text


min_pol = -0.5
max_pol = 0.5
min_subj = 0.1
max_subj = 0.7
nlp.analyze_sentiment = MagicMock(return_value=(0, 0.3))

test_review_complete_data = {
    "text":
        [
            {
                "id": "some id",
                "text": test_textual_data
            }
        ],
    "ignore-verbs":
        test_ignore_verbs,
    "dependencies":
        test_dependencies,
    "minSubj": min_subj,
    "maxSubj": max_subj,
    "minPol": min_pol,
    "maxPol": max_pol,
}


def test_process_reviews_all_ok(app, client):
    response = client.post("/review-extraction", json=test_review_complete_data)
    assert response.status_code == 200 and json.loads(response.text) == expected_mock_result
    nlp.extract_features.assert_called_with(test_textual_data, test_dependencies, test_ignore_verbs)
    nlp.analyze_sentiment.assert_called_with(test_textual_data)
