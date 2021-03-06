from __future__ import absolute_import

import os
from nba_py import player as nbaplayer
from draftpy.strategies.util import get_player_ids
from draftpy.models import PotentialPick
from draftpy.strategies.util import DRAFT_KINGS_WEIGHTS
from draftpy.strategies.util import MIN_PLAYER_POINTS

NUM_GAMES = int(os.environ.get("LAST_N_GAMES", "5"))


class LastNGamesStrategy(object):
    def __init__(self):
        pass

    def go(self, game):
        """game = tuple (home, away)"""
        players = get_player_ids(game[0]) + get_player_ids(game[1])
        return self.picks_last_n_games(players)

    # This signature is kinda weird, but i dont feel like changing it right now
    def picks_last_n_games(self, player_ids, num_games=NUM_GAMES):
        picks = []
        print "Getting stats for players"
        for player_id in player_ids:
            print "Getting stats for player: {}".format(player_id)
            gamelog = nbaplayer.PlayerGameLogs(player_id).info()
            est_points = 0
            for k in DRAFT_KINGS_WEIGHTS.keys():
                est_points += gamelog[k].head(num_games).mean()
            if est_points >= MIN_PLAYER_POINTS:
                picks.append(PotentialPick(player_id, est_points))
        return picks
