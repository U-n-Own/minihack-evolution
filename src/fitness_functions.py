""" Library in which we implement some fitness function for our agent """


import numpy as np


def fitness_func_1(agent_pos_before_rule, agent_pos_after_rule, goal_pos):
    """
    Function we discussed, take the distance before and after compute the difference and 
    multiply the result for a monotone function
    TODO: Check if implementation is correct
    """
    
    x1, y1 = agent_pos_before_rule
    x2, y2 = agent_pos_after_rule
    goal_1, goal_2 = goal_pos
    
    #Maybe use lambda function for mahattan distance
    distance_before = np.abs(x1 - goal_1) + np.abs(y1 - goal_2)
    distance_after = np.abs(x2 - goal_1) + np.abs(y2 - goal_2)
    
    #return a lambda function
    fitness = (distance_before - distance_after) * 1/(distance_before)
    
    return fitness
    
# How is defined as example in the documentation
    
def fitness_func(solution, solution_idx):
    # The fitness function calulates the sum of products between each input and its corresponding weight.
    output = numpy.sum(solution*function_inputs)
    # The value 0.000001 is used to avoid the Inf value when the denominator numpy.abs(output - desired_output) is 0.0.
    fitness = 1.0 / (numpy.abs(output - desired_output) + 0.000001)
    
    return fitness

#Class for the fitness function
class FitnessFunction:
    
    def __init__(self):
        pass
    
    def fitness_func_0(self, agent_pos_before_rule, agent_pos_after_rule, goal_pos):
        """
        Function we discussed, take the distance before and after compute the difference and 
        multiply the result for a monotone function
        TODO: Check if implementation is correct
        """
        
        x1, y1 = agent_pos_before_rule
        x2, y2 = agent_pos_after_rule
        goal_1, goal_2 = goal_pos
        
        #Maybe use lambda function for mahattan distance
        distance_before = np.abs(x1 - goal_1) + np.abs(y1 - goal_2)
        distance_after = np.abs(x2 - goal_1) + np.abs(y2 - goal_2)
        
        #return a lambda function
        fitness = (distance_before - distance_after) * 1/(distance_before)
    
        return fitness
    
    def _manatthan_distance(self, x1, y1, x2, y2):
    
        return np.abs(x1 - x2) + np.abs(y1 - y2)
    
    def _euclidean_distance(self, x1, y1, x2, y2):
        
        return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)    

    def evaluate_fitness_euclidean(self, agent, room):
        """TODO: This need to be changed to fit the minihack environment """        

        x1, y1 = agent.room.agent_position
        x2, y2 = agent.room.flag_position
        
        return self._euclidean_distance(x1, y1, x2, y2)