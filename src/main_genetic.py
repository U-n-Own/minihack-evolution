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
print(search_goal(room))

# creating the rules with the genetic algorithm
rules, fitness_list, fitness_list_norm = genetic_algorithm(environment=room,
                                                           rules=rules,
                                                           fitness_list_norm=fitness_list_norm,
                                                           chance_for_mutation=0.01,
                                                           number_of_rules=1000,
                                                           number_of_generations=5
                                                           )
print(fitness_list)
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
    if rule.fitness <= 2:
        break
    x, y = rule.position
    if not (theres_rule[x, y]):
        final_rules[x, y] = int(movements[rule.movement[0]])
        theres_rule[x, y] = True
        print(rule)
        print(search_goal(room))
        print(rule.fitness)
        counter += 1

print("n. mossse buone", counter)
#
# # finally move the agent
print(final_rules[3:18, 32:47])
goal_position = search_goal(room)
print(goal_position)
agent_position = search_agent(room)
agent_position = [agent_position[0][0], agent_position[1][0]]
count_moves = 0

while agent_position != goal_position:
    ag_x, ag_y = agent_position
    ag_x = int(ag_x)
    ag_y = int(ag_y)
    if theres_rule[ag_x, ag_y]:
        step = final_rules[ag_x, ag_y]
        movement = rev_movements[final_rules[ag_x, ag_y]]

        env.step(step)
        print(f"movimento della forma {movement}")
        print(f"mossa {count_moves} rule")
        env.render()
        # aggiorno la posizione dell'agente

        rule = Rule(1)
        rule.position = (ag_x, ag_y)
        rule.movement = [movement]
        if rule.is_good(3, 32):
            agent_position[0] += movement[0]
            agent_position[1] += movement[1]
        count_moves += 1
    else:
        step = np.random.choice(range(8))
        env.step(step)
        movement = rev_movements[step]

        print(f"movimento della forma {movement}")
        print(f"mossa {count_moves} random")
        env.render()
        # aggiorno la posizione dell'agente

        rule = Rule(1)
        rule.position = (ag_x, ag_y)
        rule.movement = [movement]
        if rule.is_good(3, 32):
            agent_position[0] += movement[0]
            agent_position[1] += movement[1]
        count_moves += 1
