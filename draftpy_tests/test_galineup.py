from unittest2 import TestCase
from draftpy import galineup
from draftpy.cli import DKReader
from draftpy.models import PotentialPick


class GalineupTest(TestCase):

    def test_players_to_position_map(self):
        expected_c = [
            "Pau Gasol",
            "DeAndre Jordan",
            "Al Horford",
        ]

        expected_pg = [
            "Russell Westbrook",
            "Rajon Rondo",
            "Chris Paul",
            "Jeff Teague",
            "Derrick Rose",
            "Dennis Schroder",
        ]

        expected_sg = [
            "Jimmy Butler",
            "Jamal Crawford",
        ]

        expected_sf = [
            "Kevin Durant",
            "Carmelo Anthony",
            "Rudy Gay",
            "Omri Casspi",
        ]

        expected_pf = [
            "DeMarcus Cousins",
            "Blake Griffin",
            "Paul Millsap",
            "Kristaps Porzingis",
            "Serge Ibaka",
            "Nikola Mirotic",
        ]

        expected_g = expected_pg + expected_sg
        expected_f = expected_sf + expected_pf
        expected_util = expected_c + expected_pg + expected_pf + expected_sf + expected_sg

        reader = DKReader("dksalaries/DKSalaries-test.csv")
        picks = [PotentialPick(0, 0, name=i[0], position=i[1], salary=i[2]) for i in reader.players()]
        players = galineup.players_to_position_map(picks)
        self.assertEqual(expected_sf, [i.name for i in players["SF"]])
        self.assertEqual(expected_pf, [i.name for i in players["PF"]])
        self.assertEqual(expected_sg, [i.name for i in players["SG"]])
        self.assertEqual(expected_pg, [i.name for i in players["PG"]])
        self.assertEqual(expected_c, [i.name for i in players["C"]])
        self.assertEqual(len(expected_util), len(players["UTIL"]))
        self.assertEqual(set(expected_g), set([i.name for i in players["G"]]))
        self.assertEqual(expected_f, [i.name for i in players["F"]])


