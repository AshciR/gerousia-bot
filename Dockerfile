# We're using Python 3.10 running on the Alpine Linux distribution
FROM python:3.10-alpine

# Copy the required files into the docker image
RUN mkdir /bot
COPY src/gerousiabot /bot/gerousiabot
COPY Pipfile* /bot/
COPY .env /bot

# Use this path (that contains the Dockerfile) as the working dir
WORKDIR /bot

# Install the pipenv package and its dependencies
RUN pip install pipenv
RUN pipenv install

ENTRYPOINT ["pipenv", "run", "python", "gerousiabot/main.py"]
