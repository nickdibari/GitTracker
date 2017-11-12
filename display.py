import csv

from models import Dev

# Import the configuration settings for the script
# TODO: Maybe handle this in a more efficient way?
# TODO: Add hashing for password so it's not stored in plaintext
try:
    from config import (
        RECORDS_FILENAME
    )
except ImportError:
    print('No config file set!')
    print('Read the README for details on how to setup the config file')
    exit(1)


def main():
    # Open leaderboard data from CSV file
    devs = {}
    with open(RECORDS_FILENAME, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            avatar = row['Avatar']
            commits = row['Commits']

            devs[avatar] = commits

    # Sort leaderboard by commits
    devs = sorted(devs.iteritems(), key=lambda (k,v): (v,k), reverse=True)
    
    # Display records
    print('Username | Commits')
    for name, commits in devs:
        print('{} | {}'.format(name, commits))


if __name__ == '__main__':
    main()
