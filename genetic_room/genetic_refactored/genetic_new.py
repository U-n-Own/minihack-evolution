import numpy as np
from rules_new import RuleNew, make_rule_good
from tqdm import tqdm

def choose_rules(fitness_list: list, n_rules=100):
    '''
    choose n_rules rules from the population according to their fitness
    '''
    # normalize the fitness
    fitness_list = np.array(fitness_list)
    fitness_list = fitness_list / np.sum(fitness_list)
    # choose n_rules rules
    return np.random.choice(range(len(fitness_list)), size=n_rules, p=fitness_list)


def mutation(chance_for_mutation, rule):
    '''
    apply a mutation to the rule with a chance_of_mutation
    probability for each position in the room.
    '''
    mutation_matrix = np.random.random(size=(15, 15))
    mutation_indexes = np.where(mutation_matrix < chance_for_mutation)

    for i in range(len(mutation_indexes[0])):
        x = mutation_indexes[0][i]
        y = mutation_indexes[1][i]

        rule.rules_grid[x, y] = np.random.randint(0, 7)  # mutation

    rule = make_rule_good(rule)
    return rule


def crossover(parent1: RuleNew, parent2: RuleNew):
    crossover_mask = np.random.randint(2, size=(15, 15))
    child1 = RuleNew()
    child2 = RuleNew()
    for i in range(15):
        for j in range(15):
            if crossover_mask[i, j] == 0:
                child1.set_movement(i, j, parent1.get_movement(i, j))
                child2.set_movement(i, j, parent2.get_movement(i, j))
            else:
                child1.set_movement(i, j, parent2.get_movement(i, j))
                child2.set_movement(i, j, parent1.get_movement(i, j))
    return child1, child2


def genetic_algorithm_iteration(distance_grid,
                                population,
                                fitness_calculator,
                                fitness_list,
                                chance_for_mutation,
                                n_rules):
    """
    one iteration of the genetic algorithm
    parameters:
        distance_grid: the distance grid of the room: distance_grid[i,j] is the infinite norm distance from (i,j)
        to the goal
        population: the population of rules
        fitness_list: the fitness list of the population. Can be non normalized, but must be positive.
        chance_for_mutation: the chance for mutation for each position in the room
        n_rules: the number of rules to choose. The new population will have n_rules rules
    """

    # choose the rules
    rules_indexes = choose_rules(fitness_list, n_rules)
    population_parents = [population[i] for i in rules_indexes]
    new_population = []
    for i in range(0, len(population_parents), 2):
        parent1 = population_parents[i]
        parent2 = population_parents[i + 1]
        # crossover
        child1, child2 = crossover(parent1, parent2)
        # mutation
        child1 = mutation(chance_for_mutation, child1)
        child2 = mutation(chance_for_mutation, child2)
        # add the children to the new population
        new_population.append(child1)
        new_population.append(child2)

    # calculate the fitness of the new population
    fitness_list = [fitness_calculator.calculate_fitness(rule) for rule in new_population]
    return new_population, fitness_list


def genetic_algorithm(distance_grid,
                      population,
                      fitness_calculator,
                      fitness_list,
                      chance_for_mutation,
                      n_rules,
                      n_iterations):
    sum_fitness_epoch=np.zeros((n_iterations,))
    for i in tqdm(range(n_iterations)):
        temperature = 1 - i / n_iterations
        population, fitness_list = genetic_algorithm_iteration(distance_grid,
                                                               population,
                                                               fitness_calculator,
                                                               fitness_list,
                                                               chance_for_mutation * temperature,
                                                               n_rules)

        fitness_list = np.array(fitness_list)
        sum_fitness_epoch[i] = np.sum(fitness_list)
        if np.min(fitness_list) < 0:
            fitness_list = fitness_list - np.min(fitness_list)

    return population, fitness_list, sum_fitness_epoch


