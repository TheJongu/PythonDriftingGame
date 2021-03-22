import os
import pygame
from math import sin, cos, atan2, radians, degrees, copysign
from pygame.math import Vector2

class Car:
    def __init__(self, x, y, aMaxSpeed = 600, aBackSpeed = -100, aMinWheelbase = 50, aMaxWheelbase = 500):
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
    # Process the pressed Buttons on the Keyboard
    def processInputs(self, aPressedKey, aDelta):
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
        if abs(self.steerAngle) > 2.8: theDeceleration += 20
        
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
        self.speed += 3
        if(self.speed > self.MAXFRONTSPEED): self.speed = self.MAXFRONTSPEED
    
    def decelerate(self):
        self.speed -= 8
        if(self.speed < self.MAXBACKSPEED): self.speed = self.MAXBACKSPEED
    
    def friction(self):
        theDeceleration = 5
        if self.speed > 0: self.speed -= theDeceleration
        else: self.speed += theDeceleration
        if abs(self.speed < 20): self.speed = 0

    def steerRight(self):
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
        self.wheelBase = abs(self.speed)/2
        if(self.wheelBase < self.MINWHEELBASE):
            self.wheelBase = self.MINWHEELBASE
        if(self.wheelBase > self.MAXWHEELBASE):
            self.wheelBase = self.MAXWHEELBASE
        
            

    def update(self, dt):

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



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car Drifting Game")
        width = 1280
        height = 720
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
            self.screen.fill((50, 50, 50))
            
            rotated = pygame.transform.rotate(car_image, degrees(-car.direction))
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.displayPos2 - (rect.width / 2, rect.height / 2))
            
            if abs(car.steerAngle) < 1.2:
                pygame.draw.circle(self.screen, (0, 255, 0), (300, 300), 15, 10)
                pygame.draw.circle(self.screen, (0, 255, 0), (900, 300), 15, 10)
            elif abs(car.steerAngle) < 1.6:
                pygame.draw.circle(self.screen, (255, 255, 0), (300, 300), 15, 10)
                pygame.draw.circle(self.screen, (255, 255, 0), (900, 300), 15, 10)
            elif abs(car.steerAngle) >= 1.6:
                pygame.draw.circle(self.screen, (255, 0, 0), (300, 300), 15, 10)
                pygame.draw.circle(self.screen, (255, 0, 0), (900, 300), 15, 10)
            
            #pygame.draw.circle(self.screen, (255,165,0), car.displayPos1, 15, 10)
            #pygame.draw.circle(self.screen, (255,165,0), car.displayPos2, 15, 10)
            #pygame.draw.circle(self.screen, (255,165,0), car.displayPos3, 15, 10)
            #pygame.draw.circle(self.screen, (255,165,0), car.displayPos4, 15, 10)
            #pygame.draw.circle(self.screen, (0,255,0), car.displayPosFront, 5, 10)
            #pygame.draw.circle(self.screen, (255,0,0), car.displayPosBack, 5, 10)
            
            #pygame.draw.circle(self.screen, (100,255,0), car.frontWheel, 5, 10)
            #pygame.draw.circle(self.screen, (255,100,0), car.turningWheel, 5, 10)

           


            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
