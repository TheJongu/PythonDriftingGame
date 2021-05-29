"""
    author: JONAS GUGEL
    data: 19.03.2021
    licence: free

"""

import pygame
import random
from math import sin, cos, tan,atan2, radians, degrees, copysign
from pygame import Vector2
from skidmark import SkidMark
from hitbox import Hitbox

class Car:
    """A class to represent the driving car on screen with the necessary calculations to simulate the driving physics.
    """


    def __init__(self, x, y, aMaxSpeed = 600, aBackSpeed = -100, aMinWheelbase = 50, aMaxWheelbase = 500, aHitboxList=[], aCarType = 1):
        """Inits the car with parameters, which change the cars behaviour.

        Args:
            x (int): x Startposition of the car
            y (int): y Startposition of the car
            aMaxSpeed (int, optional): max speed the car can go forward. Defaults to 600.
            aBackSpeed (int, optional): max speed the car can go reverse. Defaults to -100.
            aMinWheelbase (int, optional): the minimum distance the simulated wheels can be appart, usually when slow/standing, impacts slow turing. Defaults to 50.
            aMaxWheelbase (int, optional): the maximum distance the simulated wheels can be appart, usually when highspeed, impacts the drifting handling massively. Defaults to 500.

        SOURCES:   
            Car pictures have been taken from:
                Drift-Car: https://www.shutterstock.com/de/image-illustration/scarlet-red-modern-sports-car-top-606631487
                Race-Car (F1): VectorStock.com/17359688
            They have been edited by me.
        """
        
        # Constants
        self.MAXFRONTSPEED = aMaxSpeed
        self.MAXBACKSPEED = aBackSpeed
        self.MINWHEELBASE = aMinWheelbase
        self.MAXWHEELBASE = aMaxWheelbase
        self.MAXSKIDMARKS = 5000
        self.position = Vector2(x, y)

        self.turningWheel = Vector2(0, 0)
        self.frontWheel = Vector2(0, 0)
        self.displayPosFront = Vector2(0, 0)
        self.displayPosBack = Vector2(0, 0)
        self.displayPos1 = Vector2(0, 0)
        self.displayPos2 = Vector2(0, 0)
        self.displayPos3 = Vector2(0, 0)
        self.displayPos4 =  Vector2(0, 0)
        self.displayPngPosition = Vector2(0,0)
        self.skidmarkOffsetVector = Vector2(0,0)
        self.pngOffset = -5
        self.hitboxList = aHitboxList

        self.direction = 0
        self.wheelBase = 0
        self.speed = 0
        self.steerAngle = 0
        self.direction = 0

        self.skidMarkList = []
        if aCarType == 1:
            self.carImage = "car_try.png"
        if aCarType == 2:
            self.carImage = "race_car.png"
            

    def processInputs(self, aPressedKey, aDelta):
        """Gets the pressed key and the time since the last call to process the cars behaviour.

        Args:
            aPressedKey (pygame key): The key which was pressed by the user
            aDelta (float): the time since last call. For 60fps should be approx 16 ms

        Tests:
            * Key not relavent to the car: Nothing happens
            * Two keys pressed: Both get processed
        """
        # (Re-)Set MaxFrontSpeed into currentFrontSpeed for this run of the process input
        # If the car goes over Hitboxes, this currentFrontSpeed will be set lower or higher 
        self.currentFrontSpeed = self.MAXFRONTSPEED

        if aPressedKey[pygame.K_UP] or aPressedKey[pygame.K_w] or aPressedKey[pygame.K_c]:
            self.accelerate()
        elif aPressedKey[pygame.K_DOWN] or aPressedKey[pygame.K_s] or aPressedKey[pygame.K_x]:
            self.decelerate()
        
        self.calculateHitboxes()
        self.friction()

        theDeceleration = 0
        if abs(self.steerAngle) > 1.6: theDeceleration += 5 
        if abs(self.steerAngle) > 2.0: theDeceleration += 5
        if abs(self.steerAngle) > 2.4: theDeceleration += 10
        if abs(self.steerAngle) > 2.8: theDeceleration += 10
        
        if self.speed > 0: self.speed -= theDeceleration
        else: self.speed += theDeceleration

        if abs(self.speed) < 10: self.steerAngle = 0

        if aPressedKey[pygame.K_RIGHT] or aPressedKey[pygame.K_d] or aPressedKey[pygame.K_m]:
            self.steerRight()
        elif aPressedKey[pygame.K_LEFT] or aPressedKey[pygame.K_a] or aPressedKey[pygame.K_n]:
            self.steerLeft()

        if aPressedKey[pygame.K_SPACE]:
            self.speed = self.speed + 20

        # reset
        if aPressedKey[pygame.K_r]:
            self.position = (200,200)
        
        

        # Move the car
        self.update(aDelta)

    def accelerate(self):
        """Accelerates the car with a set speed every updatetick.

        Tests:
            * Car can not be faster then the MAXFRONTSPEED 
            * Car does not "Jump" to positive speed when acc while driving backwards
        """
        
        if(self.speed < self.MAXFRONTSPEED): self.speed += 8
    
    def decelerate(self):
        """Decelerates the car with a set speed every updatetick.

        Tests:
            * Car can not be faster then the MAXBACKSPEED
            * Car does not "Jump" to negative speed when breaking
        """

        self.speed -= 8
        if(self.speed < self.MAXBACKSPEED): self.speed = self.MAXBACKSPEED
        # Draw breaking skidmarks
        if(self.speed > 0):
            self.updateSkidmarkOffsetVector()
            self.skidMarkList.append(SkidMark((self.displayPos1.x + self.skidmarkOffsetVector.x, self.displayPos1.y + self.skidmarkOffsetVector.y),degrees(-self.direction), 2, self.speed))
            self.skidMarkList.append(SkidMark((self.displayPos1.x - self.skidmarkOffsetVector.x, self.displayPos1.y - self.skidmarkOffsetVector.y),degrees(-self.direction), 2, self.speed))
    
    def friction(self):
        """Applies driving-directional friction the car every updatetick to slow the car down over time.

        Tests:
            * Car can not be faster then the MAXBACKSPEED
            * Car is getting slowed down over time when not accelerating/decelerating
        """
        deceleration = 3
        if(self.speed > self.currentFrontSpeed * 1.5): deceleration = 25
        if(self.speed > self.currentFrontSpeed * 1.75): deceleration = 50
        if(self.speed > self.currentFrontSpeed * 2): deceleration = 100
        
        if self.speed > 0: self.speed -= deceleration
        else: self.speed += deceleration
        if abs(self.speed) < 5: self.speed = 0

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

        if(len(self.skidMarkList) > self.MAXSKIDMARKS):
            del self.skidMarkList[:2]
    
    def calculateHitboxes(self):
    
        for hitbox in self.hitboxList:            
            if hitbox.checkIfPointIsInside(self.position):
                if hitbox.slowdownFlag:
                    self.currentFrontSpeed = hitbox.maxSpeed
                else:
                   self.speed += hitbox.maxSpeed
              

    def calcWheelPositions(self, dt):
        """Calucates the wheelPosition of the Car. 

        The Code is based on the idea from:
        Source: http://engineeringdotnet.blogspot.com/2010/04/simple-2d-car-physics-in-games.html
        Used on date: April 2021  
        This code has been taken and implemented. However his code works for "traditional driving physics". Meaning: Actual driving with frontwheel steering.
        This was not the scope of this project. So I majorly adjusted the codea and his basic idea, which allows me to simulate a drift.

        Args:
            dt : The timedelta since the last call
        
        Tests:
            * Are the wheels correctly positioned?
            * Does the car not exceed the max speed?
        """

        if(self.speed > 0):
            self.turningWheel = self.position - self.wheelBase/2 * Vector2( cos(self.direction) , sin(self.direction))
            self.frontWheel = self.position + self.wheelBase/2 * Vector2( cos(self.direction) , sin(self.direction))  

            self.frontWheel += self.speed * dt * Vector2(cos(self.direction) , sin(self.direction))
            self.turningWheel += self.speed * dt * Vector2(cos(self.direction+self.steerAngle) , sin(self.direction+self.steerAngle))

            self.position = (self.turningWheel + self.frontWheel) / 2
            self.direction = atan2( self.frontWheel.y - self.turningWheel.y , self.frontWheel.x - self.turningWheel.x )
        else: 
            self.turningWheel = self.position - self.wheelBase/2 * Vector2( cos(self.direction) , sin(self.direction))
            self.frontWheel = self.position + self.wheelBase/2 * Vector2( cos(self.direction) , sin(self.direction))  

            self.turningWheel += self.speed * dt * Vector2(cos(self.direction) , sin(self.direction))
            self.frontWheel += self.speed * dt * Vector2(cos(self.direction+self.steerAngle) , sin(self.direction+self.steerAngle))

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
        self.displayPos1 = self.position - 15 * Vector2( cos(self.direction) , sin(self.direction))
        self.displayPos2 = self.position + 40 * Vector2( cos(self.direction) , sin(self.direction))
        self.displayPos3 = self.position + 50 * Vector2( cos(self.direction) , sin(self.direction))
        self.displayPos4 = self.position + 60 * Vector2( cos(self.direction) , sin(self.direction))
        self.displayPngPosition = self.position + self.pngOffset * Vector2( cos(self.direction) , sin(self.direction))

        self.calcWheelPositions(dt)
        self.calculateSkidMarks()
        
    
    def updateSkidmarkOffsetVector(self):
        """ Updates the skidmarkOffsetVector with the current direction
        Args:
            self: self

        Tests:
            * Is the skidmarkVector at the correct position for the skidmarks?
            * Is the circle overflow correctly calculated?

        """
        theOffsetAngle = degrees(self.direction) + 90 
        if degrees(self.direction) > 90:
            theOffsetAngle -= 360

        self.skidmarkOffsetVector = Vector2(cos(radians(theOffsetAngle)), sin(radians(theOffsetAngle))) * 5

    def calculateSkidMarks(self):
        """ Calculates the need of SkidMarks based of steeringAngle and car speed.

        Args: 
            self: self

        Tests:
            * Are the Skidmarks the correct color?
            * Are the Skidmarks on the correct Position?
            * Are the Skidmarks drawn on the correct layer? (Under the car, over the bg?)
        """
        self.updateSkidmarkOffsetVector()
        if abs(self.steerAngle) > 0.8 and self.speed > 0:

            self.skidMarkList.append(SkidMark((self.displayPos1.x + self.skidmarkOffsetVector.x, self.displayPos1.y + self.skidmarkOffsetVector.y),degrees(-self.direction), self.steerAngle, self.speed))
            self.skidMarkList.append(SkidMark((self.displayPos1.x - self.skidmarkOffsetVector.x, self.displayPos1.y - self.skidmarkOffsetVector.y),degrees(-self.direction), self.steerAngle, self.speed))
        if  0 < self.speed < 100:
            self.skidMarkList.append(SkidMark((self.displayPos1.x + self.skidmarkOffsetVector.x, self.displayPos1.y + self.skidmarkOffsetVector.y),degrees(-self.direction), 2, self.speed))
            self.skidMarkList.append(SkidMark((self.displayPos1.x - self.skidmarkOffsetVector.x, self.displayPos1.y - self.skidmarkOffsetVector.y),degrees(-self.direction), 2, self.speed))
             
                  



