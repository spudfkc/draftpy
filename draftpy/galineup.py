import os
import numpy
import random

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

MIN_POINTS = int(os.environ.get("MIN_LINEUP_POINTS", "260"))
MED_POINTS = int(os.environ.get("MED_LINEUP_POINTS", "300"))

MAX_SALARY = 50000
MAX_POINTS = 5000
INDV_INIT_SIZE = 8
NGEN = int(os.environ.get("NGEN", "500"))


random.seed()


class GALineup(object):

    def __init__(self, players):
        self.dup_pos = {}
        self.players = players
        self.num_players = len(players)
        self.pos = players_to_position_map(players)
        self.pos_names = list(self.pos.keys())

        creator.create("Fitness", base.Fitness, weights=(-1.0, 1.0))
        creator.create("Individual", list, fitness=creator.Fitness)

        toolbox = base.Toolbox()
        self.toolbox = toolbox

        toolbox.register("attr_item", random.randrange, self.num_players)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_item, INDV_INIT_SIZE)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", self.evalLineup)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", self.mutSet)
        toolbox.register("select", tools.selNSGA2)

    def evalLineup(self, individual):
        """lower is better?"""
        salary = 0.0
        points = 0.0
        bonus = 0.0
        if len(individual) != 8:
            return 500000, 0
        current_players = []
        for item in individual:
            current_players.append(self.players[item])
            salary += float(self.players[item].salary)
            points += float(self.players[item].est_points)
            position = self.players[item].position
            num_pos = self.dup_pos.get(position, 0)
            num_pos += 1
            self.dup_pos[position] = num_pos
        if len(current_players) != len(set(current_players)):
            # Duplicate players
            return 500000, 0
        if salary > MAX_SALARY:
            # This lineup is too expensive
            return 500000, 0
        if salary < 48000:
            return 500000, 0
        if points < MIN_POINTS:
            # This lineup doesnt make enough points
            return 500000, 0
        if points > MED_POINTS:
            bonus = -30000

        return salary + bonus, points

    def get_random_player_index_for_position(self, position):
        players_in_pos = self.pos[position]
        num_players = len(players_in_pos)
        random.randrange(num_players)

    def random_player(self):
        # Get a random position
        random_index = random.randrange(len(self.pos_names))
        random_pos_name = self.pos_names[random_index]
        # Get a random player in that position
        random_player_in_position = random.randrange(len(self.pos[random_pos_name]))

        new_player = self.pos[random_pos_name][random_player_in_position]
        return new_player, random_pos_name

    def mutSet(self, individual):
        """Mutation that pops and adds an element"""
        if len(individual) == 0:
            # We need to guarentee order here
            for pos_name in self.pos_names:
                individual.append(random.randrange(len(self.pos[pos_name])))
            return individual,

        random_position = random.choice(self.pos.keys())
        random_player_in_position = random.choice(self.pos[random_position])

        # Replace players
        pos_index = self.pos.keys().index(random_position)
        individual[pos_index] = self.pos[random_position].index(random_player_in_position)

        return individual,

    def main(self):
        random.seed()
        MU = 50
        LAMBDA = 100
        CXPB = 0.7
        MUTPB = 0.2

        pop = self.toolbox.population(n=MU)
        hof = tools.HallOfFame(100)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean, axis=0)
        stats.register("std", numpy.std, axis=0)
        stats.register("max", numpy.max, axis=0)

        algorithms.eaMuPlusLambda(pop, self.toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats, halloffame=hof)
        return pop, stats, hof


def get_salary(players):
    return sum([i.salary for i in players])


def get_points(players):
    return sum([i.est_points for i in players])


def players_to_position_map(players):
    pos = {}
    pos_sf = sorted([i for i in players if i.position == "SF"], key=lambda x: x.est_points)
    pos_pf = sorted([i for i in players if i.position == "PF"], key=lambda x: x.est_points)
    pos_sg = sorted([i for i in players if i.position == "SG"], key=lambda x: x.est_points)
    pos_pg = sorted([i for i in players if i.position == "PG"], key=lambda x: x.est_points)
    pos_c = sorted([i for i in players if i.position == "C"], key=lambda x: x.est_points)

    pos_f = sorted(pos_sf + pos_pf, key=lambda x: x.est_points)
    pos_g = sorted(pos_sg + pos_pg, key=lambda x: x.est_points)
    pos_util = sorted(pos_f + pos_g + pos_c, key=lambda x: x.est_points)

    pos["SF"] = pos_sf
    pos["PF"] = pos_pf
    pos["SG"] = pos_sg
    pos["PG"] = pos_pg
    pos["C"] = pos_c
    pos["F"] = pos_f
    pos["G"] = pos_g
    pos["UTIL"] = pos_util

    return pos


class ApoLineup(object):
    pos = {}

    def __init__(self, players):
        self.players = players
        self.pos = players_to_position_map(players)

    def main(self):
        pass


