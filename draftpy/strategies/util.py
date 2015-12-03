import os
from nba_py import team as nbateam


MIN_PLAYER_POINTS = int(os.environ.get("MIN_PLAYER_POINTS", "30"))

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
    if type(team) != str:
        team = team['id']
    return [i for i in nbateam.TeamPlayers(team).season_totals().PLAYER_ID]
