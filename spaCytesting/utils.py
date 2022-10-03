import json

import spacy
import numpy
from spacy import Language
from spacytextblob.spacytextblob import SpacyTextBlob
from sentence_transformers import SentenceTransformer
from numpy import dot, linalg


def cosine_similarity(sentence1, sentence2) -> float:
    numerator = numpy.dot(sentence1, sentence2)
    denominator = numpy.linalg.norm(sentence1) * numpy.linalg.norm(sentence2)
    return numerator / denominator


def analyze_sentiment(text: str) -> tuple:
    nlp = spacy.load("en_core_web_md")
    nlp.add_pipe('spacytextblob')
    doc = nlp(text)
    polarity = doc._.blob.polarity
    subjectivity = doc._.blob.subjectivity
    return polarity, subjectivity


def extract_features(text: str, relevant_dependencies: list, nlp_pipeline: Language) -> list:
    document = nlp_pipeline(text)
    features = []
    for syntactic_dependency in relevant_dependencies:
        for chunk in document.noun_chunks:
            if chunk.root.dep_ in syntactic_dependency:
                features.append(f'{chunk.root.head.text.lower()} {chunk.text.lower()}')

    return features


def get_string_matchings(extracted_features, expected_output):
    true_positives = []
    for feature in extracted_features:
        for expected in expected_output:
            if expected in feature or feature in expected:
                true_positives.append(feature)
    return true_positives


def get_synonyms(extracted_features, expected_output, threshold=0.8):
    sentence_embedding_generator = SentenceTransformer('distiluse-base-multilingual-cased')
    true_positives = []
    synonyms = {}
    extracted_features_embeddings = [sentence_embedding_generator.encode(feature) for feature in extracted_features]
    expected_output_embeddings = [sentence_embedding_generator.encode(output) for output in expected_output]
    for i, feature_embedding in enumerate(extracted_features_embeddings):
        current_feature_synonyms = []
        for j, expected_embedding, in enumerate(expected_output_embeddings):
            similarity = cosine_similarity(feature_embedding, expected_embedding)
            if similarity >= threshold:
                if extracted_features[i] not in true_positives:
                    true_positives.append(extracted_features[i])
                current_feature_synonyms.append(expected_output[j])
                # break
        synonyms[extracted_features[i]] = current_feature_synonyms

    return true_positives, synonyms


def assess_quality(extracted_features: list, expected_output: list, comparison_type='manual', threshold=0.8):
    if comparison_type not in ['manual', 'similarity']:
        raise Exception
    true_positives = []
    synonyms = {}
    if comparison_type == 'manual':
        true_positives = get_string_matchings(extracted_features, expected_output)
    else:
        true_positives, synonyms = get_synonyms(extracted_features, expected_output, threshold)

    precision = round(len(true_positives) / len(extracted_features), 3)
    recall = round(len(true_positives) / len(expected_output), 3)
    if precision + recall == 0:
        f_score = 0
    else:
        f_score = round(2 * (precision * recall) / (precision + recall), 3)
    metrics = {
        'precision': precision,
        'recall': recall,
        'f_score': f_score
    }
    return metrics, true_positives, synonyms