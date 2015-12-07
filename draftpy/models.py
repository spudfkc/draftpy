from nba_py import player as nbaplayer


class PotentialPick(object):
    player_id = None
    est_points = None

    def __init__(self, player_id, est_points):
        self.player_id = player_id
        self.est_points = est_points

    def __str__(self):
        return '{} ~ {} ~ {}'.format(self.name, self.player_id, self.est_points)


class PlayerPicker(object):
    strategy = None

    def __init__(self, strategy):
        self.strategy = strategy

    def resolve(self, picks):
        result = []
        for pick in picks:
            r = {
                "id": pick.player_id,
                "name": nbaplayer.PlayerSummary(pick.player_id).json['resultSets'][1]['rowSet'][0][1],
                "points": pick.est_points,
            }
            result.append(r)
        return result

    def run(self, games):
        best_picks = []
        for game in games:
            best_picks = best_picks + self.strategy.go(game)
        return best_picks


class PlayerFilter(object):
    def filter(self, player):
        pass
