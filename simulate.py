import os
import datetime

def log(msg):
    print(f'{datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()} {msg}')

def historical_data():
    log('Requested historical data')

def current_season_matches():
    log('Requested current season matches')

def entry():
    try:
        log('Loading user defined predict module')
        from src import main
        log('User defined predict module loaded')
        required_predictions = [
            {'teamA': 'teamA', 'teamB': 'teamB'},
            {'teamA': 'teamC', 'teamB': 'teamD'}
        ]
        log('Starting call to user defined function')
        result = main.predict(required_predictions, historical_data, current_season_matches, log)
        log('User defined function completed')
        log(f'User returned: {result}')
    except Exception as e:
        log(f'{e}')

entry()