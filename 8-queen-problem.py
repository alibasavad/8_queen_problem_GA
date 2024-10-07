import random
from itertools import permutations

# constants
pop_size = 50
parentCount = 5
mutation_prob = 5
rounds = 0

# functions


def init(popSize):
    result = []
    for i in range(popSize):
        sample = random.sample(range(1, 9), 8)
        result.append({"genotype": sample, "penality": totalPenality(sample)})

    return (sorted(result, key=lambda chrom: -chrom["penality"]))


def totalPenality(permutation: list):
    penality = 0
    for col, row in enumerate(permutation):
        for index, p in enumerate(permutation):
            if (col == index):
                continue
            if (abs(col - index) == abs(row - p)):
                penality += 1
    return penality


def parentSelectoin(pop, count):
    randomIndex = random.sample(range(len(pop)), count)
    parents = []
    for i in randomIndex:
        parents.append(pop[i])
    parents = (sorted(parents, key=lambda chrom: chrom["penality"]))
    # return [parents[0]["genotype"], parents[1]["genotype"]]
    childs = crossover(parents[0]["genotype"], parents[1]["genotype"])

    return [{
            "genotype": childs[0],
            "penality": totalPenality(childs[0])}, {
            "genotype": childs[1],
            "penality": totalPenality(childs[1])}]


def mutation(child: list):
    if (random.randint(0, 100) > mutation_prob):
        return (child)
    randomIndex = random.sample(range(len(child)), 2)
    gen1 = child[randomIndex[0]]
    gen2 = child[randomIndex[1]]
    child[randomIndex[0]] = gen2
    child[randomIndex[1]] = gen1

    return (child)


def crossover(parent1, parent2):
    position = random.randint(0, 8)
    child1 = parent1[0:position]
    child2 = parent2[0:position]
    for i in range(len(parent1)):
        index = i+position
        if (index >= 8):
            index -= 8
        if parent1[index] not in child2:
            child2.append(parent1[index])
        if parent2[index] not in child1:
            child1.append(parent2[index])

    return [mutation(child1), mutation(child2)]


def printChrom(chrom):
    for i in range(8):
        print("|", end='')
        for j in range(8):
            if j+1 == chrom[i]:
                print(" Q | ", end='')
            else:
                print("   | ", end='')
        print()
        print("----------------------------------------")


pop = init(pop_size)


while True:
    if (pop[-1]["penality"] == 0):
        print("rounds : ", rounds)
        print(pop[-1])
        printChrom(pop[-1]["genotype"])
        break

    childs = parentSelectoin(pop, parentCount)

    if childs[0] not in pop:
        for chrom in pop:
            if (childs[0]["penality"] < chrom["penality"]):
                pop[pop.index(chrom)] = childs[0]
                break
    pop = sorted(pop, key=lambda chrom: -chrom["penality"])

    if childs[1] not in pop:
        for chrom in pop:
            if (childs[1]["penality"] < chrom["penality"]):
                pop[pop.index(chrom)] = childs[1]
                break
    pop = sorted(pop, key=lambda chrom: -chrom["penality"])

    rounds += 1
