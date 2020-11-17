import random

class Env:
    def __init__(self):
        ''' All state data '''
        ''' Environment state '''
        self.TimeOfDay = [0, 1, 2, 3] # Morning/Noon/Evening/Night
        self.Temperature = [0, 1, 2, 3, 4] # Level 0-4
        # self.Humidity = [0, 1, 2] # Level 0-2
        self.Brightness = [0, 1, 2, 3] # Level 0-4
        self.Soundlevel = [0, 1, 2, 3, 4] # Level 0-5

        ''' Agent state '''
        self.CeilingLight = [0, 1] # OFF/ON
        self.StandLight = [0, 1] # OFF/ON
        self.AC = [0, 1, 2, 3] # OFF/LOW/MEDIUM/HIGH
        self.Fan = [0, 1, 2, 3] # OFF/LOW/MEDIUM/HIGH
        self.TV = [0, 1] # OFF/ON
        self.Speaker = [0, 1, 2, 3] # OFF/LOW/MEDIUM/HIGH

        ''' Agent actions '''
        self.CeilingLightActions = [0, 1, 2] # Still/OFF/ON
        self.StandLightActions = [0, 1, 2] # Still/OFF/ON
        self.ACActions = [0, 1, 2, 3, 4] # Still/OFF/ON/UP/DOWN
        self.FanActions = [0, 1, 2, 3, 4] # Still/OFF/LOW/MEDIUM/HIGH
        self.TVActions = [0, 1, 2] # Still/OFF/ON
        self.SpeakerActions = [0, 1, 2] # Still/UP/DOWN

        ''' Current states '''
        self.currState = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # 0: Time, 1: Temperature, 2: Brightness, 3: Sound level, 4: Ceiling, 5: Stand, 6: AC, 7: Fan, 8: TV, 9: Speak
        self.agents = {'ceiling': 4, 'stand': 5, 'ac': 6, 'fan': 7, 'tv': 8, 'speaker': 9}
        # Ceilling: 4, Stand: 5, AC: 6, Fan: 7, TV: 8, Speaker: 9

    ''' Function to calculate the temperature according to AC and Fan '''
    def calculateTemperature(self, time, ac, fan):
        time_to_tem = {0: 3, 1: 4, 2: 2, 3: 2}
        ac_to_tem = {0: 0, 1: -1, 2: -2, 3: -3}
        fan_to_tem = {0: 0, 1: -0.5, 2: -1, 3: -1.5}
        temperature = int(max(min(time_to_tem[time] + ac_to_tem[ac] + fan_to_tem[fan], 4), 0))
        return temperature

    ''' Function to calculate the brightness according to time of day, lights, and tv '''
    def calculateBrightness(self, time, ceiling, stand, tv):
        time_to_brightness = {0: 3, 1: 2, 2: 1, 3: 0}
        ceiling_to_brightness = {0: 0, 1: 2}
        stand_to_brightness = {0: 0, 1: 2}
        tv_to_brightness = {0: 0, 1: 1}
        brightness = int(max(min(time_to_brightness[time] + ceiling_to_brightness[ceiling] + stand_to_brightness[stand] + tv_to_brightness[tv], 3), 0))
        return brightness

    ''' Function to calculate the sound level according to AC, fan, and speaker '''
    def calculateSoundLevel(self, ac, fan, speaker):
        ac_to_sound = {0: 0, 1: 0.5, 2: 1, 3: 1.5}
        fan_to_sound = {0: 0, 1: 0.5, 2: 0.5, 3: 1}
        speaker_to_sound = {0: 0, 1: 1, 2: 2, 3: 3}
        soundlevel = int(max(min(ac_to_sound[ac] + fan_to_sound[fan] + speaker_to_sound[speaker], 4), 0))
        return soundlevel

    ''' Function to reset the all environment state to random initial state '''
    def reset(self):
        ''' Get random state of each agent '''
        ceiling = random.choice(self.CeilingLight)
        stand = random.choice(self.StandLight)
        ac = random.choice(self.AC)
        fan = random.choice(self.Fan)
        tv = random.choice(self.TV)
        speaker = random.choice(self.Speaker)

        ''' Set the environment depending on the agent's state '''
        time = random.choice(self.TimeOfDay)
        temperature = self.calculateTemperature(time, ac, fan)
        brightness = self.calculateBrightness(time, ceiling, stand, tv)
        sound = self.calculateSoundLevel(ac, fan, speaker)

        self.currState = [time, temperature, brightness, sound, ceiling, stand, ac, fan, tv, speaker]

    ''' Function to update agents' state '''
    def updateAgents(self, actions):
        ceilingAct, standAct, acAct, fanAct, tvAct, speakerAct = actions[0], actions[1], actions[2], actions[3], actions[4], actions[5]
        # Ceiling Light
        if ceilingAct != 0:
            self.currState[self.agents['ceiling']] = ceilingAct - 1
        # Stand Light
        if standAct != 0:
           self.currState[self.agents['stand']] = standAct - 1
        # AC
        if acAct != 0:
            if acAct == 1:
                self.currState[self.agents['ac']] = 0
            if acAct == 2:
                if self.currState[self.agents['ac']] == 0:
                    self.currState[self.agents['ac']] = 2
            if acAct == 3:
                if self.currState[self.agents['ac']] != 0:
                    self.currState[self.agents['ac']] = min(self.currState[self.agents['ac']] + 1, 3)
            if acAct == 4:
                if self.currState[self.agents['ac']] != 0:
                    self.currState[self.agents['ac']] = max(self.currState[self.agents['ac']] - 1, 0)
        # Fan
        if fanAct != 0:
            self.currState[self.agents['fan']] = fanAct - 1
        # TV
        if tvAct != 0:
            self.currState[self.agents['tv']] = standAct - 1
        # Speaker
        if speakerAct != 0:
            if speakerAct == 1:
                self.currState[self.agents['speaker']] = min(self.currState[self.agents['speaker']] + 1, 3)
            if speakerAct == 2:
                self.currState[self.agents['speaker']] = max(self.currState[self.agents['speaker']] - 1, 0)

    ''' Function to update environment state '''
    def updateEnviornment(self):
        currCeiling = self.currState[self.agents['ceiling']]
        currStand = self.currState[self.agents['stand']]
        currAC = self.currState[self.agents['ac']]
        currFan = self.currState[self.agents['fan']]
        currTV = self.currState[self.agents['tv']]
        currSpeaker = self.currState[self.agents['speaker']]
        currTime = self.currState[0]
        ''' Calculate new environment factors '''
        self.currState[1] = self.calculateTemperature(currTime, currAC, currFan)
        self.currState[2] = self.calculateBrightness(currTime, currCeiling, currStand, currTV)
        self.currState[3] = self.calculateSoundLevel(currAC, currFan, currSpeaker)


    ''' Function to move the next time step '''
    def step(self, actions):
        ''' Update the states induced by agents' actions '''
        self.updateAgents(actions)
        self.updateEnviornment()
        updatedState = self.currState[:]

        print('----Current state induced by agents----')
        self.showState()
        print('---------------------------------------')

        ''' Update the statet induced by user's actions '''
        # userActions, done = self.getUserActions()
        # self.updateAgents(userActions)
        nextState = self.getUserFeedback()
        self.currState = nextState[:]
        self.updateEnviornment()
        # nextState = self.currState[:]

        ''' Calculate the reward '''
        rewards = self.calculateRewards(actions, updatedState, nextState)
        return nextState, rewards, done

    def calculateRewards(self, actions, currState, nextState):
        positive = 1
        negative = -1
        feedback = nextState[4:]
        currCeiling, currStand, currAC, currFan, currTV, currSpeaker = currState[4], currState[5], currState[6], currState[7], currState[8], currState[9] 
        nextCeiling, nextStand, nextAC, nextFan, nextTV, nextSpeaker = nextState[4], nextState[5], nextState[6], nextState[7], nextState[8], nextState[9]

        rewards = list(map(lambda x: positive if x==0 else negative, userActions))
        return rewards


    ''' Get user's feedback by using input and return user's actions '''
    def getUserFeedback(self):
        # Ceiling Light
        ceilingState = {'off': 0, 'on': 1}
        standState = {'off': 0, 'on': 1}
        acState = {'off': 0, 'low': 1, 'medium': 2, 'high': 3}
        fanState = {'off': 0, 'low': 1, 'medium': 2, 'high': 3}
        tvState = {'off': 0, 'on': 1}
        speakerState = {'off': 0, 'low': 1, 'medium': 2, 'high': 3}
        dicts = [ceilingState, standState, acState, fanState, tvState, speakerState]

        ceilingFeedback = input('[Ceiling Light] Please the select preferable state. off/on ')
        while not (ceilingFeedback in ceilingState):
            ceilingFeedback = input('[Ceiling Light] Wrong input. off/on ')

        # Stand Light
        standFeedback = input('[Stand Light] Please the select preferable state. off/on ')
        while not (standFeedback in standState):
            standFeedback = input('[Stand Light] Wrong input. off/on ')

        # AC
        acFeedback = input('[Aircon] Please the select preferable state. off/low/medium/high ')
        while not (acFeedback in acState):
            acFeedback = input('[Aircon] Wrong input. off/low/medium/high ')

        # Fan
        fanFeedback = input('[Fan] Please the select preferable state. off/low/medium/high ')
        while not (fanFeedback in fanState):
            fanFeedback = input('[Fan] Wrong input. off/low/medium/high ')

        # TV
        tvFeedback = input('[TV] Please the select preferable state. off/on ')
        while not (tvFeedback in tvState):
            tvFeedback = input('[TV] Wrong input. off/on ')

        # Speaker
        speakerFeedback = input('[Speaker] Please the select preferable state. off/low/medium/high ')
        while not (speakerFeedback in speakerState):
            speakerFeedback = input('[Speaker] Wrong input. off/low/medium/high ')

        done = input('User action is done? y/n ')
        while not (done in 'yn' and len(done) == 1):
            done = input('Wrong input  - y/n ')

        newState = (ceilingFeedback, standFeedback, acFeedback, fanFeedback, tvFeedback, speakerFeedback)
        newState = tuple(map(lambda x, y: x[y], dicts, newState))
        done = {'y': 1, 'n': 0}[done]

        return (newState, done)


    def getUserActions(self):
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
        speakerAct = input('[Speaker] Please the select action by typing the number [0, 1, 2] = [Still/OFF/ON] ')
        while not (speakerAct in '012' and len(speakerAct) == 1):
            speakerAct = input('[Speaker] Wrong input - Type a number [0, 1, 2] = [Still/OFF/ON] ')

        done = input('User action is done? y/n ')
        while not (done in 'yn' and len(done) == 1):
            done = input('Wrong input  - y/n ')

        user_actions = (ceilingAct, standAct, acAct, fanAct, tvAct, speakerAct)
        user_actions = tuple(map(lambda x: int(x), user_actions))
        done = {'y': 1, 'n': 0}[done]

        return (user_actions, done)

    ''' print the current environment states '''
    def showState(self):
        timeToStr = {0: 'Moring', 1: 'Noon', 2: 'Evening', 3: 'Night'}
        ceilingToStr = {0: 'OFF', 1: 'ON'}
        standToStr = {0: 'OFF', 1: 'ON'}
        acToStr = {0: 'OFF', 1: 'LOW', 2: 'MEDIUM', 3: 'HIGH'}
        fanToStr = {0: 'OFF', 1: 'LOW', 2: 'MEDIUM', 3: 'HIGH'}
        tvToStr = {0: 'OFF', 1: 'ON'}
        speakerToStr = {0: 'OFF', 1: 'LOW', 2: 'MEDIUM', 3: 'HIGH'}

        currState = self.currState
        print(f'Current State')
        print(f'[Time of day] {timeToStr[currState[0]]}')
        print(f'[Temperature] Level {currState[1]}')
        print(f'[Brightness] Level {currState[2]}')
        print(f'[Sound Level] Level {currState[3]}')
        print(f'[Ceiling Light] {ceilingToStr[currState[4]]}')
        print(f'[Stand Light] {standToStr[currState[5]]}')
        print(f'[Aircon] {acToStr[currState[6]]}')
        print(f'[Fan] {fanToStr[currState[7]]}')
        print(f'[TV] {tvToStr[currState[8]]}')
        print(f'[Speaker] {speakerToStr[currState[9]]}')
