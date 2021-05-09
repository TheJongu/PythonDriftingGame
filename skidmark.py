import pygame as py
import random

"""

"""


class SkidMark:
    """A SkidMark is a Circle with lines giving it texture, which represents a Tyre-Skidmark when the car drifts, breaks or Accelerates from stand still
    
    """
    # Variables

    def __init__(self, aPositionTuple, aRotation, anAlpha, aSpeed):
        self.PositionTuple = aPositionTuple
        self.Rotation = aRotation
        self.Alpha = anAlpha
        self.TimeToLive = 255.0
        self.CarSpeed = aSpeed
        self.BLACK = (0 , 0 , 0)

         
        self.color = abs(127 - abs(anAlpha * anAlpha *  30))
        
        self.GREEN = (self.color,self.color,self.color)
        self.TEXTURE = (60 , 60 , 60)
        random.randint(45,65)
        # define a surface (RECTANGLE)  
        self.TimeToLive = abs(255)
        self.image_orig = py.Surface((8 , 8))  
        #self.image_orig.fill((180,20,20))
        # for making transparent background while rotating an image  
        #self.image_orig.fill( self.GREEN)
        self.image_orig.set_colorkey(self.BLACK)  
        py.draw.circle(self.image_orig, self.GREEN, (4,4), 4, 10)
        #theColor = random.randint(45,65)
        #py.draw.line(self.image_orig,(theColor,theColor,theColor),(random.randint(4,12),random.randint(4,12)),(random.randint(4,12),random.randint(4,12)))
        #theColor = random.randint(45,65)
        #py.draw.line(self.image_orig,(theColor,theColor,theColor),(random.randint(4,12),random.randint(4,12)),(random.randint(4,12),random.randint(4,12)))
        #theColor = random.randint(45,65)
        #py.draw.line(self.image_orig,(theColor,theColor,theColor),(random.randint(4,12),random.randint(4,12)),(random.randint(4,12),random.randint(4,12)))
        #theColor = random.randint(45,65)

        # fill the rectangle / surface with green color  
        #self.image_orig.fill(self.GREEN)  
        # creating a copy of orignal image for smooth rotation  
        self.image = self.image_orig.copy()
        self.image.set_colorkey(self.BLACK)  
        # define rect for placing the rectangle at the desired position  
        self.rect = self.image.get_rect()  
        self.rect.center = self.PositionTuple  
        # keep rotating the rectangle until running is set to False  
    
        # clear the screen every time before drawing new objects  
        

        # making a copy of the old center of the rectangle  
        self.old_center = self.rect.center  
        # defining angle of the rotation  
        self.rot = self.Rotation  
        # rotating the orignal image  
        self.new_image = py.transform.rotate(self.image_orig , self.rot)  
        self.image_orig.set_alpha(10)
        self.rect = self.new_image.get_rect()



    def update(self, screen, dt):    

        # set the rotated rectangle to the old center  
        self.rect.center = self.old_center  
        self.TimeToLive -= .2
        if(self.TimeToLive < 0): self.TimeToLive = 0
        self.new_image.set_alpha(int(self.TimeToLive))
        
        # drawing the rotated rectangle to the screen  
        #py.draw.circle(screen, self.GREEN, self.PositionTuple, 8, 10)
        screen.blit(self.new_image , self.rect)




# #### Temp
# for aSkidMark in self.skidMarkList:
#             pygame.draw.rect(aScreen, (green, green, green, 0), aSkidMark, 5, 1)
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