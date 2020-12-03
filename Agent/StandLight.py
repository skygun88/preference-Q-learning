from collections import defaultdict
import numpy as np
import random


class StandLightAgent:
    def __init__(self, user, task):
        self.user = user
        self.task = task
        self.actions = [0, 1, 2] # Still/OFF/ON
        self.init_lr = 0.75
        self.time_step = 0
        self.discount_factor = 0.25
        self.rewardQueue = [0.0, 0.0, 0.0, 0.0, 0.0] # if there are more than 2 negative reward here, reset the time step.
        self.T_reset = 3
        self.q_table = defaultdict(lambda: [1.0, 0.0, 0.0]) # Still/OFF/ON

    ''' Function to train the agent '''
    def learn(self, state, action, reward, next_state):
        self.time_step = max(self.time_step, 1)
        curr_state = [state[0], state[2], state[4], state[5], state[8]]
        next_state = [next_state[0], next_state[2], next_state[4], next_state[5], next_state[8]]
        curr_state, next_state = str(curr_state), str(next_state)
        q_1 = self.q_table[curr_state][action]
        ''' Update the Q Function '''
        q_2 = reward + self.discount_factor * max(self.q_table[next_state])
        self.q_table[curr_state][action] += (self.init_lr/self.time_step) * (q_2 - q_1)

        ''' Update the reward queue '''
        self.rewardQueue.pop(0)
        self.rewardQueue.append(reward)

        ''' If Number of positive reward is less than T_reset, reset the time step '''
        if len(list(filter(lambda x: x >= 0, self.rewardQueue))) < self.T_reset:
            self.time_step = 0

    ''' Function to get the appropriate action according to the Q-value '''
    def get_action(self, state):
        ''' extract specific state variables which is related to this agent '''
        #curr_state = [state[0], state[2], state[4], state[5], state[8]] # Time, Brightness, Ceiling, Stand, TV
        curr_state = [state[0], state[2], state[4], state[5], state[8]] # Brightness, Ceiling, Stand, TV
        curr_state = str(curr_state)

        ''' select the action according to the Q-value '''
        q_list = self.q_table[curr_state]
        # print(f'Stand: Q values = {q_list}')
        action = arg_max(q_list)
        self.time_step += 1
        return action


def arg_max(q_list):
    max_idx_list = np.argwhere(q_list == np.amax(q_list))
    max_idx_list = max_idx_list.flatten().tolist()
    return random.choice(max_idx_list)