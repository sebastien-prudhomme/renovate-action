FROM python:3.9.0

WORKDIR /tests

COPY requirements.txt ./
RUN pip install -r requirements.txt && \
    rm -f requirements.txt

USER nobody
CMD [ "pytest", "-p", "no:cacheprovider", "--verbose" ]
