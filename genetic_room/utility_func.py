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
int_to_words = {
    0 : "north",
    1 : "east",
    2 : "south",
    3 : "west",
    4 : "north-east",
    5 : "south-east",
    6 : "south-west",
    7 : "north-west",
}

int_to_coord = {
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


def search_environment_indexes(environment:np.ndarray):
    # return the minimum (row, col) where  environment[row, col] = 32, as a tuple
    if len(np.where(environment==32)[0])==0:
        print("WARNING: environment is empty")
        return None
    indexes= np.where(environment==32)
    return indexes[0][0], indexes[1][0]


def search_environment_agent_position(environment: np.ndarray):
    '''
    Return agent position inside the environment.
    MiniHack passes us the position of the agent in the array with the 
    value of 64, which in ASCII turns into @.
    '''
    indexes = np.where(environment == 64)
    if len(indexes[0]) > 1:
        print("WARNING: more than one agent in the environment")
    if len(indexes[0]) == 0:
        print("WARNING: no agent in the environment")
        return None
    return indexes[0][0], indexes[1][0]

def search_environment_goal_position(environment: np.ndarray):
    """ 
    Return staircase position inside the environment.
    MiniHack passes us the position of the stairs going down in the matrix 
    with the value of 62, which in ASCII turns into >.
    """
    if len(np.where(environment == 62)[0]) > 1:
        print("WARNING: more than one goal in the environment")
    if len(np.where(environment == 62)[0]) == 0:
        print("WARNING: no goal in the environment")
        return None

    indexes = np.where(environment == 62)
    return indexes[0][0], indexes[1][0]


    