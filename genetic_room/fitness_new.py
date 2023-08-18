import numpy as np
import sys

sys.path.append("../")
from utility_func import int_to_coord
from rules_new import RuleNew, make_rule_good
import time


def find_distance_grid(goal_x, goal_y, shape: tuple = (15, 15)):
    # return a 15x15 matrix of distances from the goal in infinite norm
    # distance_grid[x][y] is the distance from (x,y) to the goal
    # distance_grid[goal_x][goal_y] is 0
    distance_grid = np.zeros(shape, dtype=int)
    for x in range(15):
        for y in range(15):
            distance_grid[x][y] = max(np.abs(x - goal_x), np.abs(y - goal_y))
    return distance_grid


def movement_score(goal, movement, position):
    goal_x, goal_y = goal
    x, y = position
    dx, dy = int_to_coord[movement]
    x_after = x + dx
    y_after = y + dy
    # check that we don't go off the borders
    if x + dx < 0 or x + dx > 14 or y + dy < 0 or y + dy > 14:
        return -1  # lowest possible value
    return max(np.abs(x - goal_x), np.abs(y - goal_y)) - max(np.abs(x_after - goal_x), np.abs(y_after - goal_y))
    # distance before - distance after


def proximity_score(distance):
    # the function that we use to weight the score of each position
    # the closer we are to the goal, the more important the score is
    return 1 / np.sqrt(distance)


class FitnessCalculator:
    def __init__(self, movement_score, proximity_score, distance_grid):
        """"
        movement_score: a function that takes in the goal, the movement, and the position
        and returns a score for that movement
        proximity_score: a function that takes in the distance from the goal and returns a score
        distance_grid: a 15x15 matrix of distances from the goal

        """
        self.movement_score = movement_score
        self.proximity_score = proximity_score
        self.distance_grid = distance_grid
        self.goal = (np.where(distance_grid == 0)[0][0], np.where(distance_grid == 0)[1][0])

    def calculate_fitness(self, rule: RuleNew):
        # calculate the fitness of a rule
        score = 0
        for x in range(15):
            for y in range(15):
                if self.distance_grid[x, y] != 0:
                    # the score should depend on two things:
                    # 1. how much we move towards the goal
                    # 2. how far we are from the goal, with nearer moves being more important
                    # time movement_score and proximity_score separately
                    score += self.movement_score(self.goal, rule.get_movement(x, y), (x, y)) * \
                             self.proximity_score(self.distance_grid[x, y])
        return score

    def fitness_matrix(self, rule:RuleNew):
        # calculate the fitness of each position in the room
        fitness_matrix = np.zeros((15, 15))
        for x in range(15):
            for y in range(15):
                if self.distance_grid[x, y] != 0:
                    fitness_matrix[x, y] = self.movement_score(self.goal, rule.get_movement(x, y), (x, y)) * \
                                           self.proximity_score(self.distance_grid[x, y])

def get_population_fitness(population, fitness_function: FitnessCalculator):
    # return the fitness of each rule in the population
    return [fitness_function.calculate_fitness(rule) for rule in population]


def get_population_fitness_matrix(population, fitness_function: FitnessCalculator):
    # return the fitness of each position in the room for each rule in the population
    return [fitness_function.fitness_matrix(rule) for rule in population]


# show some examples of scores
if __name__ == '__main__':
    rules = [RuleNew() for _ in range(2)]
    fitness_calculator = FitnessCalculator(movement_score, proximity_score, find_distance_grid(0, 0))
    print(get_population_fitness(rules, fitness_calculator))


