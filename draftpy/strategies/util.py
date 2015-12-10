import os
from nba_py import team as nbateam


MIN_PLAYER_POINTS = int(os.environ.get("MIN_PLAYER_POINTS", "20"))

id2player = {}

## TODO should probably move this
DRAFT_KINGS_WEIGHTS = {
    'BLK': 2,
    'AST': 1.5,
    'FG3M': 0.5,
    'PTS': 1,
    'REB': 1.25,
    'STL': 2,
    'TOV': -0.5,
}


def get_player_ids(team):
    if team in nbateam.TEAMS.keys():
        team = nbateam.TEAMS[team]['id']
    if type(team) != str:
        team = team['id']
    players = nbateam.TeamPlayers(team).season_totals()
    names = [i for i in players.PLAYER_NAME]
    ids = [i for i in players.PLAYER_ID]
    for i in range(len(ids)):
        id2player[ids[i]] = names[i]
    return [i for i in players.PLAYER_ID]
