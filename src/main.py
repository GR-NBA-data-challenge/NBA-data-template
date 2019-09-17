# This is the main function you are requested to define.
# required_predictions: a list of matches that you should predict. Each match is a dictionary
#     containing two keys: "a", the name of the first team, and "b", the name of the second team.
# historical_data: call to obtain the full data of all previous years. This data item does not change over time.
# current_season_matches: call to obtain the full data of all previous games already played in the current season.
#     This does not overlap with historical_data. This is empty when predicting the first match
#     of the current season. As the season progresses, this item will gradually include
#     previous matches of the current season.
# log: you can call log('message') to log any information you want. These messages are automatically
#     printed to console, and to the logfiles when running on the server side.
#     All logs sent to this logger can be retrieved from our servers (up to a maximum size), so
#     use this to debug issues when running your code in our simulations.
# (return): You should return, for each match requested in required_predictions, a number.
#     -1 to indicate that team A wins, 0 to indicate a tie, 1 to indicate that team B wins.
def predict(required_predictions, historical_data, current_season_matches, log):
    # This example code predicts that the first team always wins every match
    hist = historical_data()
    curr = current_season_matches()
    result = []
    for i in range(len(required_predictions)):
        result.append(-1)
    log('finished')
    return result