# This is a file to test gym enviroments and minihack from this repo: https://github.com/facebookresearch/minihack
import gym
import minihack
from nle import nethack

MOVE_ACTIONS = tuple(nethack.CompassDirection)
NAVIGATE_ACTIONS = MOVE_ACTIONS

env = gym.make(
    "MiniHack-Room-15x15-v0",
    actions=NAVIGATE_ACTIONS,
)


