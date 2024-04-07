## TransFeatEx tool

TransFeatEx is a feature extraction tool which combines consolidated syntactic and semantic feature extraction techniques with the use of a RoBERTa-based pre-trained model to automatically extract mobile app features from app-related textual documents.

## Description

The main goal of the TransFeatEx tool is to support researchers and developers in the development of projects, tools and processes which require from structured data concerning the set of features exposed by a catalogue of mobile applications. % published in mobile app stores or repositories. Without the need of annotated data, TransFeatEx leverages the accuracy of pre-trained transformer models to enrich the natural language texts received as input (such as descriptions or user-generated reviews) with linguistic annotations, and then uses such annotations to apply consolidated syntactic and semantic techniques in order to extract features from said texts. 
TransFeatEx includes customization capabilities to fine-tune feature detection tasks (e.g., POS patterns, syntactic dependency patterns) to allow for domain and context adaptation of the feature extraction process. 

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


## How to install & deploy

### In local machine

1. Clone project
2. Install the required packages outlined in "requirements.txt"
3.  Run NLPController by executing the following command:
```console
python NLPController.py
```
4. Install spaCy model 'en_core_web_trf'
```console
python -m spacy download en_core_web_trf
```
5. The service will be available at port 5000.

### In Docker container

1. Clone project
2. Make sure Docker is installed in the system.
3. Navigate to the project folder and run the following command:
```console
docker build -t {image-name} .
```
4. Once the image is built, run the following command:
```console
docker run -d -p 5000:5000 {image-name}
```
5. The service will be available at port 5000.

## How to use

### Direct feature extraction
1. Send POST request to http://{your-ip}:5000/extract-features with the payload described below.
2. Receive the results in a JSON array.

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

### Playground

1. Run the feature_visualization.py script found in visualizationtools folder.

```console
python feature_visualization.py -f source_file -c config_file
```
2. Refer to the sample input files in the folder to see the expected data format.

## How to deploy
1. 
    `docker build -t transfeatex:latest .`
2. 
    `docker run -d --name TransFeatEx -p 3004:3004 transfeatex:latest`


## Process diagram

![NLP Pipeline process diagram](https://github.com/gessi-chatbots/NLP_pipeline/blob/master/nlp_service_diagram.png?raw=true)

## License

Free use of this software is granted under the terms of the GNU General Public License v3.0: https://www.gnu.org/licenses/gpl.html
