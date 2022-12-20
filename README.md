## Feature extraction service

NLP service that, given a text about an app, extracts the features of the app mentioned.

## Description

This service exposes a NLP component that extracts features from natural language text related to a mobile app.


## File structure

- \root
  - NLPController.py: Main entry point for the service.
- \NLPService
  - NLPUtils.py: Class that contains the logic for feature extraction
  - PipelineBuilder.py: Class to build a custom NLP Spacy pipeline

## Used technologies

| Component | Description   | Version |
|-----------|---------------|---------|
| Spacy     | NLP Library   | 3.2.4   |
| Flask     | Web framework | 2.2.2   |


## How to install

1. Clone project
2. Install the required packages outlined in "requirements.txt"
3. Enjoy!

## How to use

1. Run NLPController
2. Send POST request to http://{your-ip}/extract:5000 with the payload described below.
3. Receive the results in a JSON array.

Sample payload

```json
{
  "text":
        ["some text", "some other text"],
  "ignore-verbs":
        ["verb-to-ignore-in-infitive-form1", "verb-to-ignore-in-infitive-form1"]
}
```
## Process diagram

![NLP Pipeline process diagram](https://github.com/gessi-chatbots/NLP_pipeline/blob/master/nlp_service_diagram.png?raw=true)

## License

Free use of this software is granted under the terms of the GNU General Public License v3.0: https://www.gnu.org/licenses/gpl.html
