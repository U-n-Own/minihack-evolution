from typing import List
import random

class Rule:
    '''
    The class Rule generates a couple (position, movement)
    Each rule represents an individual (state) of the population of our genetic algorithm
    '''

    agent_position: List[int, int]   #The position of the agent in the 15x15 room
    agent_movement: int              #The movement that the agent must do when is in agent_position

    def __init__(self, index_matrix: List[int, int]):
        '''
        Initiliaze a random position and random movement
        index_matrix represent the start position of the 15x15 room when is represented by a 21x79 matrix 
        '''

        self.agent_position[0]=random.choice(range(index_matrix[0], index_matrix[0]+15))
        self.agent_position[1]=random.choice(range(index_matrix[1], index_matrix[1]+15))
        self.agent_movement=random.choice([0, 1, 2, 3])  