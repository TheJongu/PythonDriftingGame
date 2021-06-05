"""Skidmarks for the car when its accelerating from a standstill or drifting.

    author: JONAS GUGEL
    data: 19.03.2021
    licence: free

"""
import pygame as py
import random


class SkidMark:
    """A SkidMark is a Circle with lines giving it texture, which represents a Tyre-Skidmark when the car drifts, breaks or Accelerates from stand still
    
    Tests:
        * Is the Skidmark drawn on the correct position?
        * Does the color of the Skidmark work?
    """
    # Variables

    def __init__(self, aPositionTuple, aRotation, anAlpha, aSpeed):
        """Init the Skidmark. Most of the params are not used, maybe in the next development.

        Args:
            aPositionTuple ((x,y))): position of the skidmark
            aRotation (rotation): rotation
            anAlpha (0-255): alpha of the skidmark
            aSpeed (float): Speed of the car

        Tests:
            * Are the values set correctly?
            * Does the RGB overwrite the set color?
        """
        self.PositionTuple = aPositionTuple
        self.Rotation = aRotation
        self.Alpha = anAlpha
        self.TimeToLive = 255.0
        self.CarSpeed = aSpeed
        self.red = 255
        self.blue = 0
        self.green = 0
        #Define colors
        self.BLACK = (0 , 0 , 0)
        # Color 77,77,77 is Max lightiness, go down to more black from here
        self.color = abs(77 - abs(anAlpha * anAlpha *  20))        
        self.GREEN = (self.color,self.color,self.color)
        self.TEXTURE = (60 , 60 , 60)
        random.randint(45,65)
        # Give the skidmark a time to live
        self.TimeToLive = 255
        self.image_orig = py.Surface((8 , 8))  
        self.image_orig.set_colorkey(self.BLACK)  
        # Draw the skidmark onto the surface
        py.draw.circle(self.image_orig, self.GREEN, (4,4), 4, 10)
        self.image = self.image_orig.copy()
        self.image.set_colorkey(self.BLACK)  
        self.rect = self.image.get_rect()  
        self.rect.center = self.PositionTuple  
    
        # making a copy of the old center of the rectangle  
        self.old_center = self.rect.center  
        # defining angle of the rotation  
        self.rot = self.Rotation  
        # rotating the orignal image  
        self.new_image = py.transform.rotate(self.image_orig , self.rot)  
        self.image_orig.set_alpha(10)
        self.rect = self.new_image.get_rect()


    def update(self, screen, dt, rgbFlag = False):    
        """Update the time to live of the skidmark lower until it invisible. Gets deleted from the skidmark list after too many new ones have been created.

        Args:
            screen (pygame-screen): the screen
            dt (float): time since last call

        Tests: 
            * Does the skidmark get a lower alpha over time?
            * Does the skidmark fade out and a appropriate speed?
        """
        # set the rotated rectangle to the old center  
        if rgbFlag:
            self.rgbSkidmarks()
        self.rect.center = self.old_center  
        self.TimeToLive -= .1
        if(self.TimeToLive < 0): self.TimeToLive = 0
        self.new_image.set_alpha(int(self.TimeToLive))
        
        # drawing the rotated skidmark to the screen  
        screen.blit(self.new_image , self.rect)

    def rgbSkidmarks(self):
        """adjusts the color of the Image to be changing RGB.

        Tests:
            * Does it cycle?
            * Do the colors looooook preeety? - yes, yes they do.
        """
        py.draw.circle(self.new_image, (self.red,self.blue,self.green), (4,4), 4, 10)
        if self.red == 255 and self.blue == 0:
            self.green  += 5
        if self.green == 255 and self.blue == 0:
            self.red -= 5
        if self.red == 0 and self.green == 255:
            self.blue += 5
        if self.blue == 255 and self.red == 0:
            self.green -= 5
        if self.green == 0 and self.blue == 255:
            self.red  += 5
        if self.red == 255 and self.green == 0:
            self.blue -= 5