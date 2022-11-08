FROM python:3.8.15-slim-buster

ADD ./* /service/

WORKDIR /service

RUN pip install -U setuptools

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_trf

ENTRYPOINT [ "python" ]

CMD ["NLPController.py" ]
