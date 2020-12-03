import random

class Env:
    def __init__(self):
        ''' All state data '''
        ''' Environment state '''
        self.TimeOfDay = [0, 1, 2, 3] # Morning/Noon/Evening/Night
        self.Temperature = [0, 1, 2, 3, 4] # Level 0-4
        # self.Humidity = [0, 1, 2] # Level 0-2
        self.Brightness = [0, 1, 2, 3] # Level 0-3
        self.Soundlevel = [0, 1, 2, 3, 4] # Level 0-4

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
        ac_to_tem = {0: 0, 1: -0.5, 2: -1.0, 3: -1.5}
        fan_to_tem = {0: 0, 1: -0.4, 2: -0.8, 3: -1.2}
        temperature = int(max(min(time_to_tem[time] + ac_to_tem[ac] + fan_to_tem[fan], 4), 0))
        return temperature

    ''' Function to calculate the brightness according to time of day, lights, and tv '''
    def calculateBrightness(self, time, ceiling, stand, tv):
        time_to_brightness = {0: 3, 1: 2, 2: 1, 3: 0}
        ceiling_to_brightness = {0: 0, 1: 1}
        stand_to_brightness = {0: 0, 1: 1}
        tv_to_brightness = {0: 0, 1: 1}
        brightness = int(max(min(time_to_brightness[time] + ceiling_to_brightness[ceiling] + stand_to_brightness[stand] + tv_to_brightness[tv], 3), 0))
        return brightness

    ''' Function to calculate the sound level according to AC, fan, and speaker '''
    def calculateSoundLevel(self, ac, fan, speaker):
        ac_to_sound = {0: 0, 1: 0.4, 2: 0.8, 3: 1.2}
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
        return self.currState[:]

    ''' Function to update agents' state '''
    def updateAgents(self, actions):
        ceilingAct, standAct, acAct, fanAct, tvAct, speakerAct = actions[0], actions[1], actions[2], actions[3], actions[4], actions[5]
        
        # Ceiling Light
        self.currState[self.agents['ceiling']] = self.executeCeilingLight(self.currState[self.agents['ceiling']], ceilingAct)
        # Stand Light
        self.currState[self.agents['stand']] = self.executeStandLight(self.currState[self.agents['stand']], standAct)
        # AC
        self.currState[self.agents['ac']] = self.executeAC(self.currState[self.agents['ac']], acAct)
        # Fan
        self.currState[self.agents['fan']] = self.executeFan(self.currState[self.agents['fan']], fanAct)
        # TV
        self.currState[self.agents['tv']] = self.executeTV(self.currState[self.agents['tv']], tvAct)
        # Speaker
        self.currState[self.agents['speaker']] = self.executeSpeaker(self.currState[self.agents['speaker']], speakerAct)

        # if ceilingAct != 0:
        #     self.currState[self.agents['ceiling']] = ceilingAct - 1
        
        # if standAct != 0:
        #    self.currState[self.agents['stand']] = standAct - 1
        
        # if acAct != 0:
        #     if acAct == 1:
        #         self.currState[self.agents['ac']] = 0
        #     if acAct == 2:
        #         if self.currState[self.agents['ac']] == 0:
        #             self.currState[self.agents['ac']] = 2
        #     if acAct == 3:
        #         if self.currState[self.agents['ac']] != 0:
        #             self.currState[self.agents['ac']] = min(self.currState[self.agents['ac']] + 1, 3)
        #     if acAct == 4:
        #         if self.currState[self.agents['ac']] != 0:
        #             self.currState[self.agents['ac']] = max(self.currState[self.agents['ac']] - 1, 0)
        
        # if fanAct != 0:
        #     self.currState[self.agents['fan']] = fanAct - 1
        
        # if tvAct != 0:
        #     self.currState[self.agents['tv']] = tvAct - 1
        
        # if speakerAct != 0:
        #     if speakerAct == 1:
        #         self.currState[self.agents['speaker']] = min(self.currState[self.agents['speaker']] + 1, 3)
        #     if speakerAct == 2:
        #         self.currState[self.agents['speaker']] = max(self.currState[self.agents['speaker']] - 1, 0)

    def executeCeilingLight(self, curr_state, action):
        result = curr_state
        if action != 0:
            result = action - 1
        return result

    def executeStandLight(self, curr_state, action):
        result = curr_state
        if action != 0:
            result = action - 1
        return result

    def executeAC(self, curr_state, action):
        result = curr_state
        if action != 0:
            if action == 1:
                result = 0
            if action == 2:
                if curr_state == 0:
                    result = 1
            if action == 3:
                if curr_state != 3:
                    result = min(curr_state + 1, 3)
            if action == 4:
                if curr_state != 0:
                    result = max(curr_state - 1, 0)
        return result

    def executeFan(self, curr_state, action):
        result = curr_state
        if action != 0:
            result = action - 1
        return result

    def executeTV(self, curr_state, action):
        result = curr_state
        if action != 0:
            result = action - 1
        return result

    def executeSpeaker(self, curr_state, action):
        result = curr_state
        if action != 0:
            if action == 1:
                result = min(curr_state + 1, 3)
            if action == 2:
                result = max(curr_state - 1, 0)
        return result


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
        nextState = self.currState[:]

        # print('----Current state induced by agents----')
        # self.showState()
        # print('---------------------------------------')

        ''' Calculate the reward '''
        return nextState

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
