## The Gerousia Bot

### Purpose:

To provide a Telegram bot that inform members of the Gerousia chat group which members are online in their Discord
server.

### Requirements:

- Python 3+
- pipenv

### Configure the project locally

1. Install the pipenv package and its dependencies (if you don't already have it)

```
pip install pipenv
```

2. Clone the project

```
git clone https://github.com/AshciR/gerousia-bot.git
```

3. Change directory to the folder

```
cd gerousia-bot/gerousiabot
```

4. Install the project's dependencies via pipenv

```
pipenv install
```

5. Create a `.env` file using the `.env.template`

```
cat .env.template > .env
```

> Get some real keys and populate your `.env` file.

### Running the project locally

You have a few ways to run the project

#### Interactively

1. Start the environment

> pipenv will automatically load your .env file

```
pipenv shell
```

2. Verify the environment is using Python 3 (Option)

```
python --version // Python 3.X.X
```

3. Run the application

``q`
python gerousiabot/main.py
```

#### Non-Interactively

1. Run the pipenv in the non-interactive mode

```
pipenv run python gerousiabot/main.py
```

#### Non-Interactively via Docker

0. Assumes that you have Docker installed on your machine

```
docker --version
```

1. Build the Docker image

```
docker build . -t <whatever-you-want-to-name-the-image>
```

2. Run the Docker container

```
docker run -d <whatever-you-want-to-name-the-image>
```

### Testing

This project also has unit tests. To run the unit tests run the following command.

```
python -m pytest tests
```

