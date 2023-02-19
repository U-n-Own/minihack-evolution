import gym
import minihack
from nle import nethack
import numpy as np
from genetic_algorithm import genetic_algorithm
from rules import generate_initial_population
from utilities import search_goal, search_agent
from itertools import product
from rules import Rule
from fitness_func import fitness

env = gym.make("MiniHack-Room-Random-15x15-v0",
               observation_keys=("chars", "colors", "specials", "pixel"), )
room = env.reset()
room = room["chars"]
rules, fitness_list, fitness_list_norm = generate_initial_population(env, 1000)

# creating the rules with the genetic algorithm
rules, fitness_list, fitness_list_norm = genetic_algorithm(environment=room,
                                                           rules=rules,
                                                           fitness_list_norm=fitness_list_norm,
                                                           chance_for_mutation=0,
                                                           number_of_rules=1000,
                                                           number_of_generations=5
                                                           )
movements = {
    (0, 1): 1,  # "east",
    (1, 0): 2,  # "sud",
    (-1, 0): 0,  # "north",
    (0, -1): 3,  # "west",
    (1, 1): 5,  # "south-east",
    (1, -1): 6,  # "south-west",
    (-1, 1): 4,  # "north-east"
    (-1, -1): 7  # "north-west"
}
rev_movements = {k: m for m, k in movements.items()}

for rule, fit in zip(rules, fitness_list):
    rule.fitness = fit

rules.sort(reverse=True)

final_rules = -np.ones_like(room, dtype=int)
theres_rule = np.zeros_like(room, dtype=bool)
counter = 0
for rule in rules:
    if rule.fitness <= 1:
        break
    x, y = rule.position
    if not (theres_rule[x, y]):
        final_rules[x, y] = int(movements[rule.movement[0]])
        theres_rule[x, y] = True
        counter += 1

print("n. mossse buone", counter)
verbose = True
################################################################################################
# # finally move the agent
goal_position = search_goal(room)
goal_position = [goal_position[0][0], goal_position[1][0]]
print(goal_position)

agent_position = search_agent(room)
agent_position = [agent_position[0][0], agent_position[1][0]]
count_moves = 0
ag_x, ag_y = agent_position
while agent_position != goal_position:

    if theres_rule[ag_x, ag_y]:
        step = final_rules[ag_x, ag_y]
        movement = rev_movements[final_rules[ag_x, ag_y]]

        env.step(step)
        if verbose:
            print(f"movimento della forma {movement}")
            print(f"mossa {count_moves} rule")
            env.render()

    else:
        step = np.random.choice(range(8))
        x = env.step(step)
        movement = rev_movements[step]
        if verbose:
            print(f"movimento della forma {movement}")
            print(f"mossa {count_moves} random")
            env.render()

    # aggiorno la posizione dell'agente
    rule = Rule(1)
    rule.position = (ag_x, ag_y)
    rule.movement = [movement]
    print(rule)
    print(rule.is_good())
    if rule.is_good():
        agent_position[0] += movement[0]
        agent_position[1] += movement[1]
    count_moves += 1
    ag_x, ag_y = agent_position
    print(agent_position)
print(f"task completed in {count_moves} moves!")