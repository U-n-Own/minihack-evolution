""" Library in which we implement some fitness function for our agent """


import numpy as np


#Class for the fitness function
class FitnessFunction:
    
    def __init__(self):
        pass
    
    def _manatthan_distance(self, x1, y1, x2, y2):
    
        return np.abs(x1 - x2) + np.abs(y1 - y2)
    
    def _euclidean_distance(self, x1, y1, x2, y2):
        
        return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)    

    def evaluate_fitness_euclidean(self, agent, room):
        
        x1, y1 = agent.room.agent_position
        x2, y2 = agent.room.flag_position
        
        return self._euclidean_distance(x1, y1, x2, y2)