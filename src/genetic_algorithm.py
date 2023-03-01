import gym
import minihack
import numpy as np
from typing import List
import random
import math
import pygad
import sys
from operator import itemgetter

# for src path import
sys.path.append('../')

from src.utilities import search_goal
from src.rules import Rule, generate_initial_population
from src.fitness_func import fitness, normalize_fitness
from src.genetic_plot import average_fitness_plot
# creo l'ambiente di gioco (in questo caso una stanza 15x15)

average_fitness = []

env = gym.make("MiniHack-Room-Random-15x15-v0",
               observation_keys=("chars", "colors", "specials", "pixel"), )


def choose_rules(n_rules, fitness_list):
    indexes_rules = range(len(fitness_list))
    return np.random.choice(indexes_rules, p=fitness_list, size=n_rules)


def mutation(chance_for_mutation, rule):
    c = np.random.random()
    mutation_occurred = (c <= chance_for_mutation)
    if mutation_occurred:
        mutation_point = np.random.randint(0, len(rule.movement))
        possible_movements = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if (x, y) != (0, 0)]
        rule.movement[mutation_point] = random.choice(possible_movements)


def genetic_alg_iteration(environment,
                          rules,
                          fitness_list,
                          number_of_rules=1000,
                          chance_for_mutation=0.1
                          ):
    rules_indices = choose_rules(number_of_rules, fitness_list)
    old_rules = []
    for i in rules_indices:
        old_rules.append(rules[i])
    new_rules = []
    new_fitness = []
    for (rule_1, rule_2) in zip(old_rules[0::2], old_rules[1::2]):
        new_rule_1 = Rule(1)
        new_rule_2 = Rule(1)

        # exchanging the movements to create the new rules: crossover single point
        new_rule_1.position = rule_1.position
        new_rule_2.position = rule_2.position
        new_rule_2.movement = rule_1.movement
        new_rule_1.movement = rule_2.movement

        # mutation
        mutation(chance_for_mutation, new_rule_1)
        mutation(chance_for_mutation, new_rule_2)

        # compute fitness of new rules
        fitness_1 = fitness(new_rule_1, environment)
        fitness_2 = fitness(new_rule_2, environment)

        new_fitness.append(fitness_1)
        new_fitness.append(fitness_2)
        new_rules.append(new_rule_1)
        new_rules.append(new_rule_2)
        
    new_fitness_norm = normalize_fitness(new_fitness)
    
    return new_rules, new_fitness, new_fitness_norm


def genetic_algorithm(environment,
                      rules,
                      fitness_list_norm,
                      number_of_rules=1000,
                      chance_for_mutation=0.1,
                      number_of_generations = 0):

    for i in range(number_of_generations):
        print("generazione:", i)
        rules, fitness_list, fitness_list_norm = genetic_alg_iteration(
            environment,
            rules,
            fitness_list_norm,
            number_of_rules=number_of_rules,
            chance_for_mutation=chance_for_mutation,
        )
        
        
        average_fitness.append(np.mean(fitness_list))
        
        
    average_fitness_plot(average_fitness, number_of_generations)
 
    return rules, fitness_list, fitness_list_norm



