# Nicholas DiBari
# github.py
# Script to gather commit data from a specified Github repository
import json
from datetime import datetime, timedelta

import requests

from models import Dev

# Import the configuration settings for the script
# TODO: Maybe handle this in a more efficient way?
# TODO: Add hashing for password so it's not stored in plaintext
try:
    from config import (
        GITHUB_REPO,
        GITHUB_USERNAME,
        GITHUB_PASSWORD,
        CACHE_FILENAME
    )
except ImportError:
    print('No config file set!')
    print('Read the README for details on how to setup the config file')
    exit(1)


GITHUB_URL = 'https://api.github.com/{}'


def main():
    # Prepare data to send
    # Get modified_since header to send in request
    modified_since = datetime.utcnow() - timedelta(minutes=15)
    modified_since_header = modified_since.strftime('%a, %d %b %Y %H:%M:%S GMT')

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
            username = record['commit']['author']['name']

            if not devs.get(username):
                avatar_url = record['author']['avatar_url']
                dev = Dev(username, avatar_url)
                devs[username] = dev

            else:
                devs[username].commits += 1

        print(devs)

    except requests.exceptions.ConnectionError as conn_error:
        error_type = type(conn_error[0])
        url = conn_error[0].url

        print('Caught a ConnectionError: {}').format(error_type)
        print('Trying to get URL: {}'.format(url))


if __name__ == '__main__':
    main()
