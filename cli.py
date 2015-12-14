#!/usr/bin/env python
from __future__ import absolute_import

import click
import pandas
from nba_py import player as nbaplayer
from draftpy.strategies.last_n_games import LastNGamesStrategy
from draftpy.strategies.vs_team import VsTeamStrategy
import draftpy.galineup
from draftpy.galineup import *


strat2class = {
    "lastngames": LastNGamesStrategy,
    "vsteam": VsTeamStrategy,
}

lineup2class = {
    "galineup": GALineup,
}


@click.group()
def cli():
    pass


def main():
    cli()


@cli.command()
@click.argument("dkfile", type=click.Path(exists=True))
@click.option("--strategy", default="lastngames", help="The strategy to determine player value with.")
@click.option("--lineup-gen", default="galineup", help="The lineup generation strategy to generate lineups.")
@click.option("--env", type=click.Path(exists=True), default=None, help="Path to a file containing environment variables to use.")
def run(dkfile, strategy, lineup_gen, env):
    if env:
        with open(env, "r") as f:
            env_data = f.read()
        for line in env_data.split("\n"):
            key, value = line.split("=")
            os.environ[key] = value

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
    for pick in all_picks:
        # Ugly as fuuuck ...there is a better way, i just haven't taken the time to find it
        pick.name = nbaplayer.PlayerSummary(pick.player_id).json['resultSets'][1]['rowSet'][0][1]

    # This is kind of shit. I just want a O(1) lookup time for player salary/pos
    name2attr = {}
    for p in reader.players():
        name2attr[p[0]] = (p[1], p[2])

    # Set salaries and positions on all picks
    for pick in all_picks:
        pick.position = name2attr[pick.name][0]
        pick.salary = name2attr[pick.name][1]

    for pick in all_picks:
        print pick

    if not lineup_gen:
        return

    generator = GALineup(all_picks)
    pop, stats, hof = generator.main()
    hof = [i for i in hof if len(i) == 8]
    for lineup in hof:
        points = sum([all_picks[i].est_points for i in lineup])
        salary = sum([all_picks[i].salary for i in lineup])
        if points < draftpy.galineup.MIN_POINTS:
            continue
        if salary > draftpy.galineup.MAX_SALARY:
            continue
        print "================================="
        for i in lineup:
            print all_picks[i]
        print "    >points: {}".format(points)
        print "    >salary: {}".format(salary)
    print ">>END HOF<<"


class DKReader(object):
    FIXED_TEAMS = {
        "GS": "GSW",
        "PHO": "PHX",
        "NY": "NYK",
        "SA": "SAS",
        "NO": "NOP",
    }

    FIXED_PLAYERS = {
        "O.J. Mayo": "O.J. Mayo",
        "J.R. Smith": "J.R. Smith",
    }

    _games = None
    _players = None

    def __init__(self, filepath):
        self.filepath = filepath
        self.read()

    def fix_team_abbr(self, team):
        return self.FIXED_TEAMS.get(team, team)

    def fix_player_name(self, player_name):
        if player_name in self.FIXED_PLAYERS.keys():
            return self.FIXED_PLAYERS[player_name]
        return player_name.replace(".", "")

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
            name = self.fix_player_name(player[1])
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
            away = self.fix_team_abbr(away.upper())
            home = self.fix_team_abbr(home.upper())
            result.append((home, away))
        self._games = set(result)
        return self._games


if __name__ == "__main__":
    main()
