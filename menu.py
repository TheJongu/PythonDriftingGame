"""Main Menu of the Car Drifting Game

    author: JONAS GUGEL
    data: 17.04.2021
    licence: free
    Source: https://pygame-menu.readthedocs.io/en/4.0.4/

    Backgroundimage of the menu has been taken from the 1998 Game "Asphalt Duel" by Rondomania.
    This Image has been changed and edited.

"""
import os
# Hide pygame prompt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import pygame_menu
from game import Game
from loguru import logger
pygame.init()
logger.add("log/file_{time}.log", backtrace=True, diagnose=True)
surface = pygame.display.set_mode((1600, 900))

mytheme = pygame_menu.themes.THEME_DEFAULT

# Set Background Image
myimage = pygame_menu.baseimage.BaseImage(
    image_path="tracks/AsphaltDuell_edited.jpg"
)
mytheme.background_color = myimage

def setCarType(value, aCarType):
    """ Sets the car type

    Args:
        value (key/val): the full value
        aCarType (val): the selected carType
    """
    menu.carType = aCarType
    

def setTrack(value, aTrack):
    """ Sets the track

    Args:
        value (key/val): the full value
        aCarType (val): the selected track
    """
    menu.track = aTrack

def runGame():
    """ Run the game
    """
    # Start the game
    logger.success("Starting game with settings: Car Type: " + str(menu.carType) + " Track: "+ str(menu.track))
    myGame = Game(surface, menu.carType, menu.track)
    myGame.run()

menu = pygame_menu.Menu('RC DRIFT CAR', 1600, 900, theme=mytheme)

menu.carType = 1
menu.track = 1
# Set menu buttons and selections
menu.add.button('Play', runGame)
menu.add.selector('Car : ', [('Drift Car', 1), ('Race Car', 2)], onchange=setCarType)
menu.add.selector('Track : ', [('Easy', 1), ('Expert', 2)], onchange=setTrack)
menu.add.button('Quit', pygame_menu.events.EXIT)

# Start Game
if __name__ == '__main__':
    logger.debug("RC Drifting - Menu")
    exit = False
    while not exit:  
        menu.mainloop(surface)
    
