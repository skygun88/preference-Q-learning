from environment import Env
from Agent.CeilingLight import *
from Agent.StandLight import *
from Agent.TV import *
from Agent.Aircon import *
from Agent.Fan import *
from Agent.Speaker import *
import sys
from user import *
from matplotlib import pyplot as plt
import numpy as np

class Coordinator:
    def __init__(self, 
            ceilingAgent: CeilingLightAgent, 
            standAgent: StandLightAgent, 
            acAgent: AirconAgent, 
            fanAgent: FanAgent, 
            tvAgent: TVAgent,
            speakerAgent: SpeakerAgent):
        self.NofAgents = 6
        self.ceiling = ceilingAgent
        self.stand = standAgent
        self.ac = acAgent
        self.fan = fanAgent
        self.tv = tvAgent
        self.speaker = speakerAgent

    def getActions(self, state):
        actions = [0, 0, 0, 0, 0, 0]
        actions[0] = self.ceiling.get_action(state)
        actions[1] = self.stand.get_action(state)
        actions[2] = self.ac.get_action(state)
        actions[3] = self.fan.get_action(state)
        actions[4] = self.tv.get_action(state)
        actions[5] = self.speaker.get_action(state)
        
        return actions


    def learnAgents(self, learningQueue):
        for (state, action, next_state, reward) in learningQueue:
            self.ceiling.learn(state[:], action[0], reward[0], next_state[:])
            self.stand.learn(state[:], action[1], reward[1], next_state[:])
            self.ac.learn(state[:], action[2], reward[2], next_state[:])
            self.fan.learn(state[:], action[3], reward[3], next_state[:])
            self.tv.learn(state[:], action[4], reward[4], next_state[:])
            self.speaker.learn(state[:], action[5], reward[5], next_state[:])

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

def singleUserTest(user, task, iterations):
    ''' Define the user and task '''
    # user, task = sys.argv[1], sys.argv[2]
    counts = []
    ''' Define Environment '''
    env = Env()

    ''' Define all agents '''
    ceiling = CeilingLightAgent(user, task)
    stand = StandLightAgent(user, task)
    ac = AirconAgent(user, task)
    fan = FanAgent(user, task)
    tv = TVAgent(user, task)
    speaker = SpeakerAgent(user, task)
    # Other agents will be added soon

    ''' Define coordinator '''
    coordinator = Coordinator(ceiling, stand, ac, fan, tv, speaker)

    for episode in range(iterations):
        print(f'Episode [{episode}] started')
        state = env.reset()
        # env.showState()
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
            if agent_count > 100:
                break;
            actions = coordinator.getActions(state)
            next_state = env.step(actions)
            learningQueue.append([state[:], actions[:], next_state[:], 0])
            state = next_state

        ''' Get feedback(reward) from user '''
        # user_actions = getUserActions()
        user_actions = readingUser(next_state, env)
        next_state = env.step(user_actions)

        while numberOfActions(user_actions) != 0:
            print('user--')
            user_count += numberOfActions(user_actions)
            # user_actions = getUserActions()
            user_actions = readingUser(next_state, env)
            next_state = env.step(user_actions)
        
        result_state = next_state[:]

        for i in range(len(learningQueue)):
            state, actions, next_state, _ = learningQueue[i]
            reward = calculateRewards(state, actions, next_state, result_state)
            learningQueue[i][3] = reward

        ''' Send each reward to each agent and learn all agent in distributed manner '''
        coordinator.learnAgents(learningQueue)

        ''' print current state '''
        # env.showState()
        # print(f'Number of actions - Agent: {agent_count}, User: {user_count}\n')
        counts.append((agent_count, user_count))
    
    # print('Count result')
    # print(counts)

    agent_counts = list(map(lambda x: x[0], counts))
    user_counts = list(map(lambda x: x[1], counts))
    episode_numbers = list(range(iterations))
    return agent_counts, user_counts


if __name__ == '__main__':
    iterations = 2000
    episode_numbers = list(range(iterations))
    agent_result = np.zeros(iterations)
    user_result = np.zeros(iterations)
    test_num = 20
    for j in range(test_num):
        agent_counts, user_counts = singleUserTest('a', 'b', iterations)
        agent_result += np.array(agent_counts)
        user_result += np.array(user_counts)

    agent_result = agent_result/test_num
    user_result = user_result/test_num

    # print(len(agent_counts), len(user_counts), len(episode_numbers))
    plt.plot(episode_numbers, agent_result, color='red', label='agent')
    plt.plot(episode_numbers, user_result, color='black' ,label='user')
    plt.legend()
    plt.show()
