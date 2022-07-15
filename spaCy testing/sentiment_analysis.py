import json

import matplotlib.pyplot as pt
import spacy

import utils

# loading reviews
with open("nlp.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

reviews = []
aux = data[0]['reviews']
for review in aux:
    reviews.append(review['review'])

evaluations = {}
pol = []
sub = []

# perform sentiment analysis
for i, review in enumerate(reviews):
    result = utils.analyze_sentiment(review)
    pol.append(result[0])
    sub.append(result[1])
    evaluations[review] = {'polarity': result[0], 'subjectivity': result[1]}

#show the distribution of polarities
pt.hist(pol)
pt.show()

mean = sum(pol) / len(pol)

# to play with upper and lower bounds, edit these values
upper = 0.2
lower = -0.2

# selecting reviews whose polarity falls between the defined upper and lower bounds
final_list = [x for x in evaluations.keys() if lower < evaluations[x]['polarity'] < upper]
nlp = spacy.load("en_core_web_trf")
feature_list = []
reviews_features = {}

# extract features from relevant reviews
for review in final_list:
    features = utils.extract_features(review, ['dobj', 'advcl'], nlp)
    reviews_features[review] = features
    feature_list = [*feature_list, *features]

with open("extracted_reviews.json", 'w', encoding='utf-8') as file:
    print(json.dumps(reviews_features, indent=4),file=file)
    print("Complete feature list:\n")
    print(json.dumps(feature_list, indent=4), file=file)


# interesting reviews
max_pol_i = pol.index(max(pol))
min_pol_i = pol.index(min(pol))

max_sub_i = sub.index(max(sub))
min_sub_i = sub.index(min(sub))

av_pol = sum(pol) / len(pol)
av_sub = sum(sub) / len(sub)

aux = [abs(x - av_pol) for x in pol]
ind = min(aux)
av_pol_i = aux.index(min(aux))
aux = [abs(x - av_sub) for x in sub]
av_sub_i = aux.index(min(aux))

extreme_reviews = {'most_positive': reviews[max_pol_i], 'most_negative': reviews[min_pol_i],
                   'most_subjective': reviews[max_sub_i], 'least_subjective': reviews[min_sub_i],
                   'average_pol': reviews[av_pol_i], 'average_sub': reviews[av_sub_i]}

# print results
with open('sentiment_analysis_results.json', 'w', encoding='utf-8') as file:
    to_print = json.dumps(evaluations, indent=4)
    print(to_print, file=file)

with open('interesting_reviews.json', 'w', encoding='utf-8') as file:
    to_print = json.dumps(extreme_reviews, indent=4)
    print(to_print, file=file)
