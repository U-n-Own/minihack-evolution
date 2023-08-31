import numpy as np
from rules_new import RuleNew, good_movement, make_rule_good
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
    mutation_x, mutation_y = np.where(mutation_matrix < chance_for_mutation)

    for i in range(len(mutation_x)):
        x = mutation_x[i]
        y = mutation_y[i]

        rule.rules_grid[x, y] = np.random.randint(0, 7)  # mutation
        movement = rule.rules_grid[x, y]
        while not good_movement((x, y), movement):
            rule.rules_grid[x, y] = np.random.randint(0, 7)  # mutation
            movement = rule.rules_grid[x, y]

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
                      n_iterations,
                      elitism=0
                      ):
    mean_fitness_epoch = np.zeros((n_iterations,))
    for i in tqdm(range(n_iterations)):
        temperature = 1 - i / n_iterations  # temperature for mutations. Goes down linearly.
        if elitism > 0:
            sort_ind = np.argsort(fitness_list)
            fitness_list = fitness_list[sort_ind]
            population = population[sort_ind]
            best_rules = population[-elitism::]
            best_fitness = fitness_list[-elitism::]
        population, fitness_list = genetic_algorithm_iteration(distance_grid,
                                                               population,
                                                               fitness_calculator,
                                                               fitness_list,
                                                               chance_for_mutation * temperature,
                                                               n_rules)

        fitness_list = np.array(fitness_list)
        population = np.array(population)
        if elitism > 0:
            population=np.append(population, best_rules)
            fitness_list=np.append(fitness_list, best_fitness)
        mean_fitness_epoch[i] = np.sum(fitness_list)/len(fitness_list)
        if np.min(fitness_list) < 0:
            fitness_list = fitness_list - np.min(fitness_list)

    return population, fitness_list, mean_fitness_epoch


if __name__ == '__main__':
    from rules_new import initial_population
    from fitness_new import FitnessCalculator, proximity_score, movement_score, get_population_fitness, \
        find_distance_grid

    initial_pop = initial_population(200)
    for rule in initial_pop:
        make_rule_good(rule)
    # Some shenanigans to make the code work

    goal = (2, 3)
    agent = (8, 6)
    distance_grid = find_distance_grid(*goal)

    fitness_calculator = FitnessCalculator(movement_score, proximity_score, distance_grid)

    fitness_list = get_population_fitness(initial_pop, fitness_calculator)
    fitness_list = np.array(fitness_list)
    initial_pop=np.array(initial_pop)
    fitness_list = fitness_list - np.min(fitness_list)
    new_population, new_fitness, sum_fitnesses = genetic_algorithm(distance_grid=distance_grid,
                                                                   population=initial_pop,
                                                                   fitness_calculator=fitness_calculator,
                                                                   fitness_list=fitness_list,
                                                                   chance_for_mutation=0,
                                                                   n_iterations=200,
                                                                   n_rules=200,
                                                                   elitism=5)
    print(sum_fitnesses)
