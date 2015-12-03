from nba_py import team as nbateam
from nba_py import player as nbaplayer
from strategies.util import get_player_ids
from models import PotentialPick


MIN_POINTS = int(os.environ.get('MIN_PLAYER_POINTS', '30'))


class VsTeamStrategy(object):

    def go(self, game):
        away, home = game.split('@')
        away = nbateam.TEAMS[away.upper()]
        home = nbateam.TEAMS[home.upper()]

        home_picks = self.picks_against_team(home, away)
        away_picks = self.picks_against_team(away, home)
        all_picks = home_picks + away_picks
        return all_picks

    def picks_against_team(self, team, against_team):
        result = []
        for player_id in get_player_ids(team):
            stats = nbateam.TeamVsPlayer(team_id=against_team['id'], vs_player_id=player_id)
            tstats = stats.json['resultSets'][1]['rowSet'][0]
            threes = tstats[11]
            blocks = tstats[23]
            rebounds = tstats[19]
            turnovers = tstats[21]
            steals = tstats[22]
            points = tstats[27]
            doubledouble = tstats[29]
            tripledouble = tstats[30]
            assists = tstats[20]
            pick = self.create_pick(player_id, points, threes, assists, rebounds, blocks, steals, turnovers, doubledouble, tripledouble)
            if pick:
                result.append(pick)
        return result

    def create_pick(self, player_id, points, threes, assists, rebounds, blocks, steals, turnovers, doubledouble, tripledouble):
        est_fantasy_points = points
        est_fantasy_points += (threes * 0.5)
        est_fantasy_points += (assists * 1.5)
        est_fantasy_points += (rebounds * 1.25)
        est_fantasy_points += (blocks * 2)
        est_fantasy_points += (steals * 2)
        est_fantasy_points += (turnovers * -0.5)
        ## FIXME this logic is not correct...find out what doubledouble actually is
        if doubledouble > 1:
            est_fantasy_points += 1.5
        if tripledouble > 1:
            est_fantasy_points += 3
        if est_fantasy_points >= self.MIN_POINTS:
            return PotentialPick(player_id, est_fantasy_points)
        else:
            return None