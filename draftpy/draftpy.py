#!/usr/bin/env python
# Input needed:
#  1. list of games (incl home/away)
#  2. list of player salaries
#  3. list of players that are out
#
import os
import sys
import pprint
from nba_py import team as nbateam
from nba_py import player as nbaplayer
from nba_py import constants
from strategies.util import get_player_ids
from strategies.last_n_games import *
from models import *

constants.CURRENT_SEASON = '2015-16'
pp = pprint.PrettyPrinter(indent=2)


def main():
    games = sys.argv[1:]

    # strategy = VsTeamStrategy()
    strategy = LastNGamesStrategy()
    f = PlayerFilter()
    g = BasicLineupGenerator()
    picker = PlayerPicker(strategy)

    picks = picker.run(games)

    d = picker.resolve(picks)
    d.sort(key=lambda x: x['points'])
    pp.pprint(d)

    lineups = g.generate(picks)


if __name__ == "__main__":
    main()