import random

class Env:
    def __init__(self):
        ''' All state data '''
        ''' Environment state '''
        self.TimeOfDay = [0, 1, 2, 3] # Morning/Noon/Evening/Night
        self.Temperature = [0, 1, 2, 3, 4] # Level 0-4
        # self.Humidity = [0, 1, 2] # Level 0-2
        self.Brightness = [0, 1, 2, 3] # Level 0-4
        self.Soundlevel = [0, 1, 2, 3, 4] # Level 0-5

        ''' Agent state '''
        self.CeilingLight = [0, 1] # OFF/ON
        self.StandLight = [0, 1] # OFF/ON
        self.AC = [0, 1, 2, 3] # OFF/LOW/MEDIUM/HIGH
        self.Fan = [0, 1, 2, 3] # OFF/LOW/MEDIUM/HIGH
        self.TV = [0, 1] # OFF/ON
        self.Speaker = [0, 1, 2, 3] # OFF/LOW/MEDIUM/HIGH

        ''' Agent actions '''
        self.CeilingLightActions = [0, 1, 2] # Still/OFF/ON
        self.StandLightActions = [0, 1, 2] # Still/OFF/ON
        self.ACActions = [0, 1, 2, 3, 4] # Still/OFF/ON/UP/DOWN
        self.FanActions = [0, 1, 2, 3, 4] # Still/OFF/LOW/MEDIUM/HIGH
        self.TVActions = [0, 1, 2] # Still/OFF/ON
        self.SpeakerActions = [0, 1, 2] # Still/UP/DOWN

        ''' Current states '''
        self.currState = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # 0: Time, 1: Temperature, 2: Brightness, 3: Sound level, 4: Ceiling, 5: Stand, 6: AC, 7: Fan, 8: TV, 9: Speak
        self.agents = {'ceiling': 4, 'stand': 5, 'ac': 6, 'fan': 7, 'tv': 8, 'speaker': 9}
        # Ceilling: 4, Stand: 5, AC: 6, Fan: 7, TV: 8, Speaker: 9

    ''' Function to calculate the temperature according to AC and Fan '''
    def calculateTemperature(self, time, ac, fan):
        time_to_tem = {0: 3, 1: 4, 2: 2, 3: 2}
        ac_to_tem = {0: 0, 1: -1, 2: -2, 3: -3}
        fan_to_tem = {0: 0, 1: -0.5, 2: -1, 3: -1.5}
        temperature = int(max(min(time_to_tem[time] + ac_to_tem[ac] + fan_to_tem[fan], 4), 0))
        return temperature

    ''' Function to calculate the brightness according to time of day, lights, and tv '''
    def calculateBrightness(self, time, ceiling, stand, tv):
        time_to_brightness = {0: 3, 1: 2, 2: 1, 3: 0}
        ceiling_to_brightness = {0: 0, 1: 2}
        stand_to_brightness = {0: 0, 1: 2}
        tv_to_brightness = {0: 0, 1: 1}
        brightness = int(max(min(time_to_brightness[time] + ceiling_to_brightness[ceiling] + stand_to_brightness[stand] + tv_to_brightness[tv], 3), 0))
        return brightness

    ''' Function to calculate the sound level according to AC, fan, and speaker '''
    def calculateSoundLevel(self, ac, fan, speaker):
        ac_to_sound = {0: 0, 1: 0.5, 2: 1, 3: 1.5}
        fan_to_sound = {0: 0, 1: 0.5, 2: 0.5, 3: 1}
        speaker_to_sound = {0: 0, 1: 1, 2: 2, 3: 3}
        soundlevel = int(max(min(ac_to_sound[ac] + fan_to_sound[fan] + speaker_to_sound[speaker], 4), 0))
        return soundlevel

    ''' Function to reset the all environment state to random initial state '''
    def reset(self):
        ''' Get random state of each agent '''
        ceiling = random.choice(self.CeilingLight)
        stand = random.choice(self.StandLight)
        ac = random.choice(self.AC)
        fan = random.choice(self.Fan)
        tv = random.choice(self.TV)
        speaker = random.choice(self.Speaker)

        ''' Set the environment depending on the agent's state '''
        time = random.choice(self.TimeOfDay)
        temperature = self.calculateTemperature(time, ac, fan)
        brightness = self.calculateBrightness(time, ceiling, stand, tv)
        sound = self.calculateSoundLevel(ac, fan, speaker)

        self.currState = [time, temperature, brightness, sound, ceiling, stand, ac, fan, tv, speaker]

    ''' Function to update agents' state '''
    def updateAgents(self, actions):
        ceilingAct, standAct, acAct, fanAct, tvAct, speakerAct = actions[0], actions[1], actions[2], actions[3], actions[4], actions[5]
        # Ceiling Light
        if ceilingAct != 0:
            self.currState[self.agents['ceiling']] = ceilingAct - 1
        # Stand Light
        if standAct != 0:
           self.currState[self.agents['stand']] = standAct - 1
        # AC
        if acAct != 0:
            if acAct == 1:
                self.currState[self.agents['ac']] = 0
            if acAct == 2:
                if self.currState[self.agents['ac']] == 0:
                    self.currState[self.agents['ac']] = 1
            if acAct == 3:
                if self.currState[self.agents['ac']] != 0:
                    self.currState[self.agents['ac']] = min(self.currState[self.agents['ac']] + 1, 3)
            if acAct == 4:
                if self.currState[self.agents['ac']] != 0:
                    self.currState[self.agents['ac']] = max(self.currState[self.agents['ac']] - 1, 0)
        # Fan
        if fanAct != 0:
            self.currState[self.agents['fan']] = fanAct - 1
        # TV
        if tvAct != 0:
            self.currState[self.agents['tv']] = standAct - 1
        # Speaker
        if speakerAct != 0:
            if speakerAct == 1:
                self.currState[self.agents['speaker']] = min(self.currState[self.agents['speaker']] + 1, 3)
            if speakerAct == 2:
                self.currState[self.agents['speaker']] = max(self.currState[self.agents['speaker']] - 1, 0)

    ''' Function to update environment state '''
    def updateEnviornment(self):
        currCeiling = self.currState[self.agents['ceiling']]
        currStand = self.currState[self.agents['stand']]
        currAC = self.currState[self.agents['ac']]
        currFan = self.currState[self.agents['fan']]
        currTV = self.currState[self.agents['tv']]
        currSpeaker = self.currState[self.agents['speaker']]
        currTime = self.currState[0]
        ''' Calculate new environment factors '''
        self.currState[1] = self.calculateTemperature(currTime, currAC, currFan)
        self.currState[2] = self.calculateBrightness(currTime, currCeiling, currStand, currTV)
        self.currState[3] = self.calculateSoundLevel(currAC, currFan, currSpeaker)


    ''' Function to move the next time step '''
    def step(self, actions):
        ''' Update the states induced by agents' actions '''
        self.updateAgents(actions)
        self.updateEnviornment()
        updatedState = self.currState[:]

        print('----Current state induced by agents----')
        self.showState()
        print('---------------------------------------')

        ''' Update the statet induced by user's actions '''
        # userActions, done = self.getUserActions()
        # self.updateAgents(userActions)
        nextState = self.getUserFeedback()
        self.currState = nextState[:]
        self.updateEnviornment()
        # nextState = self.currState[:]

        ''' Calculate the reward '''
        rewards = self.calculateRewards(actions, updatedState, nextState)
        return nextState, rewards, done

    def calculateRewards(self, actions, currState, nextState):
        positive = 1
        negative = -1
        currCeiling, currStand, currAC, currFan, currTV, currSpeaker = currState[4], currState[5], currState[6], currState[7], currState[8], currState[9] 
        nextCeiling, nextStand, nextAC, nextFan, nextTV, nextSpeaker = nextState[4], nextState[5], nextState[6], nextState[7], nextState[8], nextState[9]
        ceilingReward, standReward, acReward, fanReward, tvReward, speakerReward = positive, positive, positive, positive, positive, positive
        
        if currCeiling != nextCeiling:
            ceilingReward = negative
        if currStand != nextStand:
            standReward = negative
        if currAC != nextAC:
            if currAC < nextAC:
                if actions[0] in (0, 1, 4):
                    acReward = negative
            else:
                if actions[0] in (0, 2, 3):
                    acReward = negative
        if currFan != nextFan:
            fanReward = negative
        if currTV != nextTV:
            tvReward = negative
        if currSpeaker != nextSpeaker:
            if currSpeaker < nextSpeaker:
                if actions[5] in (0, 2):
                    speakerReward = negative
            else:
                if actions[5] in (0, 1):
                    speakerReward = negative
        # rewards = list(map(lambda x: positive if x==0 else negative, userActions))
        rewards = (ceilingReward, standReward, acReward, fanReward, tvReward, speakerReward)
        return rewards


    ''' Get user's feedback by using input and return user's actions '''
    def getUserFeedback(self):
        # Ceiling Light
        ceilingState = {'off': 0, 'on': 1}
        standState = {'off': 0, 'on': 1}
        acState = {'off': 0, 'low': 1, 'medium': 2, 'high': 3}
        fanState = {'off': 0, 'low': 1, 'medium': 2, 'high': 3}
        tvState = {'off': 0, 'on': 1}
        speakerState = {'off': 0, 'low': 1, 'medium': 2, 'high': 3}
        dicts = [ceilingState, standState, acState, fanState, tvState, speakerState]

        ceilingFeedback = input('[Ceiling Light] Please the select preferable state. off/on ')
        while not (ceilingFeedback in ceilingState):
            ceilingFeedback = input('[Ceiling Light] Wrong input. off/on ')

        # Stand Light
        standFeedback = input('[Stand Light] Please the select preferable state. off/on ')
        while not (standFeedback in standState):
            standFeedback = input('[Stand Light] Wrong input. off/on ')

        # AC
        acFeedback = input('[Aircon] Please the select preferable state. off/low/medium/high ')
        while not (acFeedback in acState):
            acFeedback = input('[Aircon] Wrong input. off/low/medium/high ')

        # Fan
        fanFeedback = input('[Fan] Please the select preferable state. off/low/medium/high ')
        while not (fanFeedback in fanState):
            fanFeedback = input('[Fan] Wrong input. off/low/medium/high ')

        # TV
        tvFeedback = input('[TV] Please the select preferable state. off/on ')
        while not (tvFeedback in tvState):
            tvFeedback = input('[TV] Wrong input. off/on ')

        # Speaker
        speakerFeedback = input('[Speaker] Please the select preferable state. off/low/medium/high ')
        while not (speakerFeedback in speakerState):
            speakerFeedback = input('[Speaker] Wrong input. off/low/medium/high ')

        done = input('User action is done? y/n ')
        while not (done in 'yn' and len(done) == 1):
            done = input('Wrong input  - y/n ')

        newState = (ceilingFeedback, standFeedback, acFeedback, fanFeedback, tvFeedback, speakerFeedback)
        newState = tuple(map(lambda x, y: x[y], dicts, newState))
        done = {'y': 1, 'n': 0}[done]

        return (newState, done)


    def getUserActions(self):
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
        speakerAct = input('[Speaker] Please the select action by typing the number [0, 1, 2] = [Still/OFF/ON] ')
        while not (speakerAct in '012' and len(speakerAct) == 1):
            speakerAct = input('[Speaker] Wrong input - Type a number [0, 1, 2] = [Still/OFF/ON] ')

        done = input('User action is done? y/n ')
        while not (done in 'yn' and len(done) == 1):
            done = input('Wrong input  - y/n ')

        user_actions = (ceilingAct, standAct, acAct, fanAct, tvAct, speakerAct)
        user_actions = tuple(map(lambda x: int(x), user_actions))
        done = {'y': 1, 'n': 0}[done]

        return (user_actions, done)

    ''' print the current environment states '''
    def showState(self):
        timeToStr = {0: 'Moring', 1: 'Noon', 2: 'Evening', 3: 'Night'}
        ceilingToStr = {0: 'OFF', 1: 'ON'}
        standToStr = {0: 'OFF', 1: 'ON'}
        acToStr = {0: 'OFF', 1: 'LOW', 2: 'MEDIUM', 3: 'HIGH'}
        fanToStr = {0: 'OFF', 1: 'LOW', 2: 'MEDIUM', 3: 'HIGH'}
        tvToStr = {0: 'OFF', 1: 'ON'}
        speakerToStr = {0: 'OFF', 1: 'LOW', 2: 'MEDIUM', 3: 'HIGH'}

        currState = self.currState
        print(f'Current State')
        print(f'[Time of day] {timeToStr[currState[0]]}')
        print(f'[Temperature] Level {currState[1]}')
        print(f'[Brightness] Level {currState[2]}')
        print(f'[Sound Level] Level {currState[3]}')
        print(f'[Ceiling Light] {ceilingToStr[currState[4]]}')
        print(f'[Stand Light] {standToStr[currState[5]]}')
        print(f'[Aircon] {acToStr[currState[6]]}')
        print(f'[Fan] {fanToStr[currState[7]]}')
        print(f'[TV] {tvToStr[currState[8]]}')
        print(f'[Speaker] {speakerToStr[currState[9]]}')
