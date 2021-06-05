""" Hitbox class which has 2 Position Tuples and can check if a given Point is inside itself
Additionally there are MaxSpeed and Slowdownflags to change the cars reaction with the Hitbox

    author: JONAS GUGEL
    data: 19.03.2021
    licence: free

"""
import pygame as py
from pygame import Vector2

class Hitbox:
    """A Hitbox is a invisible rect, which defines areas. These can be used to change the cars speed.
    
    Tests:
        * Do the slowdown flags work?
        * Does a Hitbox interact with the car fast enough?

    """
    # Variables

    def __init__(self, aPositionTuple1: Vector2, aPositionTuple2: Vector2, aMaxspeed = 100, aSlowdownFlag = True, aCheckpointFlag = False):
        """Init of the Hitbox, sets all the Values

        Args:
            aPositionTuple1 (Vector2): Position1
            aPositionTuple2 (Vector2): Position2
            aMaxspeed (int, optional): aMaxspeed that car can have being in this hitbox. Defaults to 100.
            aSlowdownFlag (bool, optional): changes the hitbox from slowing down to speeding up the car. Defaults to True.
            aCheckpointFlag (bool, optional): Defines the hitbox as a checkpoint. Defaults to False.

        Tests:
            * Are the values set correctly?
            * Does the slowdown work?
            * Does the speedup work?
        """
        self.position1 = Vector2(aPositionTuple1)
        self.position2 = Vector2(aPositionTuple2)
        self.dimensions = Vector2(abs(self.position1.x - self.position2.x),abs(self.position1.y - self.position2.y))
        self.maxSpeed = aMaxspeed
        self.slowdownFlag = aSlowdownFlag
        self.checkpointFlag = aCheckpointFlag

    def checkIfPointIsInside(self, aPosition: Vector2): 
        """Returns a boolean if the given point is inside the Hitbox

        Args:
            aPosition (Vector2): a Point to check

        Returns:
            boolean: is the point inside? True/False

        Tests:
            * Is the position check correct?
            * Is the game fast enough to check?
        """
        return (self.position1.x < aPosition.x < self.position2.x or self.position2.x < aPosition.x < self.position1.x) and (self.position1.y < aPosition.y < self.position2.y or self.position2.y < aPosition.y < self.position1.y)

    def drawDebugHitbox(self, aScreen, carposition):
        """Draws the Hitbox outlines if the developer requests it.

        Args:
            aScreen (pygame.screen): the pygame screen
            carposition (Vector2]): the car position
        
        Tests:
            * Does the rect change color if the player is inside?
            * Is the position correct?
        """
        if self.checkIfPointIsInside(carposition):
            py.draw.rect(aScreen, (255, 0, 0), (self.position1, self.dimensions),5)
        else:
            py.draw.rect(aScreen, (0, 255,0), (self.position1, self.dimensions),5)

        