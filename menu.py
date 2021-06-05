"""Main Menu of the Car Drifting Game  

    author: JONAS GUGEL
    data: 17.04.2021
    licence: free
    Source: https://pygame-menu.readthedocs.io/en/4.0.4/

    Backgroundimage of the menu as the "You Crashed"-Screen has been taken from the 1998 Game "Asphalt Duel" by Rondomania.
    This Image has been changed and edited.

    Tests: 
        * Does the menu work correctly?
        * Does the Game close correclty?

"""
import os
# Hide pygame prompt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import pygame_menu
from game import Game
from loguru import logger
pygame.init()
#Remove console output
logger.remove()
# add logfile
logger.add("log/file_{time}.log", backtrace=True, diagnose=True)

surface = pygame.display.set_mode((1600, 900))

mytheme = pygame_menu.themes.THEME_DEFAULT

# Set Background Image
myimage = pygame_menu.baseimage.BaseImage(
    image_path="assets/AsphaltDuell_edited.jpg"
)
mytheme.background_color = myimage

def setCarType(value, aCarType):
    """ Sets the car type

    Args:
        value (key/val): the full value
        aCarType (val): the selected carType
    
    Tests:
        * Is the Car set correctly?
        * Is the Car switchable?
    """
    menu.carType = aCarType
    

def setTrack(value, aTrack):
    """ Sets the track

    Args:
        value (key/val): the full value
        aCarType (val): the selected track
    
    Tests:
        * Is the Track set correctly?
        * Is the Track switchable?
    """
    menu.track = aTrack

def setRgbMode(value, aRgb):
    """Sets the RGB Mode

    Args:
        value (key/val): the full value
        aRgb (val): the rgb mode value

    Tests:
        * Is the RGB Mode set correctly?
        * Is the RGB Mode switchable?
    """
    menu.rgb = aRgb

def runGame():
    """ Run the game

    Tests:
        * Does the game run?
        * Does the game stop?
    """
    # Start the game
    logger.success("Starting game with settings: Car Type: " + str(menu.carType) + " Track: "+ str(menu.track))
    myGame = Game(surface, menu.carType, menu.track, menu.rgb)
    myGame.run()

def showControls():
    """ Open a new menu for the Display of the controls

    Tests:
        * Does the control menu open?
        * Does the control menu show the controls?
    """
    controlTheme = pygame_menu.themes.THEME_DEFAULT

    # Set Background Image
    controlImage = pygame_menu.baseimage.BaseImage(
        image_path="assets/Keyboardlayout.jpg"
    )
    controlTheme.background_color = controlImage
    controlMenu = pygame_menu.Menu('Controls', 1600, 900, theme=controlTheme)
    
    # Labels to push back to menu button lower
    controlMenu.add.label("")
    controlMenu.add.label("")
    controlMenu.add.label("")
    controlMenu.add.label("")
    controlMenu.add.label("")
    controlMenu.add.label("")
    controlMenu.add.label("")
    controlMenu.add.label("")
    controlMenu.add.label("")
    controlMenu.add.label("")
    # Quit - back to menu
    controlMenu.add.button('Back to Menu', finishControl)
    menu.controlMenuExit = False
    while not menu.controlMenuExit:     
        controlMenu.mainloop(surface)
def finishControl():
    """ Function to return to the main menu from the controll menu

    Tests:
        * Does the menu close?
        * Does the game behave normally?
    """
    menu.controlMenuExit = True

menu = pygame_menu.Menu('RC DRIFT CAR', 1600, 900, theme=mytheme)

menu.carType = 1
menu.track = 0
menu.rgb = False
# Set menu buttons and selections
menu.add.button('Play', runGame)
menu.add.selector('Car : ', [('Drift Car', 1), ('Race Car', 2)], onchange=setCarType)
menu.add.selector('Track : ', [('Playground', 0), ('Easy', 1), ('Expert', 2)], onchange=setTrack)
menu.add.selector('RGB Mode : ', [('Off', False), ('On', True)], onchange=setRgbMode)
menu.add.button("Controls", showControls)
menu.add.button('Quit', pygame_menu.events.EXIT)

# Start Game
if __name__ == '__main__':
    # Source: https://assetstore.unity.com/packages/audio/music/electronic/super-eurobeat-pack-1-demo-133973
    pygame.mixer.music.load('Music/0EuroBGM1SI-164.wav')
    pygame.mixer.music.play(-1,0.0)
    pygame.mixer.music.set_volume(.1)
    logger.debug("RC Drifting - Menu")
    exit = False
    while not exit:  
        menu.mainloop(surface)
    
