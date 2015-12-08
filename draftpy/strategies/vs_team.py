from __future__ import absolute_import

from nba_py import team as nbateam
from draftpy.models import PotentialPick
from draftpy.strategies.util import get_player_ids
from draftpy.strategies.util import DRAFT_KINGS_WEIGHTS
from draftpy.strategies.util import MIN_PLAYER_POINTS


class VsTeamStrategy(object):

    def go(self, game):
        # TODO add redis caching
        # FIXME this doesnt work since refactor
        away, home = game.split('@')
        away = nbateam.TEAMS[away.upper()]
        home = nbateam.TEAMS[home.upper()]

        home_picks = self.picks_against_team(home, away)
        away_picks = self.picks_against_team(away, home)
        all_picks = home_picks + away_picks
        return all_picks

    def picks_against_team(self, team, against_team):
        picks = []
        for player_id in get_player_ids(team):
            stats = nbateam.TeamVsPlayer(team_id=against_team['id'], vs_player_id=player_id)
            tstats = stats.vs_player_overall()
            est_points = 0
            for k in DRAFT_KINGS_WEIGHTS.keys():
                est_points += tstats[k].item()
            if est_points >= MIN_PLAYER_POINTS:
                picks.append(PotentialPick(player_id, est_points))
        return picks
