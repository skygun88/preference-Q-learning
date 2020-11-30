from environment import Env
from Agent.CeilingLight import *
from Agent.StandLight import *
from Agent.TV import *
import sys
from user import *
from matplotlib import pyplot as plt

class Coordinator:
    def __init__(self, ceilingAgent: CeilingLightAgent, standAgent: StandLightAgent, tvAgent: TVAgent):
        self.NofAgents = 6
        self.ceiling = ceilingAgent
        self.stand = standAgent
        self.tv = tvAgent

    def getActions(self, state):
        actions = [0, 0, 0, 0, 0, 0]
        actions[0] = self.ceiling.get_action(state)
        actions[1] = self.stand.get_action(state)
        actions[4] = self.tv.get_action(state)
        
        return actions


    def learnAgents(self, learningQueue):
        for (state, action, next_state, reward) in learningQueue:
            self.ceiling.learn(state[:], action[0], reward[0], next_state[:])
            self.stand.learn(state[:], action[1], reward[1], next_state[:])
            self.tv.learn(state[:], action[4], reward[4], next_state[:])

def numberOfActions(actions):
    result = 0
    for act in actions:
        if act != 0:
            result += 1
    return result

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
    iterations = 300
    counts = []
    ''' Define Environment '''
    env = Env()

    ''' Define all agents '''
    ceiling = CeilingLightAgent(user, task)
    stand = StandLightAgent(user, task)
    tv = TVAgent(user, task)
    # Other agents will be added soon

    ''' Define coordinator '''
    coordinator = Coordinator(ceiling, stand, tv)

    for episode in range(iterations):
        print(f'Episode [{episode}] started')
        state = env.reset()
        env.showState()
        agent_count = 0
        user_count = 0

        learningQueue = []
        ''' All agent do an action '''
        actions = coordinator.getActions(state)
        next_state = env.step(actions)
        learningQueue.append([state[:], actions[:], next_state[:], 0])
        state = next_state
        while numberOfActions(actions) != 0:
            agent_count += numberOfActions(actions)
            actions = coordinator.getActions(state)
            next_state = env.step(actions)
            learningQueue.append([state[:], actions[:], next_state[:], 0])
            state = next_state

        ''' Get feedback(reward) from user '''
        #user_actions = getUserActions()
        user_actions = readingUser(next_state)
        next_state = env.step(user_actions)

        while numberOfActions(user_actions) != 0:
            user_count += numberOfActions(user_actions)
            #user_actions = getUserActions()
            user_actions = readingUser(next_state)
            next_state = env.step(user_actions)
        
        result_state = next_state[:]

        for i in range(len(learningQueue)):
            state, actions, next_state, _ = learningQueue[i]
            reward = calculateRewards(state, actions, next_state, result_state)
            learningQueue[i][3] = reward

        ''' Send each reward to each agent and learn all agent in distributed manner '''
        coordinator.learnAgents(learningQueue)

        ''' print current state '''
        env.showState()
        print(f'Number of actions - Agent: {agent_count}, User: {user_count}\n')
        counts.append((agent_count, user_count))
    
    print('Count result')
    print(counts)

    agent_counts = list(map(lambda x: x[0], counts))
    user_counts = list(map(lambda x: x[1], counts))
    episode_numbers = list(range(iterations))

    print(len(agent_counts), len(user_counts), len(episode_numbers))
    plt.plot(episode_numbers, agent_counts, label='agent')
    plt.plot(episode_numbers, user_counts, label='user')
    plt.show()
