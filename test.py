from environment import *

env = Env()
env.reset()
env.showState()

actions = [0, 1, 1, 4, 0, 1]
env.step(actions)
