import gym
import minihack
from nle import nethack

env = gym.make("MiniHack-Room-Random-15x15-v0",
            observation_keys=["glyphs", "chars", "colors", "specials"]
)

env.reset()
env.render()

#Do random action between up, down, left, right
MOVE_ACTIONS = tuple(nethack.CompassDirection)

print(MOVE_ACTIONS)

print("\n\n\n\n\n")

env.step(1)
env.render()
