from nba_py import team as nbateam
from nba_py import player as nbaplayer
from strategies.util import get_player_ids
from models import PotentialPick
from strategies.util import DRAFT_KINGS_WEIGHTS
from strategies.util import MIN_PLAYER_POINTS


class LastNGamesStrategy(object):

    def go(self, game):
        away, home = game.split('@')
        away = nbateam.TEAMS[away.upper()]
        home = nbateam.TEAMS[home.upper()]
        players = get_player_ids(home) + get_player_ids(away)
        return self.picks_last_n_games(players)

    def picks_last_n_games(self, player_ids, num_games=5):
        picks = []
        for player_id in player_ids:
            log = nbaplayer.PlayerGameLogs(player_id).info()
            est_points = 0
            for k in DRAFT_KINGS_WEIGHTS.keys():
                est_points += log[k].head(num_games).mean()
            if est_points >= MIN_PLAYER_POINTS:
                picks.append(PotentialPick(player_id, est_points))
        return picks
