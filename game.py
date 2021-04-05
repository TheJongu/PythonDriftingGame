import os
import pygame
import random
from math import sin, cos, tan,atan2, radians, degrees, copysign
from pygame import Vector2
pygame.font.init()

class Car:
    """
    A class to represent the driving car on screen with the necessary calculations to simulate the driving physics.
    """

    
    def __init__(self, x, y, aMaxSpeed = 600, aBackSpeed = -100, aMinWheelbase = 50, aMaxWheelbase = 500):
        """
        Inits the car with parameters, which change the cars behaviour.
        
        Parameters
        ----------
            aMaxSpeed: int
                max speed the car can go forward
            aBackSpeed: int
                max speed the car can go reverse
            aMinWheelbase: int
                the minimum distance the simulated wheels can be appart, usually when slow/standing, impacts slow turing
            aMaxWheelbase: int
                the maximum distance the simulated wheels can be appart, usually when highspeed, impacts the drifting handling massively
        """
        # Constants
        self.MAXFRONTSPEED = aMaxSpeed
        self.MAXBACKSPEED = aBackSpeed
        self.MINWHEELBASE = aMinWheelbase
        self.MAXWHEELBASE = aMaxWheelbase

        self.position = Vector2(x, y)

        self.turningWheel = Vector2(0, 0)
        self.frontWheel = Vector2(0, 0)
        self.displayPosFront = Vector2(0, 0)
        self.displayPosBack = Vector2(0, 0)
        self.displayPos1 = Vector2(0, 0)
        self.displayPos2 = Vector2(0, 0)
        self.displayPos3 = Vector2(0, 0)
        self.displayPos4 =  Vector2(0, 0)

        self.direction = 0
        self.wheelBase = 0
        self.speed = 0
        self.steerAngle = 0
        self.direction = 0

        self.skidMarkList = []

    # Process the pressed Buttons on the Keyboard
    def processInputs(self, aPressedKey, aDelta):
        """
        Gets the pressed key and the time since the last call to process the cars behaviour.

        Parameters:
        ----------
            aPressedKey: pygame key
                The key which was pressed by the user
            aDelta: float
                the time since last call. For 60fps should be approx 16 ms
        """

        if aPressedKey[pygame.K_UP]:
            self.accelerate()
        elif aPressedKey[pygame.K_DOWN]:
            self.decelerate()
        else:
            self.friction()

        theDeceleration = 0
        if abs(self.steerAngle) > 1.6: theDeceleration += 5 
        if abs(self.steerAngle) > 2.0: theDeceleration += 5
        if abs(self.steerAngle) > 2.4: theDeceleration += 10
        if abs(self.steerAngle) > 2.8: theDeceleration += 10
        
        if self.speed > 0: self.speed -= theDeceleration
        else: self.speed += theDeceleration

        if abs(self.speed) < 10: self.steerAngle = 0

        if aPressedKey[pygame.K_RIGHT]:
            self.steerRight()
        elif aPressedKey[pygame.K_LEFT]:
            self.steerLeft()
        
        if aPressedKey[pygame.K_j]:
            self.position = (200,200)
        
        

        # Move the car
        self.update(aDelta)

    def accelerate(self):
        """
        accelerates the car with a set speed every updatetick.

        Parameters:
        ----------
            self: car
                the car
        """
        
        self.speed += 3
        if(self.speed > self.MAXFRONTSPEED): self.speed = self.MAXFRONTSPEED
    
    def decelerate(self):
        """
        decelerates the car with a set speed every updatetick.

        Parameters:
        ----------
            self: car
                the car
        """
        self.speed -= 8
        if(self.speed < self.MAXBACKSPEED): self.speed = self.MAXBACKSPEED
    
    def friction(self):
        """
        Applies driving-directional friction the car every updatetick to slow the car down over time.

        Parameters:
        ----------
            self: car
                the car
        """
        theDeceleration = 5
        if self.speed > 0: self.speed -= theDeceleration
        else: self.speed += theDeceleration
        if abs(self.speed < 20): self.speed = 0

    def steerRight(self):
        """
        Steers the car right with a set turningangle every updatetick.
        The more the car is already turning, the longer it takes the car to turn more. This is so, that the car is easier drivable with a keyboard
        TODO: add a function for the steeringAngleDecrease

        Parameters:
        ----------
            self: car
                the car
        """
        theSteerAngle = -0.01
        if abs(self.speed) > 0:
            if self.steerAngle > 0: theSteerAngle = -0.05
            elif self.steerAngle > -1.0: theSteerAngle = -0.040
            elif self.steerAngle > -1.5: theSteerAngle = -0.025 
            elif self.steerAngle > -3.0: theSteerAngle = -0.005
            self.steerAngle += theSteerAngle
            if abs(self.steerAngle) > 3: self.steerAngle = -3
        else:
            self.steerAngle = 0
    def steerLeft(self):
        """
        Steers the car left with a set turningangle every updatetick.
        The more the car is already turning, the longer it takes the car to turn more. This is so, that the car is easier drivable with a keyboard
        TODO: add a function for the steeringAngleDecrease

        Parameters:
        ----------
            self: car
                the car
        """
        theSteerAngle = 0.01
        if abs(self.speed) > 0:
            if self.steerAngle < 0: theSteerAngle = 0.05
            elif self.steerAngle < 1.0: theSteerAngle = 0.040 
            elif self.steerAngle < 1.5: theSteerAngle = 0.025
            elif self.steerAngle < 3.0: theSteerAngle = 0.005 
            self.steerAngle += theSteerAngle
            if(abs(self.steerAngle) > 3): self.steerAngle = 3
        else:
            self.steerAngle = 0

    def calcWheelBase(self):
        """
        Calculates the wheelbase based on the speed. The faster the car is, the further appart the two simulated wheels are, until the MAXWHEELBASE is hit.
        The slower the car is, the shorter the wheelbase is, with a minimum of MINWHEELBASE 

        Parameters:
        ----------
            self: car
                the car
        """

        self.wheelBase = abs(self.speed)/2
        if(self.wheelBase < self.MINWHEELBASE):
            self.wheelBase = self.MINWHEELBASE
        if(self.wheelBase > self.MAXWHEELBASE):
            self.wheelBase = self.MAXWHEELBASE
        
    def drawSkidMarks(self, aScreen):  
        """
        Draws the skidmarks of the car.
        TODO: Skidmarks are to be reworked: 
            As own class and objects - with fadeout and turing in the car direction

        Parameters:
        ----------
            self: car
                the car
            aScreen: screen
                the screen the skidmarks are to be drawn to
        """
        red = 255
        green = 100
        blue = 0        
        for aSkidMark in self.skidMarkList:
            pygame.draw.rect(aScreen, (green, green, green, 0), aSkidMark, 5, 1)
            # if red == 255 and blue == 0:
            #     green  += 5
            # if green == 255 and blue == 0:
            #     red -= 5
            # if red == 0 and green == 255:
            #     blue += 5
            # if blue == 255 and red == 0:
            #     green -= 5
            # if green == 0 and blue == 255:
            #     red  += 5
            # if red == 255 and green == 0:
            #     blue -= 5
            green -= 1
            if green < 0: green = 0

        if(len(self.skidMarkList) > 500):
            del self.skidMarkList[:2]


    def update(self, dt):
        """
        Updates the cars physics and position

        Parameters:
        ----------
            self: car
                the car
            dt: flaot
                the time delta since the last call
        """
        self.calcWheelBase()

        self.displayPosFront = self.position + 70 * Vector2( cos(self.direction) , sin(self.direction))
        self.displayPosBack = self.position + 20 * Vector2( cos(self.direction) , sin(self.direction))
        self.displayPos1 = self.position + 30 * Vector2( cos(self.direction) , sin(self.direction))
        self.displayPos2 = self.position + 40 * Vector2( cos(self.direction) , sin(self.direction))
        self.displayPos3 = self.position + 50 * Vector2( cos(self.direction) , sin(self.direction))
        self.displayPos4 = self.position + 60 * Vector2( cos(self.direction) , sin(self.direction))

        self.turningWheel = self.position - self.wheelBase/2 * Vector2( cos(self.direction) , sin(self.direction))
        self.frontWheel = self.position + self.wheelBase/2 * Vector2( cos(self.direction) , sin(self.direction))  

        self.frontWheel += self.speed * dt * Vector2(cos(self.direction) , sin(self.direction))
        self.turningWheel += self.speed * dt * Vector2(cos(self.direction+self.steerAngle) , sin(self.direction+self.steerAngle))

        self.position = (self.turningWheel + self.frontWheel) / 2
        self.direction = atan2( self.frontWheel.y - self.turningWheel.y , self.frontWheel.x - self.turningWheel.x )

        if abs(self.steerAngle) > 1:

            theOffsetAngle = degrees(self.direction) + 90 
            if degrees(self.direction) > 90:
                theOffsetAngle -= 360

            theOffsetVectorRR = Vector2(cos(radians(theOffsetAngle)), sin(radians(theOffsetAngle))) * 24

            self.skidMarkList.append((self.position.x + theOffsetVectorRR.x - 3, self.position.y + theOffsetVectorRR.y - 5 , 10 , 10 ))
            self.skidMarkList.append((self.position.x - theOffsetVectorRR.x - 3, self.position.y - theOffsetVectorRR.y - 5 , 10 , 10 ))



