'''
Rules for the task of finding the exit of the room.
each rule is basically a movement for each cell in the room.
the movement is represented by a number between 0-7.
'''
import time
import random
import numpy as np
import sys
sys.path.append("../")
from utility_func import int_to_coord


class RuleNew:
    def __init__(self):
        """
        initialize the rule as a matrix such that
        each position in the room has a movement associated with it.
        """
        self.rules_grid = np.random.randint(8, size=(15, 15))
        self.fitness = -np.inf

    def get_movement(self, x, y):
        """
        return the movement for a given cell
        """
        return self.rules_grid[x][y]

    def set_movement(self, x, y, movement: int):
        """
        set the movement for a given cell
        """
        if movement < 0 or movement > 7:
            raise ValueError("movement must be between 0 and 7")

        self.rules_grid[x][y] = movement

    def set_fitness(self, fitness):
        self.fitness = fitness


def good_movement(position, movement):
    x, y = position
    dx, dy = int_to_coord[movement]
    # check that the movements do not cause the agent to leave the room
    if 0 <= x + dx <= 14 and 0 <= y + dy <= 14:
        return True
    return False


def good_rule(rule: RuleNew):
    # check only the borders aka x == 14 or y == 14
    return all(good_movement((x, y), rule.get_movement(x, y)) for x in range(15) for y in range(15))


def make_rule_good(rule):
    for x in range(1, 14):
        while not good_movement((0, x), rule.get_movement(0, x)):
            rule.set_movement(0, x, random.randint(0, 7))
        while not good_movement((14, x), rule.get_movement(14, x)):
            rule.set_movement(14, x, random.randint(0, 7))
        while not good_movement((x, 0), rule.get_movement(x, 0)):
            rule.set_movement(x, 0, random.randint(0, 7))
        while not good_movement((x, 14), rule.get_movement(x, 14)):
            rule.set_movement(x, 14, random.randint(0, 7))

    while not good_movement((0, 0), rule.get_movement(0, 0)):
        rule.set_movement(0, 0, random.randint(0, 7))
    while not good_movement((14, 14), rule.get_movement(14, 14)):
        rule.set_movement(14, 14, random.randint(0, 7))
    while not good_movement((0, 14), rule.get_movement(0, 14)):
        rule.set_movement(0, 14, random.randint(0, 7))
    while not good_movement((14, 0), rule.get_movement(14, 0)):
        rule.set_movement(14, 0, random.randint(0, 7))

    return rule


arrow_dictionary = {
    0: "\u2191",
    1: "\u2192",
    2: "\u2193",
    3: "\u2190",
    4: "\u2197",
    5: "\u2198",
    6: "\u2199",
    7: "\u2196",
}


def print_rule(rule):
    for x in range(15):
        for y in range(15):
            print(arrow_dictionary[rule.get_movement(x, y)], end=" ")
        print()


def initial_population(size=100):
    return [RuleNew() for _ in range(size)]  # 100 rules


if __name__ == '__main__':
    start = time.time()
    for i in range(100):
        rule = RuleNew()
        print_rule(rule)
        print('good rule:')
        make_rule_good(rule)
        print_rule(rule)
        print(good_rule(rule))
    print(time.time() - start)  # 0.005 sec per rule
