#!/usr/bin/env python
# Input needed:
#  1. list of games (incl home/away)
#  2. list of player salaries
#  3. list of players that are out
#
import sys
import pprint
from nba_py import constants
from strategies import last_n_games
# from draftpy.strategies.vs_team import VsTeamStrategy
import models
from generators import BasicLineupGenerator

constants.CURRENT_SEASON = '2015-16'
pp = pprint.PrettyPrinter(indent=2)


def main():
    games = sys.argv[1:]

    # strategy = VsTeamStrategy()
    strategy = last_n_games.LastNGamesStrategy()
    f = models.PlayerFilter()
    g = BasicLineupGenerator()
    picker = models.PlayerPicker(strategy)

    picks = picker.run(games)

    d = picker.resolve(picks)
    d.sort(key=lambda x: x['points'])
    pp.pprint(d)

    lineups = g.generate(picks)
    # print lineups


if __name__ == "__main__":
    main()


