"""The Game which uses the other python files.

Runs a simple drifting game.

    author: JONAS GUGEL
    data: 19.03.2021
    licence: free

"""
import os
# Hide pygame prompt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import random
from math import sin, cos, tan,atan2, radians, degrees, copysign
from pygame import Vector2
pygame.font.init()

from car import Car
from skidmark import SkidMark
from hitbox import Hitbox
from trackdata import Trackdata
from lapmanager import LapManager




class Game:
    """ The Game Class, of which the object handles all the basic of the game
        
    """

    myfont = pygame.font.SysFont('Arial', 30, True)
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car Drifting Game")
        width = 1600
        height = 900
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        


    def run(self):
        """ Inits all the Runs the game
            Contains the game loop.

            Tests:
                * Does the game Stop if requested?
                * Does the game run at the correct fps?
        """
        trackdata = Trackdata()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(image_path)
        car_image = pygame.transform.scale(car_image, (48,24))
        track01_image = pygame.image.load("tracks/track_02.jpg")
        track01_image = pygame.transform.scale(track01_image,(1600,900))
        car = Car(200, 100, 401, -100, 20, 800, trackdata.track02_hitboxes)
        lapManager = LapManager(trackdata.track02_checkpoints)

        
        while not self.exit:
            lapManager.checkCheckpointPassed(car.position)
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            car.processInputs(pressed, dt)
            # Drawing
            self.screen.fill((100, 100, 100))
            self.screen.blit(track01_image, (0,0))
            lapManager.drawCheckpointMarks(self.screen)
            rotated = pygame.transform.rotate(car_image, degrees(-car.direction))
            car.drawSkidMarks(self.screen)
            rect = rotated.get_rect()



            self.screen.blit(rotated, car.displayPngPosition - (rect.width / 2, rect.height / 2))
            

            #pygame.draw.circle(self.screen, (255,255,0), car.position, 15, 10)
            #pygame.draw.circle(self.screen, (0,255,0), car.frontWheel, 15, 10)
            #pygame.draw.circle(self.screen, (0,0,255), car.turningWheel, 15, 10)
            #pygame.draw.circle(self.screen, (255,255,0), car.displayPos1, 15, 10)
            #pygame.draw.circle(self.screen, (255,0,255), car.displayPos2, 15, 10)
            #pygame.draw.circle(self.screen, (0,255,255), car.displayPos3, 15, 10)
            
            speed = car.speed / 3
            if 130 < speed < 137: speed = 130
            textsurfaceVector = self.myfont.render("CarSpeed: " + str(int(speed)), False, (0, 0, 0))
            self.screen.blit(textsurfaceVector,(190,25))

            textsurfaceVector = self.myfont.render("Last Lap time: " + str(round(lapManager.lastLap, 3)), False, (0, 0, 0))
            self.screen.blit(textsurfaceVector,(440,25))

            textsurfaceVector = self.myfont.render("Fastest Lap: " + str(round(lapManager.fastestLap, 3)), False, (0, 0, 0))
            self.screen.blit(textsurfaceVector,(780,25))

            #for hitbox in trackdata.track01_hitboxes:        
            #    hitbox.drawDebugHitbox(self.screen, car.position)

           # for hitbox in trackdata.track01_checkpoints:        
            #    hitbox.drawDebugHitbox(self.screen, car.position)

            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()

# Start Game
if __name__ == '__main__':
    game = Game()
    game.run()
