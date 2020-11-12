import random

class Env:
    def __init__(self):
        self.agents = [0, 1, 2, 3, 4, 5] # 0: Ceilling, 1: Stand, 2: AC. 3: Fan, 4: TV, 5: Speaker
        ''' All state data '''
        ''' Environment state '''
        self.TimeOfDay = [0, 1, 2, 3] # Morning/Noon/Evening/Night
        self.Temperature = [0, 1, 2] # Level 0-2
        # self.Humidity = [0, 1, 2] # Level 0-2
        self.Brightness = [0, 1, 2, 3] # Level 0-4
        self.Soundlevel = [0, 1, 2, 3, 4] # Level 0-5

        ''' Agent state '''
        self.CeilingLight = [0, 1] # OFF/ON
        self.StandLight = [0, 1] # OFF/ON
        self.AC = [0, 1, 2, 3] # OFF/LOW/MEDIUM/HIGH
        self.Fan = [0, 1, 2, 3] # OFF/LOW/MEDIUM/HIGH
        self.TV = [0, 1] # ON/OFF
        self.Speaker = [0, 1, 2, 3] # OFF/LOW/MEDIUM/HIGH

        ''' Agent actions '''
        self.CeilingLightActions = [0, 1, 2] # Still/OFF/ON
        self.StandLightActions = [0, 1, 2] # Still/OFF/ON
        self.ACActions = [0, 1, 2, 3, 4] # Still/OFF/ON/UP/DOWN
        self.FanActions = [0, 1, 2] # Still/UP/DOWN
        self.TVActions = [0, 1, 2] # Still/OFF/ON
        self.SpeakerActions = [0, 1, 2] # Still/UP/DOWN

        ''' Current states '''
        self.currState = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
        # 0: Time, 1: Temperature, 2: Brightness, 3: Sound level, 4: Ceiling, 5: Stand, 6: AC, 7: Fan, 8: TV, 9: Speak

    ''' Function to calculate the temperature according to AC and Fan '''
    def calculateTemperature(self, ac, fan):
        pass

    ''' Function to calculate the brightness according to time of day, lights, and tv '''
    def calculateBrightness(self, time, ceiling, stand, tv):
        pass
    ''' Function to calculate the sound level according to AC, fan, and speaker '''
    def calculateSoundLevel(self, ac, fan, speaker):
        pass

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
        temperature = self.calculateTemperature(ac, fan)
        brightness = self.calculateBrightness(time, ceiling, stand, tv)
        sound = self.calculateSoundLevel(ac, fan, speaker)

        self.currState = [time, temperature, brightness, sound, ceiling, stand, ac, fan, tv, speaker]


    ''' Function to move the next time step '''
    def step(self, actions):
        pass

    ''' print the current environment states '''
    def showState(self):
        pass

    def getUserActions(self):
        pass