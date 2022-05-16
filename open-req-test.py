import json

import requests

with open("info.json", 'r', encoding='utf-8') as file:
    nlp_data = json.load(file)

requirements_list = []

for i, element in enumerate(nlp_data):
    temp_dict = {}
    if element['app_name'] is not None:
        temp_dict['description'] = element['description']
        temp_dict['id'] = f'app {i}'
        temp_dict['title'] = element['app_name']
        requirements_list.append(temp_dict)

formatted_info = {
    "requirements": requirements_list
}
headers = {
    'content-type': 'application/json'
}

one_app_test = {
    'requirements': [
        {'description': nlp_data[0]['description'],
         'id': 'osmand-1',
         'title': nlp_data[0]['app_name']
         }
    ]
}
app_test = json.dumps(one_app_test)
one_app_res = requests.post('http://localhost:9406/keywords-extraction/requirements?stemmer=false', data=app_test, headers=headers)

one_app_results = json.loads(one_app_res.text)

info = json.dumps(formatted_info)
res = requests.post('http://localhost:9406/keywords-extraction/requirements?stemmer=false', data=info, headers=headers)
temp = json.loads(res.text)
print(temp)
