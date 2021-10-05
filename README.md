## The Gerousia Bot
### Purpose:
To provide a Telegram bot that inform members of the
Gerousia chat group which members are online in their
Discord server.

### Requirements:
- Python 3+
- pipenv

### Running locally
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
cd gerousiabot
```
4. Install the project's dependencies via pipenv
```
pipenv install
```
5. Start the environment
```
pipenv shell
```
5.5 Verify the environment is using Python 3 (Option)
```
python --version // Python 3.X.X
```
6. Run the application
```
python gerousiabot/main.py
```

### Testing
This project also has unit tests. To run the unit tests
run the following command.
```
python -m pytest tests
```

