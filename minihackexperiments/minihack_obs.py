import gym
import minihack

#Generate a Room-15x15 task
env=gym.make(
    "MiniHack-Room-Random-15x15-v0",
    observation_keys=("glyphs", "chars", "colors", "specials", "pixel"),
)

 
obs = env.reset() #Generate a new environment and save the describtions arrays in obs
env.render() #Print the room 

#obs contains the "glyphs","chars",...,"pixel" arrays which describe the room
#See documentation for information on arrays
print(obs)

#TODO 
#Search array to see stairs location

print('\n\n\n\n\n')
env.step(1) #Move agent to the north
env.render()
