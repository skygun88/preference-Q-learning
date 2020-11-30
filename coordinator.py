from environment import Env
from Agent.CeilingLight import *
from Agent.StandLight import *
import sys
from user import *

class Coordinator:
    def __init__(self, ceilingAgent, standAgent):
        self.NofAgents = 6
        self.ceiling = ceilingAgent
        self.stand = standAgent

    def getActions(self, state):
        ceiling_action = self.ceiling.get_action(state)
        
        return (ceiling_action)


    def learnAgents(self, learningQueue):
        for (state, action, next_state, reward) in learningQueue:
            self.ceiling.learn(state, action, reward[0], next_state)

def isActionsDone(actions):
    for act in actions:
        if act != 0:
            return False
    return True

def showActions(actions):
    ceiling = {0: 'Still', 1: 'OFF', 2: 'ON'}
    stand = {0: 'Still', 1: 'OFF', 2: 'ON'}
    ac = {0: 'Still', 1: 'OFF', 2: 'ON', 3: 'UP', 4: 'DOWN'}
    fan = {0: 'Still', 1: 'OFF', 2: 'LOW', 3: 'MEDIUM', 4: 'HIGH'}
    tv = {0: 'Still', 1: 'OFF', 2: 'ON'}
    speaker = {0: 'Still', 1: 'UP', 2: 'DOWN'}
    act_str = (ceiling, stand, ac, fan, tv, speaker)
    agent_str = ('Ceiling', 'Stand', 'AC', 'Fan', 'TV', 'Speaker')
    result_str = ' / '.join(list(map(lambda x, y, z: f'{z}: {x[y]}', act_str, actions, agent_str)))
    print('Actions - ' + result_str)

if __name__ == '__main__':
    ''' Define the user and task '''
    user, task = sys.argv[1], sys.argv[2]
    counts = []
    ''' Define Environment '''
    env = Env()

    ''' Define all agents '''
    ceiling = CeilingLightAgent(user, task)
    stand = StandLightAgent(user, task)
    # Other agents will be added soon

    ''' Define coordinator '''
    coordinator = Coordinator(ceiling, stand)

    for episode in range(30):
        state = env.reset()
        agent_count = 0
        user_count = 0

        learningQueue = []
        ''' All agent do an action '''
        actions = coordinator.getActions(state)
        next_state = env.step(actions)
        learningQueue.append((state[:], actions[:], next_state[:], 0))
        state = next_state
        while not isActionsDone(actions):
            agent_count += 1
            actions = coordinator.getActions(state)
            next_state = env.step(actions)
            learningQueue.append((state[:], actions[:], next_state[:], 0))
            state = next_state

        ''' Get feedback(reward) from user '''
        user_actions = getUserActions()
        next_state = env.step(user_actions)

        while not isActionsDone(user_actions):
            user_count += 1
            user_actions = getUserActions()
            next_state = env.step(user_actions)
        
        result_state = next_state[:]

        for i in range(learningQueue):
            state, actions, next_state, _ = learningQueue[i]
            reward = calculateRewards(state, actions, next_state, result_state)
            learningQueue[i][3] = reward

        ''' Send each reward to each agent and learn all agent in distributed manner '''
        coordinator.learnAgents(learningQueue)

        ''' print current state '''
        env.showState()
        print(f'Number of actions - Agent: {agent_count}, User: {user_count}')
        counts.append((agent_count, user_count))