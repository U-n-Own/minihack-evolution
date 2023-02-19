import gym
import minihack
import numpy as np
from typing import List
import random
import math
import pygad
from operator import itemgetter
from src.utilities import search_goal
from fitness_func import fitness, normalize_fitness


class Rule:
    def __init__(self, number_of_moves=1, x_start=0, y_start=0):
        possible_movements = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if (x, y) != (0, 0)]
        #possible_movements = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.position = (random.randrange(0 + x_start, 15 + x_start), random.randrange(0 + y_start, 15 + y_start))
        self.movement = []
        for i in range(number_of_moves):
            self.movement.append(random.choice(possible_movements))

    def is_good(self, x_start=3, y_start=32):
        (x, y) = self.position
        for (movement_x, movement_y) in self.movement:
            (x_after, y_after) = (x + movement_x, y + movement_y)
            if not ((0 + x_start, 0 + y_start) <= (x_after, y_after) < (15 + x_start, 15 + y_start)):
                return False
            (x, y) = (x_after, y_after)
        return True

    def __str__(self):
        return f"posizione: {self.position}, movimento: {self.movement}"

    def fitness(self):
        return -np.infty

    def __lt__(self, other):
        return self.fitness <= other.fitness


def generate_initial_population(environment, number_of_genes, number_of_moves=1):
    room = environment.reset()
    # finding the indexes from where the room starts
    (x_start, y_start) = (np.where(room["chars"] != 32)[0][0], np.where(room["chars"] != 32)[1][0],)

    # creating a number of good rules and compute their fitness

    rules = []
    fitness_list = []
    for i in range(number_of_genes):
        while True:
            rules.append(Rule(number_of_moves=number_of_moves, x_start=x_start, y_start=y_start))
            if rules[i].is_good(x_start, y_start):
                break
            rules.pop()
        fitness_list.append(fitness(rules[i], room["chars"]))
    # normalizing fitness to obtain a probability
    fitness_list_norm = normalize_fitness(fitness_list)
    return rules, fitness_list, fitness_list_norm
