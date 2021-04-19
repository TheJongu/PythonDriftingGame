"""

"""

import pygame
import random
from math import sin, cos, tan,atan2, radians, degrees, copysign
from pygame import Vector2
from skidmark import SkidMark

class Car:
    """A class to represent the driving car on screen with the necessary calculations to simulate the driving physics.
    """


    def __init__(self, x, y, aMaxSpeed = 600, aBackSpeed = -100, aMinWheelbase = 50, aMaxWheelbase = 500):
        """Inits the car with parameters, which change the cars behaviour.

        Args:
            x (int): x Startposition of the car
            y (int): y Startposition of the car
            aMaxSpeed (int, optional): max speed the car can go forward. Defaults to 600.
            aBackSpeed (int, optional): max speed the car can go reverse. Defaults to -100.
            aMinWheelbase (int, optional): the minimum distance the simulated wheels can be appart, usually when slow/standing, impacts slow turing. Defaults to 50.
            aMaxWheelbase (int, optional): the maximum distance the simulated wheels can be appart, usually when highspeed, impacts the drifting handling massively. Defaults to 500.

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

    def processInputs(self, aPressedKey, aDelta):
        """Gets the pressed key and the time since the last call to process the cars behaviour.

        Args:
            aPressedKey (pygame key): The key which was pressed by the user
            aDelta (float): the time since last call. For 60fps should be approx 16 ms

        Tests:
            * Key not relavent to the car: Nothing happens
            * Two keys pressed: Both get processed
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
        """Accelerates the car with a set speed every updatetick.

        Tests:
            * Car can not be faster then the MAXFRONTSPEED 
            * Car does not "Jump" to positive speed when acc while driving backwards
        """
        
        self.speed += 3
        if(self.speed > self.MAXFRONTSPEED): self.speed = self.MAXFRONTSPEED
    
    def decelerate(self):
        """Decelerates the car with a set speed every updatetick.

        Tests:
            * Car can not be faster then the MAXBACKSPEED
            * Car does not "Jump" to negative speed when breaking
        """

        self.speed -= 8
        if(self.speed < self.MAXBACKSPEED): self.speed = self.MAXBACKSPEED
    
    def friction(self):
        """Applies driving-directional friction the car every updatetick to slow the car down over time.

        Tests:
            * Car can not be faster then the MAXBACKSPEED
            * Car is getting slowed down over time when not accelerating/decelerating
        """

        theDeceleration = 5
        if self.speed > 0: self.speed -= theDeceleration
        else: self.speed += theDeceleration
        if abs(self.speed < 20): self.speed = 0

    def steerRight(self):
        """Steers the car right with a set turningangle every updatetick.

        The more the car is already turning, the longer it takes the car to turn more. This is so, that the car is easier drivable with a keyboard
        TODO: add a function for the steeringAngleDecrease

        Tests:
            * Car turns in to the right when button is pressed
            * Car turns slower the more its turned
            * Countersteering works as expected from the User
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
        """Steers the car left with a set turningangle every updatetick.
        The more the car is already turning, the longer it takes the car to turn more. This is so, that the car is easier drivable with a keyboard
        TODO: add a function for the steeringAngleDecrease

        Tests:
            * Car turns in to the left when button is pressed
            * Car turns slower the more its turned
            * Countersteering works as expected from the User
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
        """ Calculates the wheelbase based on the speed. The faster the car is, the further appart the two simulated wheels are, until the MAXWHEELBASE is hit.
        The slower the car is, the shorter the wheelbase is, with a minimum of MINWHEELBASE 

        Tests:
            * The Wheelbase of the car can not be smaller/bigger then the defined MINWHEELBASE/MAXWHEELBASE of the car
            * The calculation is correct
        """

        self.wheelBase = abs(self.speed)/2
        if(self.wheelBase < self.MINWHEELBASE):
            self.wheelBase = self.MINWHEELBASE
        if(self.wheelBase > self.MAXWHEELBASE):
            self.wheelBase = self.MAXWHEELBASE
        
    def drawSkidMarks(self, aScreen):  
        """ Draws the skidmarks of the car.
        TODO: Skidmarks are to be reworked: 
            As own class and objects - with fadeout and turing in the car direction

        Args:
            aScreen (pygame.surface): the screen the skidmarks are to be drawn to

        Tests:
            * Skidmars are being drawn.
            * If too many SkidMarks exist, the last 2 are deleted
            * The Game can handle the amount of SkidMarks
        """     
        for aSkidMark in self.skidMarkList:
            aSkidMark.update(aScreen,0)

        if(len(self.skidMarkList) > 1000):
            del self.skidMarkList[:2]

    def calcWheelPositions(self, dt):
        """Calucates the wheelPosition of the Car. 

        The Code is based on the idea from:
        Source: http://engineeringdotnet.blogspot.com/2010/04/simple-2d-car-physics-in-games.html
        This code has been taken and implemented. However his code works for "traditional driving physics". Meaning: Actual driving with frontwheel steering.
        This was not the scope of this project. So I majorly adjusted the codea and his basic idea, which allows me to simulate a drift.

        Args:
            dt : The timedelta since the last call
        
        Tests:
            * Are the wheels correctly positioned?
            * Does the car not exceed the max speed?
        """
        self.turningWheel = self.position - self.wheelBase/2 * Vector2( cos(self.direction) , sin(self.direction))
        self.frontWheel = self.position + self.wheelBase/2 * Vector2( cos(self.direction) , sin(self.direction))  

        self.frontWheel += self.speed * dt * Vector2(cos(self.direction) , sin(self.direction))
        self.turningWheel += self.speed * dt * Vector2(cos(self.direction+self.steerAngle) , sin(self.direction+self.steerAngle))

        self.position = (self.turningWheel + self.frontWheel) / 2
        self.direction = atan2( self.frontWheel.y - self.turningWheel.y , self.frontWheel.x - self.turningWheel.x )



    def update(self, dt):
        """ Updates the cars physics and position

        Args:
            self (car): the car
             dt (float): the time delta since the last call
        """

        self.calcWheelBase()

        self.displayPosFront = self.position + 70 * Vector2( cos(self.direction) , sin(self.direction))
        self.displayPosBack = self.position + 20 * Vector2( cos(self.direction) , sin(self.direction))
        self.displayPos1 = self.position + 30 * Vector2( cos(self.direction) , sin(self.direction))
        self.displayPos2 = self.position + 40 * Vector2( cos(self.direction) , sin(self.direction))
        self.displayPos3 = self.position + 50 * Vector2( cos(self.direction) , sin(self.direction))
        self.displayPos4 = self.position + 60 * Vector2( cos(self.direction) , sin(self.direction))

        self.calcWheelPositions(dt)

        if abs(self.steerAngle) > 1:

            theOffsetAngle = degrees(self.direction) + 90 
            if degrees(self.direction) > 90:
                theOffsetAngle -= 360

            theOffsetVectorRR = Vector2(cos(radians(theOffsetAngle)), sin(radians(theOffsetAngle))) * 18

            self.skidMarkList.append(SkidMark((self.position.x + theOffsetVectorRR.x, self.position.y + theOffsetVectorRR.y),degrees(-self.direction), 250, self.speed))
            self.skidMarkList.append(SkidMark((self.position.x - theOffsetVectorRR.x, self.position.y - theOffsetVectorRR.y),degrees(-self.direction), 150, self.speed))
           
