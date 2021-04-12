import os
import pygame
import random
from math import sin, cos, tan,atan2, radians, degrees, copysign
from pygame import Vector2
pygame.font.init()

from car import Car
from skidmark import SkidMark

class Game:
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    theCircleColor = (255, 255, 0)
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
            
            pygame.draw.circle(self.screen, self.theCircleColor, (400, 450), 15, 10)
            pygame.draw.circle(self.screen, self.theCircleColor, (1200, 450 ), 15, 10)
            SkidMark((50, 50),0, 150, 0).update(self.screen,0)
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
