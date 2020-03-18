from collections import deque
import os
import numpy as np

class Stick:
    def __init__(self, name):
        self.points = deque(maxlen = 4)
        self.minPoint = 500
        self.isGoingDown = False
        self.min = 500
        self.name = name

    def getName(self):
        return self.name
   
    def setMin(self, min):
        self.min = min

    def getMin(self):
        return self.min

    def getIsGoingDown(self):
        return self.isGoingDown

    def updateIsGoingDown(self, isGoingDown):
        self.isGoingDown = isGoingDown
    
    def getPoints(self):
        return self.points

    def addPoint(self, x, y):
        self.points.appendleft((x, y))
        
    def getX(self):
        return self.points[0][0]

    def getY(self):
        return self.points[0][1]
