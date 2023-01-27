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

### Direct feature extraction
1. Run NLPController
2. Send POST request to http://{your-ip}:5000/extract-features with the payload described below.
3. Receive the results in a JSON array.

Sample payload

```json
{
  "text":
        [
          {
            "id": "some id",
            "text":  "some text"
          }
        ],
  "ignore-verbs":
        ["verb-to-ignore-in-infitive-form1", "verb-to-ignore-in-infitive-form1"],
  "dependencies":
        ["spacy-dep1", "spacy-dep2"]
}
```
### Sentiment analysis filtering feature extraction

1. Run NLPController
2. Send POST request to http://{your-ip}:5000/review-extraction with the same payload as above.
3. Provide the polarity and subjectiviy thresholds you are interested in.
4. Receive the results in a JSON array.

As previously stated, the payload is the same, but you can include subjectivity and polarity thresholds:
- Subjectivity measures how objective is a text; the higher the score, the less objective.
- Polarity measures if the text shows a positive or negative sentiment.

To define these thresholds, you can include the following parameters in the request body:
- maxSubj: Maximum subjectivity the text can have (max allowed value: 1).
- minSubj: Minimum subjectivity the text can have (min allowed value: 0).
- minPol: Minimum polarity the text can have (min allowed value: -1).
- maxPol: Maximum polarity the text can have (max allowed value: 1).

Note: If you don't include a parameter, it defaults to the highest or lowest value available.

## Process diagram

![NLP Pipeline process diagram](https://github.com/gessi-chatbots/NLP_pipeline/blob/master/nlp_service_diagram.png?raw=true)

## License

Free use of this software is granted under the terms of the GNU General Public License v3.0: https://www.gnu.org/licenses/gpl.html
