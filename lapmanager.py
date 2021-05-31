"""

    author: JONAS GUGEL
    data: 19.03.2021
    licence: free

"""
import pygame as py
import time
from pygame import Vector2
from hitbox import Hitbox
from loguru import logger

class LapManager:
    """A Hitbox is a invisible rect, which defines areas. These can be used to change the cars speed.
    
    """
    # Variables

    def __init__(self, aCheckpointList):
        self.startTime = 0
        self.raceTimeStart = 0
        self.checkpointList = aCheckpointList
        self.checkpointsPassed = len(self.checkpointList)
        self.currentCheckpoint = self.checkpointList[len(self.checkpointList)-1]
        self.lastLap = 0
        self.fastestLap = 0
        self.laps = 1

    def checkCheckpointPassed(self, carposition: Vector2):
        if self.currentCheckpoint.checkIfPointIsInside(carposition):
            logger.debug("Car passed checkpoint - \tCar Position:" + str(carposition) + " \tCheckpoint Pos1:" + str(self.currentCheckpoint.position1)+ " \tCheckpoint Pos2:" + str(self.currentCheckpoint.position2))
            if self.raceTimeStart == 0: self.raceTimeStart = time.time()
            self.checkpointsPassed += 1
            if(self.checkpointsPassed > len(self.checkpointList) - 1):
                # only first time
                if(self.startTime != 0):
                    self.lastLap = time.time() - self.startTime
                    if self.lastLap < self.fastestLap or self.fastestLap == 0: self.fastestLap = self.lastLap
                    self.laps = self.laps + 1
                self.startTime = time.time()
                self.checkpointsPassed = 0

            self.currentCheckpoint = self.checkpointList[self.checkpointsPassed]
                # lap finished
    def drawCheckpointMarks(self, aScreen):
        
        for checkpoint in self.checkpointList:            
            self.drawOneCheckpointMark(checkpoint, aScreen, (150,150,150))
        self.drawOneCheckpointMark(self.currentCheckpoint, aScreen, (0,255,0))
            
    def drawOneCheckpointMark(self, checkpoint, aScreen, aColor):
        tmpVec = Vector2(0,0)
        if checkpoint.dimensions.x < checkpoint.dimensions.y: tmpVec = (0,checkpoint.dimensions.y)
        else: tmpVec = (checkpoint.dimensions.x, 0)
        py.draw.circle(aScreen, aColor, checkpoint.position1, 15, 10)
        py.draw.circle(aScreen, aColor, checkpoint.position1+tmpVec, 15, 10)
            
        py.draw.circle(aScreen, (0,0,0), checkpoint.position1, 5, 2)
        py.draw.circle(aScreen, (0,0,0), checkpoint.position1, 15, 2)
        py.draw.circle(aScreen, (0,0,0), checkpoint.position1+tmpVec, 5, 2)
        py.draw.circle(aScreen, (0,0,0), checkpoint.position1+tmpVec, 15, 2)


    
    



        