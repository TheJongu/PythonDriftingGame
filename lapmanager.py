"""

    author: JONAS GUGEL
    data: 19.03.2021
    licence: free

"""
import pygame as py
import time
from pygame import Vector2
from hitbox import Hitbox

class LapManager:
    """A Hitbox is a invisible rect, which defines areas. These can be used to change the cars speed.
    
    """
    # Variables

    def __init__(self, aCheckpointList):
        self.startTime = 0
        self.checkpointList = aCheckpointList
        self.checkpointsPassed = len(self.checkpointList)
        self.currentCheckpoint = self.checkpointList[len(self.checkpointList)-1]
        self.lastLap = 0
        self.fastestLap = 0
        self.laps = 0

    def checkCheckpointPassed(self, carposition: Vector2):
        if self.currentCheckpoint.checkIfPointIsInside(carposition):
            self.checkpointsPassed += 1
            if(self.checkpointsPassed > len(self.checkpointList) - 1):
                # only first time
                if(self.startTime != 0):
                    self.lastLap = time.time() - self.startTime
                    if self.lastLap < self.fastestLap or self.fastestLap == 0: self.fastestLap = self.lastLap
                self.startTime = time.time()
                self.checkpointsPassed = 0

            self.currentCheckpoint = self.checkpointList[self.checkpointsPassed]
                # lap finished
    def drawCheckpointMarks(self, aScreen):
        for checkpoint in self.checkpointList:
            if checkpoint == self.currentCheckpoint:
                py.draw.circle(aScreen, (0,255,0), checkpoint.position1, 15, 10)
                
            else: 
                py.draw.circle(aScreen, (255,255,0), checkpoint.position1, 15, 10)
            py.draw.circle(aScreen, (0,0,0), checkpoint.position1, 5, 2)
            py.draw.circle(aScreen, (0,0,0), checkpoint.position1, 15, 2)
            

    
    



        