from nba_py import player as nbaplayer


class PotentialPick(object):
    player_id = None
    est_points = None

    def __init__(self, player_id, est_points):
        self.player_id = player_id
        self.est_points = est_points
        self.name = "-"
        self.position = "-"
        self.salary = "-"

    def __str__(self):
        return '{} ~ {} ~ {}'.format(self.name, self.player_id, self.est_points)


class PlayerPicker(object):
    strategy = None

    def __init__(self, strategy):
        self.strategy = strategy

    def run(self, games):
        best_picks = []
        for game in games:
            best_picks = best_picks + self.strategy.go(game)
        return best_picks


class PlayerFilter(object):
    def filter(self, player):
        pass