class Game:
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
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
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(image_path)
        car = Car(200, 400)
        ppu = 32

        while not self.exit:
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
            car.drawSkidMarks(self.screen)
            rotated = pygame.transform.rotate(car_image, degrees(-car.direction))
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.displayPos2 - (rect.width / 2, rect.height / 2))
            pygame.draw.circle(self.screen, (255, 255, 0), (300, 300), 15, 10)
            pygame.draw.circle(self.screen, (255, 255, 0), (900, 300), 15, 10)

            

            #theOffset = 26 * Vector2(cos( tan(24/12) * - car.direction ), sin(tan(24/12) * -car.direction))

            #pygame.draw.rect(self.screen, (200, 0, 0), (car.position.x-5, car.position.y-5, 10, 10), 10, 1)
            #pygame.draw.rect(self.screen, (0, 200, 0), (car.position.x + theOffsetVectorRR.x -5, car.position.y + theOffsetVectorRR.y -5, 10, 10), 10, 1)
            #Green
            #pygame.draw.rect(self.screen, (0, 0, 200), (car.position.x - theOffsetVectorRR.x - 5, car.position.y - theOffsetVectorRR.y - 5, 10, 10), 10, 1)
            
            #pygame.draw.circle(self.screen, (100,255,0), car.frontWheel, 5, 10)
            #pygame.draw.circle(self.screen, (255,100,0), car.turningWheel, 5, 10)

            # textsurface = self.myfont.render("Direction: " + str(degrees(car.direction)) + 
            #                                 "theOffsetAngle: " + str(theOffsetAngle)
            #                                 , False, (0, 0, 0))
            
            # textsurfaceVector = self.myfont.render("theOffsetVectorRR: " + str(theOffsetVectorRR) 
            #                                 , False, (0, 0, 0))
            #self.screen.blit(textsurface,(0,0))
            #self.screen.blit(textsurfaceVector,(0,30))

            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
