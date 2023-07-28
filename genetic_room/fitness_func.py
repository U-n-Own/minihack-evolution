"""
In this file we define all the fitness function that we use
to give one score for each rule throughout the genetic algorithm.
"""

import numpy as np
import math
from utility_func import movement_dictionary

def find_distance_grid(x_goal_position: int, y_goal_position: int):

    distance_grid=np.zeros((15,15), int)

    for x in range(15):
        for y in range(15):
            distance_grid[x][y]=max(np.abs(x-x_goal_position), np.abs(y-y_goal_position))
    
    return distance_grid

def single_position_score(distance_grid: np.ndarray, x_start: int, y_start: int, movement: int):

    x_after=x_start+movement_dictionary[movement][0]
    y_after=y_start+movement_dictionary[movement][1]

    distance_before=distance_grid[x_start][y_start]
    distance_after=distance_grid[x_after][y_after]

    if distance_after!=distance_before:
        single_score=(distance_before-distance_after)/math.sqrt(distance_before)
    else :
        single_score=(-1)/(5*math.sqrt(distance_before))
    
    return single_score*10


def fitness_function(movement, distance_grid: np.ndarray):

    score=0

    for x in range(15):
        for y in range(15):
            if distance_grid[x][y]!=0:
                score=score+single_position_score(distance_grid, x, y, movement.rules_grid[x][y])*(1/pow(2, distance_grid[x][y]-1))
    
    return score


