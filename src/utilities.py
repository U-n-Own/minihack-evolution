import numpy as np
def search_goal(environment):
    """
    Search for the goal position in the room matrix
    """
    # the goal position in a minihack environment matrix is codified by a 64

    return  np.where(environment == 62)

def search_agent(environment):
    """
    Search for the agent position in the room matrix
    """
    # the agent position in a minihack environment matrix is codified by a 42
    return np.where(environment == 64)

