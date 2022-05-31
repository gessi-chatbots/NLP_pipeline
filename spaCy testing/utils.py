import spacy
from spacy import Language


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
    nlp_pipeline = spacy.load('en_core_web_md')
    true_positives = []
    extracted_features_embeddings = [nlp_pipeline(sent) for sent in extracted_features]
    expected_output_embeddings = [nlp_pipeline(sent) for sent in expected_output]
    for i, feature_embedding in enumerate(extracted_features_embeddings):
        for expected_embedding in expected_output_embeddings:
            similarity = feature_embedding.similarity(expected_embedding)
            if similarity >= threshold:
                true_positives.append(extracted_features[i])
                break
    return true_positives


def assess_quality(extracted_features: list, expected_output: list, comparison_type='manual', threshold=0.8):
    if comparison_type not in ['manual', 'similarity']:
        raise Exception
    true_positives = []
    if comparison_type == 'manual':
        true_positives = get_string_matchings(extracted_features, expected_output)
    else:
        true_positives = get_synonyms(extracted_features, expected_output, threshold)

    precision = round(len(true_positives) / len(extracted_features), 3)
    recall = round(len(true_positives) / len(expected_output), 3)
    if precision + recall == 0:
        f_score = 0
    else:
        f_score = round(2 * (precision * recall) / (precision + recall), 3)
    metrics = (precision, recall, f_score)
    return metrics, true_positives
