from pyo import *
from math import *
import time

class Source():

    def __init__(self, mixer, trajectoire, timestamp, position, speed=1):
        self.state = False
        self.volume = 0.075
        self.player = False
        self.trajectoire = trajectoire
        self.timestamp = timestamp
        self.position = position
        self.a = 6 / (20*log10(2))
        self.speed = speed

    def getTrajectoire(self) :
        return self.trajectoire

    def getTimestamp(self) :
        return self.timestamp

    def setTimestamp(self, timestamp) :
        self.timestamp = timestamp

    def getPosition(self) :
        return self.position

    def setPosition(self, position) :
        self.position = position

    def setState(self, state):
        self.state = state
        if not isinstance(self.player, bool):
            if self.state == True:
                self.player.play()
            else:
                self.player.stop()

    def getState(self):
        return self.state

    def setVolume(self, volume):
        self.volume = volume

    def getVolume(self):
        return self.volume

    def setPlayer(self, son):
        if son == False :
            self.player = False
        else :
            self.player = SfPlayer(son, speed=self.speed, loop=1)

    def getPlayer(self):
        return self.player

    def setPath(self, path):
        self.player.setPath(path)