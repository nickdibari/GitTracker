import csv

from flask import Flask, render_template

# Import the configuration settings for the script
# TODO: Maybe handle this in a more efficient way?
# TODO: Add hashing for password so it's not stored in plaintext
try:
    from config import (
        GITHUB_REPO,
        RECORDS_FILENAME
    )
except ImportError:
    print('No config file set!')
    print('Read the README for details on how to setup the config file')
    exit(1)

app = Flask(__name__, template_folder='assets/templates')


@app.route('/')
def index():
    devs = []

    # Read leaderboard data from CSV file
    with open(RECORDS_FILENAME, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            data = {
                'avatar': row['Avatar'],
                'commits': row['Commits']
            }
            devs.append(data)

    # Sort dev list
    devs = sorted(devs, key=lambda x: x['commits'], reverse=True)
    return render_template(
        'display.html',
        devs=devs
    )


if __name__ == '__main__':
    app.run(debug=True)
