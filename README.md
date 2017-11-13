# GitTracker

Flask application to display a leaderboard for a repository's contributors

## Setup

GitTracker requires a configuration file to set the repository to track, authentication
for the Github API, and to set the debug variable for the Flask app. To set this file,
create a file in the project directory named config.py. The following variables must
be set in the file:
```python
GITHUB_REPO = '{owner}/{repo_name}'
GITHUB_USERNAME = '{username}'
GITHUB_PASSWORD = '{password}'
DEBUG = {True/False}
```

## Running the application

1. Setup the virtual environment

    `virtualenv env`

    `source env/bin/activate`

2. Install the requirements

    `pip install -r requirements.txt`
3. Run the app

    `python app.py`

Navigate to 127.0.0.1:5000 to view the page