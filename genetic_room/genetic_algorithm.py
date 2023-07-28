"""
In this file we implement the genetic algorithm 
that we use to generate the best rule
"""

import numpy as np
import random
from typing import List
from utility_func import print_room, search_environment_indexes, search_environment_agent_position, search_environment_goal_position
from utility_func import step_dictionary, movement_dictionary
from rules import Rule, generate_initial_population
from fitness_func import find_distance_grid, fitness_function

def get_temperature(number_of_generation):
    temperature=[]
    for x in range(number_of_generation):
        temperature.append(1-x/(number_of_generation-1))   
    return temperature

def choose_rules(numeber_of_population, norm_fitness_func):

    indexes_rules = range(len(norm_fitness_func))
    return np.random.choice(indexes_rules, p=norm_fitness_func, size=len(numeber_of_population))


def normalize_fitness(fitness_func):

    translate_fitness=[float(i)-min(fitness_func) for i in fitness_func]
    norm_fitness_func=[float(i)/sum(translate_fitness) for i in translate_fitness]

    return norm_fitness_func

def mutation(chance_for_mutation, rule):

    mutation_matrix=np.random.random(size=(15,15))
    indexes=np.where(mutation_matrix<chance_for_mutation)

    for i in range(len(indexes[0])):
        x=indexes[0][i]
        y=indexes[1][i]

        rule.rules_grid[x][y]=random.randint(0,7)

def genetic_algorithm(room, 
                      population, 
                      fitness_func, 
                      number_of_population, 
                      chance_for_mutation, 
                      number_of_generation):

    norm_fitness_func=normalize_fitness(fitness_func)
    temperature=get_temperature(number_of_generation)


        