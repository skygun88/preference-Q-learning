import random
from environment import *

def getUserActions():
    # Ceiling Light
    ceilingAct = input('[Ceiling Light] Please the select action by typing the number [0, 1, 2] = [Still/OFF/ON] ')
    while not (ceilingAct in '012' and len(ceilingAct) == 1):
        ceilingAct = input('[Ceiling Light] Wrong input - Type a number [0, 1, 2] = [Still/OFF/ON] ')

    # Stand Light
    standAct = input('[Stand Light] Please the select action by typing the number [0, 1, 2] = [Still/OFF/ON] ')
    while not (standAct in '012' and len(standAct) == 1):
        standAct = input('[Stand Light] Wrong input - Type a number [0, 1, 2] = [Still/OFF/ON] ')

    # AC
    acAct = input('[Aircon] Please the select action by typing the number [0, 1, 2, 3, 4] = [Still/OFF/ON/UP/DOWN] ')
    while not (acAct in '01234' and len(acAct) == 1):
        acAct = input('[Aircon] Wrong input - Type a number [0, 1, 2, 3, 4] = [Still/OFF/ON/UP/DOWN] ')

    # Fan
    fanAct = input('[Fan] Please the select action by typing the number [0, 1, 2, 3, 4] = [Still/OFF/ON/UP/DOWN] ')
    while not (fanAct in '01234' and len(fanAct) == 1):
        fanAct = input('[Fan] Wrong input - Type a number [0, 1, 2, 3, 4] = [Still/OFF/ON/UP/DOWN] ')

    # TV
    tvAct = input('[TV] Please the select action by typing the number [0, 1, 2] = [Still/OFF/ON] ')
    while not (tvAct in '012' and len(tvAct) == 1):
        tvAct = input('[TV] Wrong input - Type a number [0, 1, 2] = [Still/OFF/ON] ')

    # Speaker
    speakerAct = input('[Speaker] Please the select action by typing the number [0, 1, 2] = [Still/UP/DOWN] ')
    while not (speakerAct in '012' and len(speakerAct) == 1):
        speakerAct = input('[Speaker] Wrong input - Type a number [0, 1, 2] = [Still/UP/DOWN] ')


    user_actions = (ceilingAct, standAct, acAct, fanAct, tvAct, speakerAct)
    user_actions = tuple(map(lambda x: int(x), user_actions))

    return user_actions


def calculateRewards(state, actions, next_state, final_state):
    ceiling, stand, ac, fan, tv, speaker = 0, 1, 2, 3, 4, 5
    agent_offset = 4
    result = [0, 0, 0, 0, 0, 0]
    # Ceiling
    result[ceiling] = -1 if next_state[ceiling+agent_offset] != final_state[ceiling+agent_offset] else 1
    # Stand
    result[stand] = -1 if next_state[stand+agent_offset] != final_state[stand+agent_offset] else 1
    # Aircon
    if actions[ac] == 0 or actions[ac] == 1:
        result[ac] = -1 if next_state[ac+agent_offset] != final_state[ac+agent_offset] else 1
    elif actions[ac] == 2 or actions[ac] == 3:
        result[ac] = -1 if next_state[ac+agent_offset] > final_state[ac+agent_offset] else 1
    elif actions[ac] == 4:
        result[ac] = -1 if next_state[ac+agent_offset] < final_state[ac+agent_offset] else 1
    # Fan
    result[fan] = -1 if next_state[fan+agent_offset] != final_state[fan+agent_offset] else 1
    # TV
    result[tv] = -1 if next_state[tv+agent_offset] != final_state[tv+agent_offset] else 1
    #Speaker
    if actions[speaker] == 0:
        result[speaker] = -1 if next_state[speaker+agent_offset] != final_state[speaker+agent_offset] else 1
    elif actions[speaker] == 1:
        result[speaker] = -1 if next_state[speaker+agent_offset] > final_state[speaker+agent_offset] else 1
    elif actions[speaker] == 2:
        result[speaker] = -1 if next_state[speaker+agent_offset] < final_state[speaker+agent_offset] else 1
    
    return result

def readingUser(state, env: Env):
    preferable_environment = [0, 2, 2, 2]
    curr_state = state[:]
    result = [0, 0, 0, 0, 0, 0]
    brightness_group = [('ceiling', (4, 0)), ('stand', (5, 1)), ('tv', (8, 4))]
    tem_group = [('ac', (6, 2)), ('fan', (7, 3))]
    sound_group = [('ac', (6, 2)), ('fan', (7, 3)), ('speaker', (9, 5))]
    random.shuffle(brightness_group)
    random.shuffle(tem_group)

    ''' Brightness setup '''
    for agent in brightness_group:
        if agent[0] == 'ceiling' or agent[0] == 'stand':
            if preferable_environment[2] > curr_state[2]:
                if curr_state[agent[1][0]] == 0:
                    result[agent[1][1]] = 2
                    curr_state[agent[1][0]] == 1
                    curr_state[2] = env.calculateBrightness(curr_state[0], curr_state[4], curr_state[5], curr_state[8])
            
        elif agent[0] == 'tv':
            if curr_state[agent[1][0]] == 1:
                result[agent[1][1]] = 1
                curr_state[agent[1][0]] == 0
                curr_state[2] = env.calculateBrightness(curr_state[0], curr_state[4], curr_state[5], curr_state[8])

    
    for agent in tem_group:
        if agent[0] == 'ac':
            if preferable_environment[1] > curr_state[1]+1: 
                ''' Need to Aircon down '''
                if curr_state[agent[1][0]] > 0:
                    result[agent[1][1]] = 4
                    curr_state[agent[1][0]] = env.executeAC(curr_state[agent[1][0]], result[agent[1][1]])
                    curr_state[2] = env.calculateTemperature(curr_state[0], curr_state[6], curr_state[7])
            
            elif preferable_environment[1] < curr_state[1]-1:
                ''' Need to Aircon up '''
                if curr_state[agent[1][0]] < 3:
                    result[agent[1][1]] = 3
                    curr_state[agent[1][0]] = env.executeAC(curr_state[agent[1][0]], result[agent[1][1]])
                    curr_state[2] = env.calculateTemperature(curr_state[0], curr_state[6], curr_state[7])

        elif agent[0] == 'fan':
            if preferable_environment[1] > curr_state[1]: 
                ''' Need to Fan down '''
                if curr_state[agent[1][0]] > 0:
                    result[agent[1][1]] = curr_state[agent[1][0]]
                    curr_state[agent[1][0]] = env.executeFan(curr_state[agent[1][0]], result[agent[1][1]])
                    curr_state[2] = env.calculateTemperature(curr_state[0], curr_state[6], curr_state[7])
            
            elif preferable_environment[1] < curr_state[1]:
                ''' Need to Fan up '''
                if curr_state[agent[1][0]] < 3:
                    result[agent[1][1]] = curr_state[agent[1][0]] + 2
                    curr_state[agent[1][0]] = env.executeFan(curr_state[agent[1][0]], result[agent[1][1]])
                    curr_state[2] = env.calculateTemperature(curr_state[0], curr_state[6], curr_state[7])
    
    ''' Sound level setup'''
    agent = sound_group[0]
    if agent[0] == 'speaker':
        if preferable_environment[3] < curr_state[3]:
            if curr_state[agent[1][0]] > 0:
                result[agent[1][1]] = 2
                curr_state[agent[1][0]] = env.executeSpeaker(curr_state[agent[1][0]], result[agent[1][1]])
                curr_state[1] = env.calculateSoundlevel(curr_state[6], curr_state[7], curr_state[9])

    return result