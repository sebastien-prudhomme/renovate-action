FROM python:3.9.0

COPY . /tests
WORKDIR /tests

RUN pip install -r requirements.txt
