import os
import datetime
import argparse
import requests
import urllib.parse
import sys

parser = argparse.ArgumentParser()

parser.add_argument('--cutoff', help='A datestring in format YYYY-MM-DD. The end of the training daterange, and the start of the week to be predicted. All data after the cutoff is automatically removed to avoid look-ahead', default='2019-01-01')

# Hidden argument to switch to the dev server
parser.add_argument('--dev', help=argparse.SUPPRESS, action="store_true")

# Hidden argument to change the path in which to look the user code.
# It is relative to the current file.
parser.add_argument('--userpath', help=argparse.SUPPRESS, default='src')

args = parser.parse_args()

env = 'dev' if args.dev else 'prod'

currdir = os.path.abspath(os.path.dirname(__file__))

userpath = os.path.abspath(os.path.join(currdir, args.userpath))

sys.path.append(userpath)

class NbaDataLoader:
    def __init__(self):
        pass

    # TODO Handle data cutoff to prevent lookahead

    # Obtain the games of a season.
    # Seasons are strings such as '2009' or '2010POST'
    # The earliest available season is '2009'
    def getSeason(self, season: str):
        r = requests.get(f'https://{env}api.nbadatachallenge.com/data/seasons/{urllib.parse.quote(season)}')
        self._checkStatus(r)
        return r.json()
    
    # Obtain a single game data
    # The gameId is a numerical game identifier.
    # You can find the gameId from the results of getSeason
    def getGame(self, gameId: int):
        r = requests.get(f'https://{env}api.nbadatachallenge.com/data/games/{urllib.parse.quote(gameId)}')
        self._checkStatus(r)
        return r.json()
    
    # Obtain full player data about all the games in a season.
    def getPlayers(self, season: str):
        r = requests.get(f'https://{env}api.nbadatachallenge.com/data/gameplayersfull/{urllib.parse.quote(season)}')
        self._checkStatus(r)
        return r.json()

    # ----- Private methods below -----

    def _checkStatus(self, response):
        if response.status_code < 200 or response.status_code > 299:
            raise Exception(f'Could not obtain season data for season {season}. Server responded with status code {response.status_code}')

def log(msg):
    print(f'{datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()} {msg}')

def entry():
    try:
        log('Loading user defined predict module')
        import main
        log('User defined predict module loaded')
        required_predictions = [
            {'teamA': 'teamA', 'teamB': 'teamB'},
            {'teamA': 'teamC', 'teamB': 'teamD'}
        ]

        dataLoader = NbaDataLoader()

        log('Starting call to user defined function')
        result = main.predict(required_predictions, dataLoader, log)
        log('User defined function completed')
        log(f'User returned: {result}')
    except Exception as e:
        log(f'{e}')

entry()