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
            print(i)
            self.sounds.append(sound)

    def play(self, volumeIndex):
        self.sounds[volumeIndex].play()
