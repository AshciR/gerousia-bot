# We're using Python 3.10 running on the Alpine Linux distribution
FROM python:3.10-alpine

# Use this path (that contains the Dockerfile) as the working dir
WORKDIR ./gerousiabot

# Copy the required files into the docker image
COPY ./gerousiabot ./gerousiabot
COPY Pipfile* .
COPY .env .

# Install the pipenv package and its dependencies
RUN pip install pipenv
RUN pipenv install

ENTRYPOINT ["pipenv", "run", "python", "gerousiabot/main.py"]
