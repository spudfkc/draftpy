from __future__ import absolute_import

import pandas as pd
from draftpy.strategies.util import id2player
from draftpy.galineup import GALineup


class SalaryResolver(object):
    salaries = {}

    def __init__(self, path):
        pd_players = pd.read_csv(path, header=0)
        players = [list(x) for x in pd_players.values]
        for player in players:
            # name -> salary
            name = player[1].replace('.', '')
            self.salaries[name] = (player[2], player[0])


class BasicLineupGenerator(object):
    def generate(self, potential_picks):
        sr = SalaryResolver("DKSalaries.csv")
        for p in potential_picks:
            p.name = id2player[p.player_id]
            p.salary = sr.salaries[p.name][0]
            p.position = sr.salaries[p.name][1]

        galineup = GALineup(potential_picks)
        lineups = galineup.main()

        best = [i for i in lineups if len(i) == 8]
        print "=========="
        for i in best:
            for j in i:
                print potential_picks[j]
            print "=========="
        return lineups
