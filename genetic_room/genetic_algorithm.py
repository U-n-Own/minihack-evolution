"""
In this file we implement the genetic algorithm 
that we use to generate the best rule
"""

import numpy as np
import random
import copy
from typing import List
from utility_func import print_room, search_environment_indexes, search_environment_agent_position, search_environment_goal_position
from utility_func import step_dictionary, movement_dictionary
from rules import Rule, generate_initial_population
from fitness_func import find_distance_grid, fitness_function

def get_temperature(number_of_generation):
    """
    define the temperature that we will use 
    to lower the chance_of_mutation during generations.
    """
    temperature=[]
    for x in range(number_of_generation):
        temperature.append(1-x/(number_of_generation-1))   
    return temperature

def normalize_fitness(fitness_func):
    """
    fitness scores are normalized to probabilities
    for use them in the choose_rules function.
    """
    translate_fitness=[float(i)-min(fitness_func) for i in fitness_func]
    norm_fitness_func=[float(i)/sum(translate_fitness) for i in translate_fitness]

    return norm_fitness_func

def choose_rules(numeber_of_population, norm_fitness_func):
    """
    choose the rules with probabilities that will be the parents to 
    generate two new rules during the genetic algorithm.
    """
    indexes_rules = range(len(norm_fitness_func))
    return np.random.choice(indexes_rules, p=norm_fitness_func, size=len(numeber_of_population))

def mutation(chance_for_mutation, rule):
    """
    apply a mutation to the rule with a chance_of_mutation
    probability for each position in the room.
    """
    mutation_matrix=np.random.random(size=(15,15))
    indexes=np.where(mutation_matrix<chance_for_mutation)

    for i in range(len(indexes[0])):
        x=indexes[0][i]
        y=indexes[1][i]

        rule.rules_grid[x][y]=random.randint(0,7)
    
    rule.rules_grid=rule.is_good()
    return rule

def genetic_algorithm_iteration(distance_grid, population, norm_fitness_func, chance_for_mutation):

    rules_indexes=choose_rules(len(population), norm_fitness_func)
    population_parents=[]

    for i in rules_indexes:
        population_parents.append(population[i])

    new_population=[]
    new_fitness_func=[]

    for i in range(0, len(population_parents), 2):

        rule_1=population_parents[i]
        rule_2=population_parents[i+1]

        change_columns=np.random.randint(2, size=(1, 15))
        change_rows=np.random.randint(2, size=(1, 15))

        for x in range(len(change_columns)):
            if change_columns[0][x]==1:
                c=copy.copy(rule_1.rules_grid[:, x:x+1])
                rule_1.rules_grid[:, x:x+1]=rule_2.rules_grid[:,x:x+1]
                rule_2.rules_grid[:, x:x+1]=c
            if change_rows[0][x]==1:
                c=copy.copy(rule_1.rules_grid[x:x+1, :])
                rule_1.rules_grid[x:x+1, :]=rule_2.rules_grid[x:x+1, :]
                rule_2.rules_grid[x:x+1, :]=c
        
        rule_1=mutation(rule_1, chance_for_mutation)
        rule_2=mutation(rule_2, chance_for_mutation)

        new_population.append(rule_1)
        new_population.append(rule_2)
        new_fitness_func.append(fitness_function(rule_1, distance_grid))
        new_fitness_func.append(fitness_function(rule_1, distance_grid))


    return new_population, new_fitness_func



def genetic_algorithm(distance_grid, 
                      population, 
                      fitness_func, 
                      number_of_population, 
                      chance_for_mutation, 
                      number_of_generation):
    
    if number_of_population<len(population):
        population[number_of_population:len(population)]=[]
    temperature=get_temperature(number_of_generation)

    for i in range(number_of_generation):

        norm_fitness_func=normalize_fitness(fitness_func)
        population, fitness_func = genetic_algorithm_iteration(distance_grid,
                                                               population,
                                                               norm_fitness_func,
                                                               chance_for_mutation*temperature[i])
        

        