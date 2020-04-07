
import random
import math
from deap import base
from deap import creator
from deap import tools

class myclass:
    def __init__(self):
        self.yo=[]

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
creator.create("Fitnessfunc",base.Fitness, weights=(1.0,))
creator.create("Individualfunc",myclass,fitness=creator.FitnessMax)
ind=creator.Individualfunc()
print(ind.yo)

toolbox = base.Toolbox()
toolboxfunc = base.Toolbox()
# Attribute generator
#                      define 'attr_bool' to be an attribute ('gene')
#                      which corresponds to integers sampled uniformly
#                      from the range [0,1] (i.e. 0 or 1 with equal
#                      probability)
def fill_myclass():
    class1=creator.Individualfunc()
    for i in range(100):
        class1.yo.append(random.randint(0,1))
    return class1

toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers
#                         define 'individual' to be an individual
#                         consisting of 100 'attr_bool' elements ('genes')
toolbox.register("individual", tools.initRepeat, creator.Individual,
    toolbox.attr_bool, 100)

# define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolboxfunc.register("individual",fill_myclass)
toolboxfunc.register("population",tools.initRepeat,list,toolboxfunc.individual)

# the goal ('fitness') function to be maximized
def evalOneMax(individual):
    return sum(individual),

def evalMaxfunc(individual):
    return sum(individual.yo),

def mutatefunc(individual,indpb=0.1):
    for i in range(len(individual.yo)):
        if random.random() < indpb:
            individual.yo[i] = type(individual.yo[i])(not individual.yo[i])

    return individual,

def matefunc(ind1,ind2):
    size = min(len(ind1.yo), len(ind2.yo))
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    ind1.yo[cxpoint1:cxpoint2], ind2.yo[cxpoint1:cxpoint2] \
        = ind2.yo[cxpoint1:cxpoint2], ind1.yo[cxpoint1:cxpoint2]

    return ind1, ind2
#----------
# Operator registration
#----------
# register the goal / fitness function
toolbox.register("evaluate", evalOneMax)
# register the crossover operator
toolbox.register("mate", tools.cxTwoPoint)
# register a mutation operator with a probability to
# flip each attribute/gene of 0.05
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
# operator for selecting individuals for breeding the next
# generation: each individual of the current generation
# is replaced by the 'fittest' (best) of three individuals
# drawn randomly from the current generation.
toolbox.register("select", tools.selTournament, tournsize=3)

toolboxfunc.register("evaluate", evalMaxfunc)
toolboxfunc.register("mate",matefunc)
toolboxfunc.register("mutate",mutatefunc,indpb=0.05)
toolboxfunc.register("select", tools.selTournament, tournsize=3)

#----------

def main():
    random.seed(64)
    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolboxfunc.population(n=300)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2

    print("Start of evolution")

    # Evaluate the entire population
    fitnesses = list(map(toolboxfunc.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        print(fit)

    print("  Evaluated %i individuals" % len(pop))
    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]
    for a in fits:
        print(a)
    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while max(fits) < 10 and g < 10:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolboxfunc.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolboxfunc.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolboxfunc.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolboxfunc.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolboxfunc.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

if __name__ == "__main__":
    main()
