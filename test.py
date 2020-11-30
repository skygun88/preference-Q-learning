from environment import *
from coordinator import *


env = Env()
env.reset()
#env.currState = [3, 1, 3, 1, 0, 1, 0, 3, 0, 0]
env.showState() 

actions = [0, 0, 1, 0, 0, 0]
print(showActions(getUserActions()))
print(isActionsDone(actions))
showActions(actions)
env.step(actions)
