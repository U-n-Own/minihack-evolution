''' Plots for ours genetic algorithm ''' 
import matplotlib.pyplot  as  plt
import numpy as  np

def average_fitness_plot(fitnesses, generation_number: int):
    ''' Plots the fitness for each gene after each generation
    fitnesses: list of fitness average for each generation
    '''    
    plt.xlabel( 'Generation' )
    plt.ylabel( 'Average Fitness' )
    
    # make generation number an np.array with integer 1 .. n
    generation_number = [i for i in range(1, generation_number + 1)]
    
    #FIXME:
    plt.plot(generation_number, fitnesses)

    #save plot
    plt.savefig( 'average_fitness.png' )
    