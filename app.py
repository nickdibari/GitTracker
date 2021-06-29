from datetime import datetime, timedelta
import json

from flask import Flask, render_template
import requests

# Import the configuration settings for the script
# TODO: Maybe handle this in a more efficient way?
# TODO: Add hashing for password so it's not stored in plaintext
try:
    from config import (
        GITHUB_REPO,
        GITHUB_USERNAME,
        GITHUB_PASSWORD,
        DEBUG
    )
except ImportError:
    print('No config file set!')
    print('Read the README for details on how to setup the config file')
    exit(1)

GITHUB_URL = 'https://api.github.com/{}'
CACHE_FILENAME = 'records.json'

app = Flask(__name__, template_folder='assets/templates')


def get_dev_stats():
    # Prepare data to send
    try:
        fp = open(CACHE_FILENAME, 'r')

        # Get modified_since header to send in request
        modified_since = datetime.utcnow() - timedelta(minutes=15)
        date_format = '%a, %d %b %Y %H:%M:%S GMT'
        modified_since_header = modified_since.strftime(date_format)

        fp.close()
    except IOError:
        # Results have not been cached yet, so retrieve API response
        modified_since_header = None

    headers = {
        'User-Agent': GITHUB_USERNAME,
        'Accept': 'application/vnd.github.v3+json',
        'If-Modified-Since': modified_since_header,
    }

    auth = (GITHUB_USERNAME, GITHUB_PASSWORD)

    endpoint = 'repos/{}/commits'.format(GITHUB_REPO)
    url = GITHUB_URL.format(endpoint)

    # Make request to Github API
    print('Making request to URL: {}'.format(url))

    try:
        resp = requests.get(url, headers=headers, auth=auth)
        resp.raise_for_status()

        print('Response Code: {}'.format(resp.status_code))

        # If contents have not been modified, read from cache
        if resp.status_code == 304:
            with open(CACHE_FILENAME, 'r') as json_file:
                records = json.load(json_file)

        # Else get records from API response and write to cache
        else:
            records = resp.json()

            with open(CACHE_FILENAME, 'w') as json_file:
                json.dump(records, json_file)

        # Parse response from Github API
        devs = {}

        for record in records:
            # Skip over commits that are just merge commits
            if 'Merge pull request' in record['commit']['message']:
                continue

            username = record['commit']['author']['name']

            if not devs.get(username):
                avatar_url = record['author']['avatar_url']
                devs[username] = {}
                devs[username]['login'] = username
                devs[username]['avatar'] = avatar_url
                devs[username]['commits'] = 1

            else:
                devs[username]['commits'] += 1

        return devs

    except requests.exceptions.ConnectionError as conn_error:
        error_type = conn_error
        url = conn_error.request.url

        print('Caught a ConnectionError: {}'.format(error_type))
        print('Trying to get URL: {}'.format(url))

        raise


@app.route('/')
def index():
    dev_table = get_dev_stats()

    # Sort devs by number of commits
    devs = sorted(dev_table.values(), key=lambda x: x['commits'], reverse=True)

    return render_template('display.html', devs=devs)


if __name__ == '__main__':
    app.run(debug=DEBUG)
