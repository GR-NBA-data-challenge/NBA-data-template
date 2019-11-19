# This is the main function you are requested to define.
# required_predictions: a list of matches that you should predict
# data_loader: a NbaDataLoader class instance.
#     Contains getSeason, getGame and getPlayers methods. Please refer to simulate.py for details about
#     the provided methods.
# (return): You should return, for each match requested in required_predictions, two numbers:
#     The difference between the scores: homeScore - awayScore
#     And the sum of the scores: homeScore - awayScore
def predict(required_predictions, data_loader):
    # Load games data for the 2011 season.
    # Seasons from 2009 onwards are available, including POST seasons, such as 2011POST
    games2011 = data_loader.getSeason('2011')
    print(f'Loaded {len(games2011)} 2011 games')
    print(f'First entry in 2011 season is\n{games2011.iloc[[0]]}')

    # Loading a season that is ahead of the cutoff training time returns no results.
    # In this case, the default cutoff time is in 2019, so loading 2020 data returns no results.
    # You can change the cutoff time by passing to simulate.py
    #     --cutoff YYYY-MM-DD
    games2020 = data_loader.getSeason('2020')
    print(f'Loaded {len(games2020)} 2020 games')

    # You can load an individual match's data
    aGame = data_loader.getGame(games2011.loc[100, 'gameId'])
    print(f'Game 100 in the 2011 database is\n{aGame}')

    # You can also load the full players data for an entire season
    full2011seasonPlayers = data_loader.getPlayers('2011')
    print(f'Loaded {len(full2011seasonPlayers)} 2011 season player rows')

    print(f'Required predictions are\n{required_predictions}')

    # You should fill in the sum and diff fields of the required predictions
    for index, match in required_predictions.iterrows():
        required_predictions.at[index, 'predictedSum'] = 999
        required_predictions.at[index, 'predictedDiff'] = 1
    print('finished')