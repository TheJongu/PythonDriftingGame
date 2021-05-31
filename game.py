"""The Game which uses the other python files.

Runs a simple drifting game.

    author: JONAS GUGEL
    data: 19.03.2021
    licence: free

"""
import os
import pygame
import random
import pygame_menu
import time
from math import sin, cos, tan,atan2, radians, degrees, copysign
from pygame import Vector2
pygame.font.init()

from car import Car
from skidmark import SkidMark
from hitbox import Hitbox
from trackdata import Trackdata
from lapmanager import LapManager
from loguru import logger

class Game:
    """ The Game Class, of which the object handles all the basic of the game
        
    """

    myfont = pygame.font.SysFont('Arial', 30, True)
    def __init__(self, aScreen, aCarType, aTrack):
        #pygame.init()
        pygame.display.set_caption("Car Drifting Game")
        self.screen = aScreen
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.track = self.loadTrack(aTrack)
        self.car = self.createCar(aCarType, aTrack)
        

    def run(self):
        """ Inits all the Runs the game
            Contains the game loop.

            Tests:
                * Does the game Stop if requested?
                * Does the game run at the correct fps?
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, self.car.carImage)
        car_image = pygame.image.load(image_path).convert_alpha()
        car_image = pygame.transform.scale(car_image, (48,24))        
        pygame.Surface((48,24), )

        
        while not self.exit:
            self.lapManager.checkCheckpointPassed(self.car.position)
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            if self.lapManager.laps != 5:
                # User input
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_ESCAPE]:
                    self.exit = True
                    logger.debug("Exiting running Game, going to menu") 

                self.car.processInputs(pressed, dt)
            else: 
                self.finishGame()
            # Drawing
            self.screen.fill((255,255,255))
            self.screen.blit(self.trackImage, (0,0))
            self.lapManager.drawCheckpointMarks(self.screen)
            rotated = pygame.transform.rotate(car_image, degrees(-self.car.direction))
            self.car.drawSkidMarks(self.screen)
            rect = rotated.get_rect()

            self.screen.blit(rotated, self.car.displayPngPosition - (rect.width / 2, rect.height / 2))

            # For debugging car position
            #pygame.draw.circle(self.screen, (255,255,0), self.car.position, 15, 10)
            #pygame.draw.circle(self.screen, (0,255,0), self.car.frontWheel, 15, 10)
            #pygame.draw.circle(self.screen, (0,0,255), self.car.turningWheel, 15, 10)
            #pygame.draw.circle(self.screen, (255,255,0), car.displayPos1, 15, 10)
            #pygame.draw.circle(self.screen, (255,0,255), car.displayPos2, 15, 10)
            #pygame.draw.circle(self.screen, (0,255,255), car.displayPos3, 15, 10)
            
            speed = self.car.speed 
            #if 130 < speed < 137: speed = 130
            textsurfaceVector = self.myfont.render("CarSpeed: " + str(int(speed)), False, (0, 0, 0))
            self.screen.blit(textsurfaceVector,(190,25))

            textsurfaceVector = self.myfont.render("Last Lap time: " + str(round(self.lapManager.lastLap, 3)), False, (0, 0, 0))
            #textsurfaceVector = self.myfont.render("Last Lap time: " + str(self.car.steerAngle), False, (0, 0, 0))
            self.screen.blit(textsurfaceVector,(440,25))

            textsurfaceVector = self.myfont.render("Fastest Lap: " + str(round(self.lapManager.fastestLap, 3)), False, (0, 0, 0))
            self.screen.blit(textsurfaceVector,(780,25))

            textsurfaceVector = self.myfont.render("Lap: " + str(self.lapManager.laps) + "/5", False, (0, 0, 0))
            self.screen.blit(textsurfaceVector,(1100,25))

            #debug for drawing hitboxes of the tracks
            #for hitbox in trackdata.track01_hitboxes:        
            #    hitbox.drawDebugHitbox(self.screen, car.position)
            
            #debug for drawing hitboxes of the tracks
            #for hitbox in trackdata.track02_checkpoints:        
            #    hitbox.drawDebugHitbox(self.screen, car.position)


            pygame.display.flip()

            self.clock.tick(self.ticks)
        

    def loadTrack(self, aTrack):
        """ Loads the track data into the object variables game

        Args:
            aTrack (int): 1 (easy) or 2 (expert)

        Tests:
            * Is the correct track loaded?
            * Do the checkpoints work?
            * Do the hitboxes word?
        """
        self.trackdata = Trackdata()
        if aTrack == 1:
            self.trackImage = pygame.image.load("tracks/track_01.jpg")
            self.trackImage = pygame.transform.scale(self.trackImage,(1600,900))
            self.lapManager = LapManager(self.trackdata.track01_checkpoints)
        else:

            self.trackImage = pygame.image.load("tracks/track_02.jpg")
            self.trackImage = pygame.transform.scale(self.trackImage,(1600,900))
            self.lapManager = LapManager(self.trackdata.track02_checkpoints)

    def createCar(self, aCarType, aTrack):
        """ Creates a new car with the self.carType and self.track

        Args:
            aCarType (int): 1 (driftcar) or 2 (race car)

        Tests:
            * Is the car set correctly?
            * Do driftcar and race car behave differently?
        """
        if aTrack == 1:
            return Car(200, 100, 401, -100, 20, 800, self.trackdata.track01_hitboxes, aCarType)
        else:
            return Car(200, 100, 401, -100, 20, 800, self.trackdata.track02_hitboxes, aCarType)
    
    def finishGame(self):
        """After racing 5 laps, stop the game and show the finish screen.

        Tests:
            * Is the time correct?
            * Is the text readable?
        """
        mytheme = pygame_menu.themes.THEME_ORANGE

        # Set Background Image
        myimage = pygame_menu.baseimage.BaseImage(
            image_path="tracks/trophy.jpg"
        )
        mytheme.background_color = myimage
        resultScreen = pygame_menu.Menu('Results', 1600, 900, theme=mytheme)


        resultScreen.add.label("Schnellste Runde:\t" + str(round(self.lapManager.fastestLap, 3)))
        resultScreen.add.label("Gesamt Renndauer:\t"+ str(round(time.time() - self.lapManager.raceTimeStart, 3)))
        resultScreen.add.label("")
        
        resultScreen.add.button('Back to Menu', self.stopResultMenu)
        
        self.resultScreenExit = False
        while not self.resultScreenExit:     
            resultScreen.mainloop(self.screen)

    def stopResultMenu(self):
        """Stop the result menu and stop the game

        Tests:
            * Is the result menu closed correctly?
            * Is the game reset to the menu?
        """
        self.resultScreenExit = True
        self.exit = True

# Start Game
if __name__ == '__main__':
    game = Game()
    game.run()
