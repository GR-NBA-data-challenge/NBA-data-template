import os
import datetime
import argparse
import requests
import urllib.parse
import sys
import re
import traceback

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

def checkStatus(response):
    if response.status_code < 200 or response.status_code > 299:
        raise Exception(f'Could not obtain season data for season {season}. Server responded with status code {response.status_code}')

class NbaDataLoader:
    def __init__(self):
        pass

    # Obtain the games of a season.
    # Seasons are strings such as '2009' or '2010POST'
    # The earliest available season is '2009'
    def getSeason(self, season: str):
        r = requests.get(f'https://{env}api.nbadatachallenge.com/data/seasons/{urllib.parse.quote(season)}')
        checkStatus(r)
        data = r.json()
        result = []
        for d in data:
            dateTime = d['dateTime']
            if dateTime < args.cutoff:
                result.append(d)
        return result
    
    # Obtain a single game data
    # The gameId is a numerical game identifier.
    # You can find the gameId from the results of getSeason
    def getGame(self, gameId: int):
        r = requests.get(f'https://{env}api.nbadatachallenge.com/data/games/{urllib.parse.quote(gameId)}')
        checkStatus(r)
        data = r.json()
        if data['dateTime'] < args.cutoff:
            return data
        else:
            return None
    
    # Obtain full player data about all the games in a season.
    def getPlayers(self, season: str):
        r = requests.get(f'https://{env}api.nbadatachallenge.com/data/gameplayersfull/{urllib.parse.quote(season)}')
        checkStatus(r)
        data = r.json()
        result = []
        for d in data:
            dateTime = d['dateTime']
            if dateTime < args.cutoff:
                result.append(d)
        return result

def loadPredictions():
    r = requests.get(f'https://{env}api.nbadatachallenge.com/data/predictions/{urllib.parse.quote(args.cutoff)}')
    checkStatus(r)
    return r.json()

def log(msg):
    print(f'{datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()} {msg}')

def findByGameId(results, gameId):
    for r in results:
        if r['gameId'] == gameId:
            return r
    return None

def getField(doc, field):
    if doc is None:
        return 'None'
    if field in doc:
        return doc[field]
    else:
        return 'None'

def computeSum(a, b):
    if a is None or b is None:
        return None
    return a + b

def computeDiff(a, b):
    if a is None or b is None:
        return None
    return a - b

def displayPredictionsAndResults(results, actual):
    for game in actual:
        gameId = game['gameId']
        resultGame = findByGameId(results, gameId)
        homeScore = getField(game, 'homeScore')
        awayScore = getField(game, 'awayScore')
        actualSum = computeSum(homeScore, awayScore)
        actualDiff = computeDiff(homeScore, awayScore)
        sumPredicted = getField(resultGame, 'sum')
        awayPredicted = getField(resultGame, 'diff')
        log(f'Game {gameId}. Actual results: home {homeScore} - away {awayScore}. Actual: sum {actualSum} - diff {actualDiff}. Predicted results: sum {sumPredicted} - diff {awayPredicted}')

def sanitizeResult(results, predictions):
    if len(results) != len(predictions):
        raise Exception(f'User returned {len(results)} predictions, but expecting {len(predictions)} predictions')
    sanitized = []
    for result in results:
        if not isinstance(result['gameId'], int):
            raise Exception(f'gameId field in the prediction must be an int')
        if not isinstance(result['sum'], int):
            raise Exception(f'sum field in the prediction must be an int')
        if not isinstance(result['diff'], int):
            raise Exception(f'diff field in the prediction must be an int')
        sanitized.append({
            'gameId': result['gameId'],
            'sum': result['sum'],
            'diff': result['diff']
        })
    return sanitized

def entry():
    try:
        if not re.match('^\d\d\d\d-\d\d-\d\d$', args.cutoff):
            log(f'--cutoff argument value is not valid. Expected a YYYY-MM-DD format')
            return

        log(f'Loading prediction matches starting from {args.cutoff}')
        predictionsFull = loadPredictions()
        predictions = []
        for prediction in predictionsFull:
            predictions.append({
                'date': prediction['date'],
                'homeTeam': prediction['homeTeam'],
                'awayTeam': prediction['awayTeam'],
                'gameId': prediction['gameId']
            })

        log('Loading user defined predict module')
        import main
        log('User defined predict module loaded')

        dataLoader = NbaDataLoader()

        log('Starting call to user defined function')
        result = main.predict(predictions, dataLoader, log)
        log('User defined function completed')
        result = sanitizeResult(result, predictionsFull)
        displayPredictionsAndResults(result, predictionsFull)

        # TODO write to file if specified
    except Exception:
        log(f'An error occurred: {traceback.format_exc()}')

entry()