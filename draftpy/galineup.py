import numpy
# import pandas as pd
import random

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

MAX_SALARY = 50000
MAX_POINTS = 1000
MIN_POINTS = 100
INDV_INIT_SIZE = 8

random.seed()


## load players
# print players
class GALineup(object):

    def __init__(self, players):
        # pd_players = pd.read_csv('DKSalaries.csv', header=0)
        self.players = players  # [list(x) for x in pd_players.values]
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
            return 10000, 0
        for item in individual:
            salary += float(self.players[item].salary)
            points += float(self.players[item].est_points)
            pos = self.players[item].position
            pos_count = positions.get(pos, 0)
            positions[pos] = pos_count + 1
        if salary > MAX_SALARY:
            return 10000, 0
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
        """Mutation that pops or adds an element"""
        if random.random() < 0.5:
            if len(individual) > 0:
                individual.remove(random.choice(sorted(tuple(individual))))
        else:
            individual.add(random.randrange(self.num_players))
        return individual,

    def main(self):
        random.seed()
        NGEN = 100
        MU = 50
        LAMBDA = 100
        CXPB = 0.7
        MUTPB = 0.2

        pop = self.toolbox.population(n=MU)
        hof = tools.ParetoFront()
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean, axis=0)
        stats.register("std", numpy.std, axis=0)
        stats.register("max", numpy.max, axis=0)

        algorithms.eaMuPlusLambda(pop, self.toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats, halloffame=hof)
        return hof
        # return pop, stats, hof


# if __name__ == "__main__":
#     r = main()
#     print r
#     print ""
#     print [players[i] for i in r[0][0]]
