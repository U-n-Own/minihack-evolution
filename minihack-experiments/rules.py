from typing import List
import random

class Rule:
    '''
    The class Rule generates a couple (position, movement)
    Each rule represents an individual (state) of the population of our genetic algorithm
    '''

    agent_position: List[int, int]   #The position of the agent in the 15x15 room

    #The movement that the agent can perform 
    agent_movement: {0: 'south', 1: 'west', 2: 'north', 3: 'east'}

    def __init__(self, index_matrix: List[int, int]):
        '''
        Initiliaze a random position and random movement
        index_matrix represent the start position of the 15x15 room when is represented by a 21x79 matrix 
        '''

        self.agent_position[0]=random.choice(range(index_matrix[0], index_matrix[0]+15))
        self.agent_position[1]=random.choice(range(index_matrix[1], index_matrix[1]+15))
        
        #Random movement in any direction
        self.agent_movement=random.choice(list(self.agent_movement.keys()))
        