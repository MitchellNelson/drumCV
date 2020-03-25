from collections import deque
import simpleaudio as sa
import os

class DrumSound:
    def __init__ (self, pathToAudioFolder, name, numberOfSounds, audioExtention):
        self.pathToAudioFolder = pathToAudioFolder
        self.name = name
        self.numberOfSounds = numberOfSounds
        self.sounds = []
        self.audioExtention = audioExtention
        self.load()
    def load(self):
        for i in range(1, self.numberOfSounds + 1):
            path = "" + self.pathToAudioFolder + "/"+ self.name + str(i) + self.audioExtention
            sound = sa.WaveObject.from_wave_file(path)
            self.sounds.append(sound)

    def play(self, volumeIndex):
        # Play loudest sound if given volume is greater than max 
        if (volumeIndex > self.numberOfSounds - 1):
            self.sounds[self.numberOfSounds -1].play()
        # Play softest sound if less than 0
        elif (volumeIndex < 0):
            self.sounds[0].play()
        else:
            self.sounds[volumeIndex].play()
