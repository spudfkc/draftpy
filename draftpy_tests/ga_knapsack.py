import numpy
import pandas as pd
import random

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

MAX_SALARY = 50000
MAX_POINTS = 1000
INDV_INIT_SIZE = 8

random.seed(64)

## load players
pd_players = pd.read_csv('DKSalaries.csv', header=0)
players = [list(x) for x in pd_players.values]

num_players = len(players)

creator.create("Fitness", base.Fitness, weights=(-1.0, 1.0))
creator.create("Individual", set, fitness=creator.Fitness)

toolbox = base.Toolbox()

toolbox.register("attr_item", random.randrange, num_players)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_item, INDV_INIT_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalLineup(individual):
    salary = 0.0
    points = 0.0
    for item in individual:
        salary += float(players[item][2])
        points += float(players[item][4])
    if len(individual) > MAX_POINTS or salary > MAX_SALARY:
        return 10000, 0
    return salary, points

def cxSet(ind1, ind2):
    """Crossover on input sets"""
    temp = set(ind1)
    ind1 &= ind2
    ind2 ^= temp
    return ind1, ind2

def mutSet(individual):
    """Mutation that pops or adds an element"""
    if random.random() < 0.5:
        if len(individual) > 0:
            individual.remove(random.choice(sorted(tuple(individual))))
    else:
        individual.add(random.randrange(num_players))
    return individual,

toolbox.register("evaluate", evalLineup)
toolbox.register("mate", cxSet)
toolbox.register("mutate", mutSet)
toolbox.register("select", tools.selNSGA2)

def main():
    random.seed(64)
    NGEN = 500
    MU = 50
    LAMBDA = 100
    CXPB = 0.7
    MUTPB = 0.2

    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats, halloffame=hof)
    return pop, stats, hof

if __name__ == "__main__":
    main()
