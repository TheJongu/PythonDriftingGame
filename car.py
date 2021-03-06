"""
    author: JONAS GUGEL
    data: 19.03.2021
    licence: free

"""

import pygame
import random
from math import sin, cos, sqrt, log2,atan2, radians, degrees
from pygame import Vector2
from skidmark import SkidMark
from hitbox import Hitbox
from loguru import logger

class Car:
    """A class to represent the driving car on screen with the necessary calculations to simulate the driving physics.

    Tests:
        * Does the driving feel realistic?
        * Does the drifting work fine?
        * Can the car be a drift car and a race car?

    """


    def __init__(self, x, y, aMaxSpeed = 600, aBackSpeed = -100, aMinWheelbase = 50, aMaxWheelbase = 500, aHitboxList=[], aCarType = 1, aRgbFlag = False):
        """Inits the car with parameters, which change the cars behaviour.

        Args:
            x (int): x Startposition of the car
            y (int): y Startposition of the car
            aMaxSpeed (int, optional): max speed the car can go forward. Defaults to 600.
            aBackSpeed (int, optional): max speed the car can go reverse. Defaults to -100.
            aMinWheelbase (int, optional): the minimum distance the simulated wheels can be appart, usually when slow/standing, impacts slow turing. Defaults to 50.
            aMaxWheelbase (int, optional): the maximum distance the simulated wheels can be appart, usually when highspeed, impacts the drifting handling massively. Defaults to 500.
            aCarType (int, optional): Car type, 1 = driftcar, 2 = racecar
            aRgbFlag (boolean, optional): Rgb Flag, turns the skidmarks to rgb

        SOURCES:   
            Car pictures have been taken from:
                Drift-Car: https://de.123rf.com/photo_78087079_scarlet-red-modern-super-sports-car-top-down-view.html?vti=lfl0avz5gsvt0516rl-1-3
                Race-Car (F1): https://niharikaghorpade.wordpress.com/2018/02/24/2018-f1-car-launch-mclaren-mcl33/
            They have been edited by me to remove backgrounds
        """
        
        # Constants
        self.MAXFRONTSPEED = aMaxSpeed
        self.MAXBACKSPEED = aBackSpeed
        self.MINWHEELBASE = aMinWheelbase
        self.MAXWHEELBASE = aMaxWheelbase
        self.MAXSKIDMARKS = 5000
        self.position = Vector2(x, y)
        self.rgbFlag = aRgbFlag
        # Vectors
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
            logger.success("Car Created - Driftcar")
            self.carImage = "assets/drift_car.png"
            self.driftcarFlag = True
        if aCarType == 2:
            logger.success("Car Created - Racecar")
            self.carImage = "assets/race_car.png"
            self.driftcarFlag = False
        
            

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

        # steer left - W, C, ^
        if aPressedKey[pygame.K_UP] or aPressedKey[pygame.K_w] or aPressedKey[pygame.K_c]:
            self.accelerate()
        # steer left - S, X, (arrow down) 
        elif aPressedKey[pygame.K_DOWN] or aPressedKey[pygame.K_s] or aPressedKey[pygame.K_x]:
            self.decelerate()
        
        self.calculateHitboxes()
        self.friction()

        # Deceleration for drifting to hard, added to the friction
        theDeceleration = 0
        if abs(self.steerAngle) > 1.6: theDeceleration += 5 
        if abs(self.steerAngle) > 2.0: theDeceleration += 5
        if abs(self.steerAngle) > 2.4: theDeceleration += 10
        if abs(self.steerAngle) > 2.8: theDeceleration += 10
        
        if self.speed > 0: self.speed -= theDeceleration
        else: self.speed += theDeceleration

        if abs(self.speed) < 10: self.steerAngle = 0

        # steer right - D, M, ->
        if aPressedKey[pygame.K_RIGHT] or aPressedKey[pygame.K_d] or aPressedKey[pygame.K_m]:
            if(self.driftcarFlag):
                self.steerRightDrift()
            else:
                self.steerRightRace()
        # steer left - A, N, <-
        elif aPressedKey[pygame.K_LEFT] or aPressedKey[pygame.K_a] or aPressedKey[pygame.K_n]:
            if(self.driftcarFlag):
                self.steerLeftDrift()
            else:
                self.steerLeftRace()
        # Race car goes straight if not turing
        elif not self.driftcarFlag:
            self.steerAngle = 0
        else:
            self.decreaseSteeringDrift()
        # Speedboost
        if aPressedKey[pygame.K_SPACE]:
            self.speed = self.speed + 20

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

    def steerRightDrift(self):
        """Steers the car right with a set turningangle every updatetick. Steering made for drifting.

        The more the car is already turning, the longer it takes the car to turn more. This is so, that the car is easier drivable with a keyboard

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
    def steerLeftDrift(self):
        """Steers the car left with a set turningangle every updatetick. Steering made for drifting.
        The more the car is already turning, the longer it takes the car to turn more. This is so, that the car is easier drivable with a keyboard

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

    def decreaseSteeringDrift(self):
        """Decrease the steering angle of the drift car over time, so it moves to the middle, like in a real car.
        For more intuitive steering

        Tests: 
            * Does the car steer back?
            * Does it feel "right" and not iritating?
        """
        if self.steerAngle > 0.05:
            self.steerAngle -= 0.025
        if self.steerAngle < -0.05:
            self.steerAngle += 0.025
            

    def steerRightRace(self):
        """Steers the car right with a set turningangle every updatetick. Steering made for race car driving.

        Race-Steering is based on speed, the faster, the less turing.

        Tests:
            * Car turns in to the right when button is pressed
            * Car turns slower the faster it is
            * After releasing the button, the car doesnt steer anymore
        """
        if abs(self.speed) > 0:
            if self.speed < 300:   self.steerAngle = 0.85
            elif self.speed < 350:   self.steerAngle = 0.60
            elif self.speed < 450:   self.steerAngle = 0.40
            elif self.speed < 800:   self.steerAngle = 0.10
        else:
            self.steerAngle = 0

    def steerLeftRace(self):
        """Steers the car left with a set turningangle every updatetick. Steering made for race car driving.

        Race-Steering is based on speed, the faster, the less turing.

        Tests:
            * Car turns in to the right when button is pressed
            * Car turns slower the faster it is
            * After releasing the button, the car doesnt steer anymore
        """
        if abs(self.speed) > 0:
            if self.speed < 300:   self.steerAngle = -0.85
            elif self.speed < 350:   self.steerAngle = -0.60
            elif self.speed < 450:   self.steerAngle = -0.40
            elif self.speed < 800:   self.steerAngle = -0.10
        else:
            self.steerAngle = 0

    def calcWheelBase(self):
        """ Calculates the wheelbase based on the speed. The faster the car is, the further appart the two simulated wheels are, until the MAXWHEELBASE is hit.
        The slower the car is, the shorter the wheelbase is, with a minimum of MINWHEELBASE 

        Tests:
            * The Wheelbase of the car can not be smaller/bigger then the defined MINWHEELBASE/MAXWHEELBASE of the car?
            * The calculation is correct?
        """       
        if(self.driftcarFlag):
            self.wheelBase = abs(self.speed)/2
            
            if(self.wheelBase < self.MINWHEELBASE):
                self.wheelBase = self.MINWHEELBASE
            if(self.wheelBase > self.MAXWHEELBASE):
                self.wheelBase = self.MAXWHEELBASE
        else:
            self.wheelBase = abs(self.speed)/4
            if(self.wheelBase < 25):
                self.wheelBase = 25

    

    def drawSkidMarks(self, aScreen):  
        """ Draws the skidmarks of the car.
        TODO: Skidmarks are to be reworked: 
            As own class and objects - with fadeout and turing in the car direction

        Args:
            aScreen (pygame.surface): the screen the skidmarks are to be drawn to

        Tests:
            * Skidmars are being drawn?
            * If too many SkidMarks exist, the last 2 are deleted?
            * The Game can handle the amount of SkidMarks?
            * Change the Skidmarks color?
        """     
        for aSkidMark in self.skidMarkList:
            aSkidMark.update(aScreen,0, self.rgbFlag)

        if(len(self.skidMarkList) > self.MAXSKIDMARKS):
            del self.skidMarkList[:2]
    
    def calculateHitboxes(self):
        """Calculate if the car is in one of the tracks hitboxes. Slow the car down if it is a slowing hitbox. Speed it up if it is a boost-pad

        Tests:
            * Is the car correctly slowed down?
            * Do speedpad and graveltraps work?
        """
        for hitbox in self.hitboxList:            
            if hitbox.checkIfPointIsInside(self.position):
                logger.debug("Car is in a Hitbox: - \tCar Position:" + str(self.position) + " \tHitbox Pos1:" + str(hitbox.position1)+ " \tHitbox Pos2:" + str(hitbox.position2))
                if hitbox.slowdownFlag:
                    self.currentFrontSpeed = hitbox.maxSpeed
                else:
                   self.speed += hitbox.maxSpeed
              

    def calcWheelPositions(self, dt):
        """Calucates the wheelPosition of the Car. 

        

        Args:
            dt : The timedelta since the last call
        
        Tests:
            * Are the wheels correctly positioned?
            * Does the car not exceed the max speed?
        """

        if(self.speed > 0 and self.driftcarFlag):
            self.backWheelTurningWheel(dt)
        elif(self.speed < 0 and self.driftcarFlag): 
            self.frontWheelTurningWheel(dt)
        elif(self.speed > 0 and not self.driftcarFlag):
            self.frontWheelTurningWheel(dt)
        else: 
            self.frontWheelTurningWheel(dt)

    def backWheelTurningWheel(self, dt):    
        """Calculate the wheel positions with the backwheel turning.
        The Code is based on the idea from:
        Source: http://engineeringdotnet.blogspot.com/2010/04/simple-2d-car-physics-in-games.html
        Used on date: April 2021  
        This code has been taken and implemented. However his code works for "traditional driving physics". Meaning: Actual driving with frontwheel steering.
        This was not the scope of this project. So I majorly adjusted the code and his basic idea, which allows me to simulate a drift.
        This has been done by changing the wheelbase based on the speed of the car.
        For the Race car the Wheelbase is only slightly adjusted to sim grip.

        Args:
            dt : The timedelta since the last call

        Tests:
            * Are the tires positions correctly?
            * Does driving backwards work?

        """    
        self.turningWheel = self.position - self.wheelBase/2 * Vector2( cos(self.direction) , sin(self.direction))
        self.frontWheel = self.position + self.wheelBase/2 * Vector2( cos(self.direction) , sin(self.direction))  

        self.frontWheel += self.speed * dt * Vector2(cos(self.direction) , sin(self.direction))
        self.turningWheel += self.speed * dt * Vector2(cos(self.direction+self.steerAngle) , sin(self.direction+self.steerAngle))

        self.position = (self.turningWheel + self.frontWheel) / 2
        self.direction = atan2( self.frontWheel.y - self.turningWheel.y , self.frontWheel.x - self.turningWheel.x )

    def frontWheelTurningWheel(self, dt):
        """Calculate the wheel positions with the fronwheel turning.
        The Code is based on the idea from:
        Source: http://engineeringdotnet.blogspot.com/2010/04/simple-2d-car-physics-in-games.html
        Used on date: April 2021  
        This code has been taken and implemented. However his code works for "traditional driving physics". Meaning: Actual driving with frontwheel steering.
        This was not the scope of this project. So I majorly adjusted the code and his basic idea, which allows me to simulate a drift.
        This has been done by changing the wheelbase based on the speed of the car.
        For the Race car the Wheelbase is only slightly adjusted to sim grip.

        Args:
            dt : The timedelta since the last call

        Tests:
            * Are the tires positions correctly?
            * Does driving backwards work?
        """    
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
        # Display Postions for Car and Debugging
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
             
                  



