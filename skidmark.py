"""

    author: JONAS GUGEL
    data: 19.03.2021
    licence: free

"""
import pygame as py
import random


class SkidMark:
    """A SkidMark is a Circle with lines giving it texture, which represents a Tyre-Skidmark when the car drifts, breaks or Accelerates from stand still
    
    """
    # Variables

    def __init__(self, aPositionTuple, aRotation, anAlpha, aSpeed):
        """Init the Skidmark. Most of the params are not used, maybe in the next development.

        Args:
            aPositionTuple ((x,y))): position of the skidmark
            aRotation (rotation): rotation
            anAlpha (0-255): alpha of the skidmark
            aSpeed (float): Speed of the car
        """
        self.PositionTuple = aPositionTuple
        self.Rotation = aRotation
        self.Alpha = anAlpha
        self.TimeToLive = 255.0
        self.CarSpeed = aSpeed
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


    def update(self, screen, dt):    
        """Update the time to live of the skidmark lower until it invisible. Gets deleted from the skidmark list after too many new ones have been created.

        Args:
            screen (pygame-screen): the screen
            dt (float): time since last call
        """
        # set the rotated rectangle to the old center  
        self.rect.center = self.old_center  
        self.TimeToLive -= .1
        if(self.TimeToLive < 0): self.TimeToLive = 0
        self.new_image.set_alpha(int(self.TimeToLive))
        
        # drawing the rotated skidmark to the screen  
        screen.blit(self.new_image , self.rect)

# #### Temp for RGB-Skidmarks
# for aSkidMark in self.skidMarkList:
#             pygame.draw.rect(aScreen, (red, green, blue, 0), aSkidMark, 5, 1)
#             # if red == 255 and blue == 0:
#             #     green  += 5
#             # if green == 255 and blue == 0:
#             #     red -= 5
#             # if red == 0 and green == 255:
#             #     blue += 5
#             # if blue == 255 and red == 0:
#             #     green -= 5
#             # if green == 0 and blue == 255:
#             #     red  += 5
#             # if red == 255 and green == 0:
#             #     blue -= 5