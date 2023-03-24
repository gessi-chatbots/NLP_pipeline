import json

metrics = {
    'summaries': 0,
    'apps': 0,
    'descriptions': 0,
    'changelogs': 0,
    'reviews': 0,
    'avg-reviews': 0,
    'features': 0,
    'apps-with-features': 0,
    'avg-features-app': 0
}

with open('merged-apps-with-categories.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

metrics['apps'] = len(data)

for app in data:
    metrics['summaries'] = metrics['summaries'] + ('summary' in app.keys())
    metrics['descriptions'] = metrics['descriptions'] + ('description' in app.keys())
    metrics['changelogs'] = metrics['changelogs'] + ('changelog' in app.keys())
    metrics['reviews'] = metrics['reviews'] + len(app['reviews']) if 'reviews' in app.keys() and app['reviews'] else 0
    metrics['features'] = metrics['features'] + \
        (len(app['features']) if 'features' in app.keys() and app['features'] else 0)
    if 'features' in app.keys() and app['features']:
        metrics['apps-with-features'] = metrics['apps-with-features'] + (len(app['features']) > 0)

metrics['avg-features-app'] = metrics['features'] / metrics['apps-with-features']
metrics['avg-reviews'] = metrics['reviews'] / metrics['apps']

for metric in metrics.keys():
    # print(len(metric))
    tabs = int(len(metric)/4)
    # print(tabs)
    tabs = '\t'*(7-tabs)
    print(f'{metric}{tabs}{metrics[metric]}')
