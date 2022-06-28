import json

import utils

with open("nlp.json",'r',encoding='utf-8') as file:
    data = json.load(file)

reviews = []
aux = data[0]['reviews']
for review in aux:
    reviews.append(review['review'])

evaluations = {}
for review in reviews[:20]:
    result = utils.analyze_sentiment(review)
    evaluations[review] =  result

with open('sentiment_analysis_results.json', 'w', encoding='utf-8') as file:
    to_print = json.dumps(evaluations,indent=4)
    print(to_print,file=file)