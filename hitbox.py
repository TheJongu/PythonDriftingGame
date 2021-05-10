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

    def __init__(self, aPositionTuple1, aPositionTuple2):
        self.Position1 = aPositionTuple1
        self.Position2 = aPositionTuple2

    def checkIfPointIsInside(Vector2: aPosition): 
        if( self.Position1.x < aPosition.x < self.Position2.x):
            