import os
import numpy
import random

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

MAX_SALARY = 50000
MAX_POINTS = 750
MIN_POINTS = 200
INDV_INIT_SIZE = 8

random.seed()


class GALineup(object):

    def __init__(self, players):
        self.players = players
        self.num_players = len(players)

        creator.create("Fitness", base.Fitness, weights=(-1.0, 1.0))
        creator.create("Individual", set, fitness=creator.Fitness)

        toolbox = base.Toolbox()
        self.toolbox = toolbox

        toolbox.register("attr_item", random.randrange, self.num_players)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_item, INDV_INIT_SIZE)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", self.evalLineup)
        toolbox.register("mate", self.cxSet)
        toolbox.register("mutate", self.mutSet)
        toolbox.register("select", tools.selNSGA2)

    def evalLineup(self, individual):
        """lower is better?"""
        positions = {}
        salary = 0.0
        points = 0.0
        if len(individual) != 8:
            return 100000000, 0
        for item in individual:
            salary += float(self.players[item].salary)
            points += float(self.players[item].est_points)
            pos = self.players[item].position
            pos_count = positions.get(pos, 0)
            positions[pos] = pos_count + 1
        if salary > MAX_SALARY:
            return 15000, 0
        if points < MIN_POINTS:
            return 10000, 0
        # try to filter out more than x2 of same position
        for k, v in positions.iteritems():
            if v > 2:
                return 10000, 0
        return salary, points

    def cxSet(self, ind1, ind2):
        """Crossover on input sets"""
        temp = set(ind1)
        ind1 &= ind2
        ind2 ^= temp
        return ind1, ind2

    def mutSet(self, individual):
        """Mutation that pops and adds an element"""
        if len(individual) > 0:
            individual.remove(random.choice(sorted(tuple(individual))))
        individual.add(random.randrange(self.num_players))

        # This would be the pop OR add element
        # if random.random() < 0.5:
        #     if len(individual) > 0:
        #         individual.remove(random.choice(sorted(tuple(individual))))
        # else:
        #     individual.add(random.randrange(self.num_players))
        return individual,

    def main(self):
        random.seed()
        NGEN = int(os.environ.get("NGEN", "500"))
        MU = 50
        LAMBDA = 100
        CXPB = 0.7
        MUTPB = 0.2

        pop = self.toolbox.population(n=MU)
        real_hof = tools.HallOfFame(100)
        hof = tools.ParetoFront()
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean, axis=0)
        stats.register("std", numpy.std, axis=0)
        stats.register("max", numpy.max, axis=0)

        algorithms.eaMuPlusLambda(pop, self.toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats, halloffame=real_hof)
        return real_hof
        # return pop, stats, hof
