"""
In this file we define all the additional functions and 
dictionaries that we use throughout the program.
"""

import numpy as np
from typing import List


"""
Dictionary for movements. We have three ways to describe movements:
-1: integers between 0 and 7, as step is defined in minihack
-2: in words, for a quick understanding of where one moves
-3: in coordinates, to understand how one moves on the matrix representing the room
"""
step_dictionary = {
    0 : "north",
    1 : "east",
    2 : "south",
    3 : "west",
    4 : "north-east",
    5 : "south-east",
    6 : "south-west",
    7 : "north-west",
}

movement_dictionary = {
    0 : [-1, 0],
    1 : [0, 1],
    2 : [1,0],
    3 : [0,-1],
    4 : [-1,1],
    5 : [1, 1],
    6 : [1, -1],
    7 : [-1, -1],
}

#Functions

def print_room(environment):
#Print the room in ASCII characters. 
    
    for row in range(len(environment[:,1])):
        for col in range(len(environment[1,:])):
            print(chr(environment[row][col]), end=' ') 
        print('\n')


def search_environment_indexes(environment):
#We search the indexes to find the 15x15 submatrix representing the MiniHack task room.

    for row in range(len(environment[:,1])):
        for col in range(len(environment[1,:])):
            if int(environment[row][col]) != 32:
                return row, col      


def search_environment_agent_position(environment: np.ndarray):
    '''
    Return agent position inside the environment.
    MiniHack passes us the position of the agent in the array with the 
    value of 64, which in ASCII turns into @.
    '''
    for row in range(len(environment[:,1])):
        for col in range(len(environment[1,:])):
            if int(environment[row][col]) == 64:  
                return row, col


def search_environment_goal_position(environment: np.ndarray):
    """ 
    Return staircase position inside the environment.
    MiniHack passes us the position of the stairs going down in the matrix 
    with the value of 62, which in ASCII turns into >.
    """
    for row in range(len(environment[:,1])):
        for col in range(len(environment[1,:])):
            if int(environment[row][col]) == 62:
                return row, col


    