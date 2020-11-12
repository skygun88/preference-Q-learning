from environment import Env
from agent import CeilingLightAgent
import sys

class Coordinator:
    def __init__(self, ceilingAgent):
        self.NofAgents = 6
        self.ceiling = ceilingAgent

        

    def getActions(self, state):
        ceiling_action = self.ceiling.get_action(state)




    def learnAgents(self, state, actions, rewards, next_state):
        self.ceiling.learn(state, actions[0], rewards[0], next_state)



if __name__ == '__main__':
    ''' Define the user and task '''
    user, task = sys.argv[1], sys.argv[2]

    ''' Define Environment '''
    env = Env()

    ''' Define all agents '''
    ceiling = CeilingLightAgent(user, task)
    # Other agents will be added soon

    ''' Define coordinator '''
    coordinator = Coordinator(ceiling)

    for episode in range(30):
        state = env.reset()

        '''All agent do an action'''
        actions = coordinator.getActions(state)

        '''State update & Get feedback(reward) from user'''
        next_state, rewards, done = env.step(actions)

        ''' Send each reward to each agent and learn all agent in distributed manner '''
        coordinator.learnAgents(state, actions, rewards, next_state)
        state = next_state

        ''' print current state '''
        env.showState()




