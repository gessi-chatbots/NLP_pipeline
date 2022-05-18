import json
import re


def extract_keywords(filename: str):
    keywords = []
    with open(filename, 'r', encoding='utf-8') as file:
        regex = re.compile(r'(?<=").*(?=")')
        for line in file:
            kw = re.search(regex, line).group()
            keywords.append(kw)
    return keywords


glove_kw = extract_keywords('../OsmAnd-Glove.txt')
RAKE_kw = extract_keywords('../OsmAnd-RAKE.txt')

with open('results.json', 'r', encoding='utf-8') as file:
    app_chunks = json.load(file)

relevant_for_glove = []
relevant_for_RAKE = []
for chunk in app_chunks['OsmAnd — Maps & GPS Offline']:
    for kw in glove_kw:
        if kw in chunk:
            relevant_for_glove.append(chunk)
            break
    for kw in RAKE_kw:
        if kw in chunk:
            relevant_for_RAKE.append(chunk)
            break

print(relevant_for_glove)
print(relevant_for_RAKE)

