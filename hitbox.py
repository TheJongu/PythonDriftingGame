"""

    author: JONAS GUGEL
    data: 19.03.2021
    licence: free

"""
import pygame as py
from pygame import Vector2

class Hitbox:
    """A Hitbox is a invisible rect, which defines areas. These can be used to change the cars speed.
    
    """
    # Variables

    def __init__(self, aPositionTuple1: Vector2, aPositionTuple2: Vector2):
        self.Position1 = Vector2(aPositionTuple1)
        self.Position2 = Vector2(aPositionTuple2)
        self.Dimensions = Vector2(abs(self.Position1.x - self.Position2.x),abs(self.Position1.y - self.Position2.y))

    def checkIfPointIsInside(self, aPosition: Vector2): 
        """Returns a boolean if the given point is inside the Hitbox

        Args:
            aPosition (Vector2): a Point to check

        Returns:
            boolean: is the point inside? True/False

        Tests:
            * Is the position check correct?
        """
        if(self.Position1.x < aPosition.x < self.Position2.x or self.Position2.x < aPosition.x < self.Position1.x):
            if(self.Position1.y < aPosition.y < self.Position2.y or self.Position2.y < aPosition.y < self.Position1.y): return True
        return False

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
            py.draw.rect(aScreen, (255, 0, 0), (self.Position1, self.Dimensions),1)
        else:
            py.draw.rect(aScreen, (0, 255,0), (self.Position1, self.Dimensions),1)

        