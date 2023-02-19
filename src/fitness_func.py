from src.utilities import search_goal
import numpy as np


def fitness(rule, environment):
    if not rule.is_good():
        fit = 0
        return fit
    x_after, y_after = rule.position
    for (mv_x, mv_y) in rule.movement:
        x_after += mv_x
        y_after += mv_y
    goal_x, goal_y = search_goal(environment)
    goal_x=goal_x[0]
    goal_y=goal_y[0]
    x, y = rule.position
    distance_before = np.abs(x - goal_x) + np.abs(y - goal_y)
    distance_after = np.abs(x_after - goal_x) + np.abs(y_after - goal_y)
    if distance_before != 0:
        fit = (distance_before - distance_after)/np.sqrt(distance_before)
        fit = fit + 2
    else:
        fit = 0
    return fit

def normalize_fitness(fitness_list):
    sum_fit = np.sum(fitness_list)
    fitness_list = np.divide(fitness_list , sum_fit)
    return fitness_list