# This is the main function you are requested to define.
# required_predictions: a list of matches that you should predict
# data_loader: a NbaDataLoader class instance.
#     Contains getSeason, getGame and getPlayers methods. Please refer to simulate.py for details about
#     the provided methods.
# log: you can call log('message') to log any information you want. These messages are automatically
#     printed to console, and to the logfiles when running on the server side.
#     All logs sent to this logger can be retrieved from our servers (up to a maximum size), so
#     use this to debug issues when running your code in our simulations.
# (return): You should return, for each match requested in required_predictions, two numbers:
#     The difference between the scores: homeScore - awayScore
#     And the sum of the scores: homeScore - awayScore
def predict(required_predictions, data_loader, log):
    # Load games data for the 2010 season.
    # Seasons from 2009 onwards are available, including POST seasons, such as 2010POST
    games2010 = data_loader.getSeason('2010')
    log(f'Loaded {len(games2010)} 2010 games')
    log(f'First entry in 2010 season is {games2010[0]}')

    # Loading a season that is ahead of the cutoff training time returns no results.
    # In this case, the default cutoff time is in 2019, so loading 2020 data returns no results.
    # You can change the cutoff time by passing to simulate.py
    #     --cutoff YYYY-MM-DD
    games2020 = data_loader.getSeason('2020')
    log(f'Loaded {len(games2020)} 2019 games')

    # You can load an individual match's data
    aGame = data_loader.getGame(games2010[100]['gameId'])
    log(f'Game 100 in the 2010 database is {aGame}')

    # You can also load the full players data for an entire season
    full2010seasonPlayers = data_loader.getPlayers('2010')
    log(f'Loaded {len(full2010seasonPlayers)} 2010 season player rows')

    result = []
    for match in required_predictions:
        result.append({
            'gameId': match['gameId'],
            'sum': 999,
            'diff': 1
        })
    log('finished')
    return result