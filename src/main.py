import pandas as pd
import statsmodels.api as sm
import numpy as np
import math

def get_multi_season_game_data(data_loader, first_year, last_year):
    data = [pd.DataFrame(data_loader.getSeason(str(season))) for season in range(first_year, last_year + 1)]
    data = pd.concat(data, axis=0)
    data.dropna(axis=0, inplace=True)
    data.dateTime=pd.to_datetime(data.dateTime)
    data.sort_values('dateTime', inplace=True)
    data.reset_index(inplace=True, drop=True)
    return data


## Elo model's probability of home team winning
def home_win_probability(home_elo, away_elo):
    return 1 / (1 + math.pow(10, -(home_elo - away_elo) / 400))


## Get new Elo rating system home and away teams after a game
def get_updated_elo(
        home_elo, away_elo,
        home_victory,  ## 1 if home team won, 0 if away team won
        K,  ## model hyperparameter
):
    if home_victory not in [0, 1, False, True]:
        raise ValueError(f"home_victory should be 1 if home team won, 0 if away team won. Got {home_victory}")

    P_home_win = home_win_probability(home_elo, away_elo)
    P_away_win = 1 - P_home_win

    # When home team wins
    if home_victory:
        home_elo += K * P_away_win
        away_elo -= K * P_home_win

    # When away team wins
    else:
        home_elo -= K * P_away_win
        away_elo += K * P_home_win

    return home_elo, away_elo


## Iterate through games updating each teams Elo rating
def get_elos_over_time(data,  ## dataframe of games, must be in order of occurence
                       starting_elo_dict={},  ## dictionary of elo scores by team at the beginning of the data period
                       default_elo=0,  ## elo initally given to a team not in starting_elo_dict
                       K=10,  ## model hyperparameter; higher number means individuals game affects Elo more
                       ):
    elo_dict = starting_elo_dict.copy()
    data['homeElo'] = np.nan
    data['awayElo'] = np.nan

    ## Iterate over rows of the dataframe (i.e. over games)
    for i, row in data.iterrows():
        home_team = row['homeTeam']
        away_team = row['awayTeam']
        home_elo = elo_dict.get(home_team, default_elo)
        away_elo = elo_dict.get(away_team, default_elo)

        ## Put the team's current ELO in the dataframe (this is the teams ELO *before* the match)
        data.loc[i, 'homeElo'] = home_elo
        data.loc[i, 'awayElo'] = away_elo

        ## Calculate the new elo scores and update elo_dict with them
        home_victory = row['pointsDiff'] > 0
        home_elo, away_elo = get_updated_elo(home_elo, away_elo, home_victory, K)
        elo_dict[home_team] = home_elo
        elo_dict[away_team] = away_elo

    return elo_dict

# Write some code
def predict(required_predictions, data_loader, log=lambda x: print(x)):
    first_year = 2008

    log('Loading training data')
    train_data = get_multi_season_game_data(data_loader, first_year=first_year, last_year=2020)

    log('Getting Elo ratings over time on train data')
    elo_dict = get_elos_over_time(train_data, starting_elo_dict={}, K=10)
    train_data['EloDifference'] = train_data['homeElo'] - train_data['awayElo']
    train_data['EloSum'] = train_data['homeElo'] + train_data['awayElo']

    log('Fitting linear model from Elo difference and sum to points difference')
    X = train_data[['EloDifference', 'EloSum']]
    X = sm.add_constant(X)
    y = train_data['pointsDiff']
    diff_model = sm.OLS(y, X).fit()

    log('Fitting linear model from Elo difference and sum to points sum')
    y = train_data['pointsSum']
    sum_model = sm.OLS(y, X).fit()

    log('Generating predictions')
    #     required_predictions = pd.DataFrame(required_predictions)
    tmp = required_predictions[['homeTeam', 'awayTeam']].copy()
    tmp['homeElo'] = [elo_dict[team] for team in tmp['homeTeam']]
    tmp['awayElo'] = [elo_dict[team] for team in tmp['awayTeam']]
    tmp['EloDifference'] = tmp.eval('homeElo - awayElo')
    tmp['EloSum'] = tmp.eval('homeElo + awayElo')
    X = tmp[['EloDifference', 'EloSum']]
    X = sm.add_constant(X)
    tmp['predictedDiff'] = diff_model.predict(X)
    tmp['predictedSum'] = sum_model.predict(X)

    required_predictions['predictedDiff'] = tmp['predictedDiff']
    required_predictions['predictedSum'] = tmp['predictedSum']

    log('Finished')

    #     return required_predictions.to_dict('records')
    return required_predictions