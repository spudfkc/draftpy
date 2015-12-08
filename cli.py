#!/usr/bin/env python
from __future__ import absolute_import

import redis
import click
import pandas
from nba_py import player as nbaplayer
from draftpy.strategies.last_n_games import LastNGamesStrategy
from draftpy.strategies.vs_team import VsTeamStrategy
import draftpy.galineup
from draftpy.galineup import GALineup


strat2class = {
    "lastngames": LastNGamesStrategy,
    "vsteam": VsTeamStrategy
}


@click.group()
def cli():
    pass


def main():
    cli()


@cli.command()
@click.argument("dkfile", type=click.Path(exists=True))
@click.option("--strategy", default="lastngames", help="The strategy to determine player value with.")
def run(dkfile, strategy):
    filepath = click.format_filename(dkfile)
    reader = DKReader(filepath)
    strat = strat2class.get(strategy.lower())
    if not strat:
        click.echo("Strategy {} not found!".format(strategy))
        return 1
    all_picks = []
    strategy = strat()
    for i in reader.games():
        all_picks += strategy.go(i)

    # Set names on all picks, since we only have IDs at this point
    r = redis.StrictRedis(host="192.168.99.100", port=6379, db=0)
    for pick in all_picks:
        name = r.get(pick.player_id)
        if not name:
            # Ugly as fuuuck ... definitely look into changing this at some point
            name = nbaplayer.PlayerSummary(pick.player_id).json['resultSets'][1]['rowSet'][0][1]
            r.set(pick.player_id, name)
        pick.name = name

    # This is kind of shit. I just want a O(1) lookup time for player salary/pos
    name2attr = {}
    for p in reader.players():
        name2attr[p[0]] = (p[1], p[2])

    # Set salaries and positions on all picks
    for pick in all_picks:
        pick.position = name2attr[pick.name][0]
        pick.salary = name2attr[pick.name][1]

    generator = GALineup(all_picks)
    pop, stats, hof = generator.main()
    hof = [i for i in hof if len(i) == 8]
    for lineup in hof:
        points = sum([all_picks[i].est_points for i in lineup])
        salary = sum([all_picks[i].salary for i in lineup])
        if points < draftpy.galineup.MIN_POINTS:
            # print "--points ",
            continue
        if salary > draftpy.galineup.MAX_SALARY:
            # print "++salary ",
            continue
        print "================================="
        for i in lineup:
            print all_picks[i]
        print "    >points: {}".format(points)
        print "    >salary: {}".format(salary)
    print ">>END HOF<<"
    print stats.max


class DKReader(object):
    FIXED_TEAMS = {
        "GS": "GSW"
    }

    _games = None
    _players = None

    def __init__(self, filepath):
        self.filepath = filepath
        self.read()

    def fix_team_abbr(self, team):
        return self.FIXED_TEAMS.get(team, team)

    def read(self):
        """Reads the file"""
        self.pd_players = pandas.read_csv(self.filepath, header=0)

    def players(self):
        """Return a list of players - tuples: (name, position, salary)"""
        if self._players:
            return self._players

        result = []
        players = [list(x) for x in self.pd_players.values]
        for player in players:
            name = player[1].replace(".", "")
            result.append((name, player[0], player[2]))
        self._players = result
        return self._players

    def games(self):
        """Return a list of games - tuples (home, away)"""
        if self._games:
            return self._games

        result = []
        for game in self.pd_players.GameInfo:
            match = game.split(" ")[0]
            away, home = match.split("@")
            away = self.fix_team_abbr(away).upper()
            home = self.fix_team_abbr(home).upper()
            result.append((home, away))
        self._games = set(result)
        return self._games


if __name__ == "__main__":
    main()
