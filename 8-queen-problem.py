import random
import matplotlib.pyplot as plt

# constants
popSize = 100
matingPoolSize = 5
mutationProb = 0.05  # 5%
crossoverProb = 0.8  # 80%
queen_count = 15
rounds = 0
maxRounds = 10000
maxFitness = (queen_count * (queen_count - 1)) / 2
survivalMethod = "Generational"  # choose between "Elitism" or "Generational"

# functions


def init(popSize):
    """
    population initialize function

    Args:
        popSize (number): population size

    Returns:
        list: sorted initialized population with their fitness
    """
    pop = []
    for _ in range(popSize):
        sample = random.sample(range(1, queen_count + 1), queen_count)
        pop.append({"genotype": sample, "fitness": fitness(sample)})

    return sorted(pop, key=lambda chrom: chrom["fitness"])


def fitness(permutation: list):
    """
    fitness function that calculate the crashes of queens and return (maximum crashes possible - crash count)
    as fitness valuue

    Args:
        permutation (list): valid genotype

    Returns:
        number: fitness
    """
    crashCount = 0
    for col, row in enumerate(permutation):
        for index, val in enumerate(permutation):
            if (col == index):
                continue
            if (abs(col - index) == abs(row - val)):
                crashCount += 1

    maxCrashes = (queen_count * (queen_count - 1)) / 2

    return (maxCrashes) - (crashCount / 2)


def parentSelectoin(pop, matingPoolSize):
    """
    Parent selection function : select random mating pool and aftar thar
    select best 2 of them for crossover

    Args:
        pop (list): population
        matingPoolSize (number): size of mating pool

    Returns:
        list: two genotype as parent
    """
    matingPool = []
    randomIndexes = random.sample(range(len(pop)), matingPoolSize)
    for i in randomIndexes:
        matingPool.append(pop[i])
    parents = sorted(matingPool, key=lambda chrom: chrom["fitness"])

    return [parents[0], parents[1]]


def mutation(child: list):
    """mutation : replace two random gens

    Args:
        child (list): genotype permutation

    Returns:
        list: mutated genotype
    """
    if (random.random() > mutationProb):
        return (child)
    randomIndex = random.sample(range(len(child)), 2)
    gen1 = child[randomIndex[0]]
    gen2 = child[randomIndex[1]]
    child[randomIndex[0]] = gen2
    child[randomIndex[1]] = gen1

    return (child)


def crossover(parent1, parent2):
    """crossover

    Args:
        parent1 (list): genotype
        parent2 (list): genotype

    Returns:
        list: two children genotype
    """

    if (random.random() > crossoverProb):
        return [parent1, parent2]

    position = random.randint(1, queen_count - 1)
    child1 = parent1[0:position]
    child2 = parent2[0:position]
    for i in range(len(parent1)):
        index = i+position
        if (index >= queen_count):
            index -= queen_count
        if parent1[index] not in child2:
            child2.append(parent1[index])
        if parent2[index] not in child1:
            child1.append(parent2[index])

    return [child1, child2]


def survivalSelection(pop, child):
    """survival selection

    Args:
        pop (list): population
        child (list): child

    Returns:
        list: new population
    """
    for chrom in pop:
        if (child["fitness"] >= chrom["fitness"]):
            pop[pop.index(chrom)] = child
            break
    return sorted(pop, key=lambda chrom: chrom["fitness"])


pop = init(popSize)

while True:

    if (pop[0]["fitness"] == maxFitness or rounds == maxRounds):
        print("rounds : ", rounds)
        print(pop[0])
        break

    recombinationCount = 1
    if (survivalMethod == "Generational"):
        recombinationCount = popSize//2

    childs = []

    for i in range(recombinationCount):
        parents = parentSelectoin(pop, matingPoolSize)

        crossoveredChilds = crossover(
            parents[0]["genotype"], parents[1]["genotype"])

        mutatedChilds = []

        for child in crossoveredChilds:
            mutatedChilds.append(mutation(child))

        for child in mutatedChilds:
            childs.append({"genotype": child, "fitness": fitness(child)})

    for child in childs:
        survivalSelection(pop, child)

    rounds += 1
