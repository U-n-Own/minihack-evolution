"""
In this file we define the class that defines the task rules. 
Each rule tells us exactly how the agent should move along the room
"""

import gym 
import minihack
import numpy as np
import random
from typing import List
from utility_func import movement_dictionary, step_dictionary, inverted_step_dictionary

arrow_dictionary = {
    0 : "\u2191",
    1 : "\u2192",
    2 : "\u2193",
    3 : "\u2190",
    4 : "\u2197",
    5 : "\u2198",
    6 : "\u2199",
    7 : "\u2196",
}

class Rule:

    rules_grid: np.ndarray

    def __init__(self):
        self.rules_grid = np.random.randint(8, size=(15,15))

        self.rules_grid=self.is_good()
  

      
    def is_good(self):

        for x in range(0, 15):

            while movement_dictionary[step_dictionary[self.rules_grid[0][x]]][0]==-1:
                self.rules_grid[0][x]=random.randint(0,7)
            while movement_dictionary[step_dictionary[self.rules_grid[14][x]]][0]==1:
                self.rules_grid[14][x]=random.randint(0,7)
            while movement_dictionary[step_dictionary[self.rules_grid[x][0]]][1]==-1:
                self.rules_grid[x][0]=random.randint(0,7)
            while movement_dictionary[step_dictionary[self.rules_grid[x][14]]][1]==1:
                self.rules_grid[x][14]=random.randint(0,7)
        
        while movement_dictionary[step_dictionary[self.rules_grid[0][0]]][0]==-1 or movement_dictionary[step_dictionary[self.rules_grid[0][0]]][1]==-1:
                self.rules_grid[0][0]=random.randint(0,7)
        while movement_dictionary[step_dictionary[self.rules_grid[14][14]]][0]==1 or movement_dictionary[step_dictionary[self.rules_grid[14][14]]][1]==1:
                self.rules_grid[14][14]=random.randint(0,7)
        while movement_dictionary[step_dictionary[self.rules_grid[0][14]]][0]==-1 or movement_dictionary[step_dictionary[self.rules_grid[0][14]]][1]==1:
                self.rules_grid[0][14]=random.randint(0,7)
        while movement_dictionary[step_dictionary[self.rules_grid[14][0]]][0]==1 or movement_dictionary[step_dictionary[self.rules_grid[14][0]]][1]==-1:
                self.rules_grid[14][0]=random.randint(0,7) 

        return self.rules_grid 
        

    def print_rule(self):
        for x in range(15):
            for y in range(15):
                print(self.rules_grid[x][y], end=" ")
            print("\n")
    
    def print_rule_movement(self):
        for x in range(15):
            for y in range(15):
                print(step_dictionary[self.rules_grid[x][y]], end=" ")
            print("\n")

    def print_rule_arrow(self):
        for x in range(15):
            for y in range(15):
                print(arrow_dictionary[self.rules_grid[x][y]], end=' ')
            print("\n")

def generate_initial_population(size_of_population):

    list_of_rules=[]

    for x in range(size_of_population):
        list_of_rules.append(Rule()) 

        #list_of_rules[x].print_rule()
        #list_of_rules[x].print_rule_movement()

    return list_of_rules