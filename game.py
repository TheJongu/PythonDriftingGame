import os
import pygame
from math import sin, cos, atan2, radians, degrees, copysign
from pygame.math import Vector2

class Car:
    def __init__(self, x, y):
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

        if aPressedKey[pygame.K_RIGHT]:
            self.steerRight()
        elif aPressedKey[pygame.K_LEFT]:
            self.steerLeft()
       
            
        # Move the car
        self.update(aDelta)

    def accelerate(self):
        self.speed += 2
        if(self.speed > 600): self.speed = 600
    
    def decelerate(self):
        self.speed -= 8
        if(self.speed < -100): self.speed = -100
    
    def friction(self):
        if self.speed > 0: self.speed -= 5
        else: self.speed += 5
        if abs(self.speed < 10): self.speed = 0

    def steerRight(self):
        if abs(self.speed) > 0:
            self.steerAngle -= .05
            if(abs(self.steerAngle) > 2): self.steerAngle = -2
        else:
            self.steerAngle = 0
    def steerLeft(self):
        if abs(self.speed) > 0:
            self.steerAngle += .05
            if(abs(self.steerAngle) > 2): self.steerAngle = 2
        else:
            self.steerAngle = 0

    def calcWheelBase(self):
        self.wheelBase = abs(self.speed)/2
        if(self.wheelBase < 50):
            self.wheelBase = 50
        if(self.wheelBase > 300):
            self.wheelBase = 300
        
            

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
        car = Car(0, 0)
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
            
            pygame.draw.circle(self.screen, (100, 100, 100), car.displayPos1, 15, 10)
            pygame.draw.circle(self.screen, (100, 100, 100), car.displayPos2, 15, 10)
            pygame.draw.circle(self.screen, (100, 100, 100), car.displayPos3, 15, 10)
            pygame.draw.circle(self.screen, (100, 100, 100), car.displayPos4, 15, 10)
            pygame.draw.circle(self.screen, (0,255,0), car.displayPosFront, 5, 10)
            pygame.draw.circle(self.screen, (255,0,0), car.displayPosBack, 5, 10)

            #pygame.draw.circle(self.screen, (100,255,0), car.frontWheel, 5, 10)
            #pygame.draw.circle(self.screen, (255,100,0), car.turningWheel, 5, 10)


            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
