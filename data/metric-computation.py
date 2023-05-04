import argparse
import csv
import json
import sys
from collections import OrderedDict
from json import JSONDecodeError

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

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', required=True, help="The file to be analyzed.")
# ap.add_argument('-o', '--output', required=False, help="File with the customization parameters.")

args = vars(ap.parse_args())

source_file = args['file']
try:
    with open(source_file, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except JSONDecodeError:
            sys.exit("Input file is not a valid JSON file.")
except FileNotFoundError:
    sys.exit("Specified file not found.")

metrics['apps'] = len(data)
histogram = {}

for app in data:

    if app['features'] is None:
        histogram[0] += 1
    elif len(app['features']) in histogram:
        histogram[len(app['features'])] += 1
    else:
        histogram[len(app['features'])] = 1

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
    tabs = int(len(metric) / 4)
    tabs = '\t' * (7 - tabs)
    print(f'{metric}{tabs}{metrics[metric]}')

histogram = OrderedDict(sorted(histogram.items()))


report_file_name = f'{source_file.split(".")[0]}-report.csv'

with open(report_file_name, 'w', encoding='utf-8') as file:
    w = csv.DictWriter(file, metrics.keys())
    w.writeheader()
    w.writerow(metrics)

histogram_file_name = f'{source_file.split(".")[0]}-histogram.csv'
with open(histogram_file_name, 'w', encoding='utf-8') as file:
    w = csv.DictWriter(file, histogram.keys())
    w.writeheader()
    w.writerow(histogram)
