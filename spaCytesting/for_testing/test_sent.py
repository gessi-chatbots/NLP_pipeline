import json

import spacy
import spaCytesting.utils as utils
import matplotlib.pyplot as pt

with open("sentiment_analysis_results.json", 'r', encoding='utf-8') as temp_file:
    evaluated_reviews = json.load(temp_file)

temp_pol_res = [evaluated_reviews[x]['polarity'] for x in evaluated_reviews.keys()]
pt.hist(temp_pol_res)
pt.show()

upper = 0.2
lower = -0.2

final_list = [x for x in evaluated_reviews.keys() if lower < evaluated_reviews[x]['polarity'] < upper]
nlp = spacy.load("en_core_web_trf")
feature_list = []
reviews_features = {}

# extract features from relevant reviews
for review in final_list:
    features = utils.extract_features(review, ['dobj', 'advcl'], nlp)
    reviews_features[review] = features
    feature_list = [*feature_list, *features]

with open("extracted_reviews.json", 'w', encoding='utf-8') as file:
    print(json.dumps(reviews_features, indent=4), file=file)
    print("Complete feature list:\n")
    print(json.dumps(feature_list, indent=4), file=file)
