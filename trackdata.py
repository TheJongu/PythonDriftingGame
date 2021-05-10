"""

    author: JONAS GUGEL
    data: 19.03.2021
    licence: free

"""
import pygame as py
from pygame import Vector2
from hitbox import Hitbox

class Trackdata:
    """A Object which holds all the information about the tracks available in the game.
    
    Source for the baseassets of the race track, which have been modified:
    https://opengameart.org/content/race-track-tiles-0


    """
    def __init__(self):
        """Inits trackdata and creates all the hitboxes for the tracks
        """
        self.track01_hitboxes = []
        self.track01_checkpoints = []

        ### Track 01
        # Outside, on screen hitbox
        self.track01_hitboxes.append(Hitbox((0,0),       (1600,15),      50))
        self.track01_hitboxes.append(Hitbox((0,0),       (15,900),       50))
        self.track01_hitboxes.append(Hitbox((0,880),     (1600,900),     50))
        self.track01_hitboxes.append(Hitbox((1580,0),    (1600,900),     50))

        # Grass
        self.track01_hitboxes.append(Hitbox((256,256),   (1060,560),     150))
        self.track01_hitboxes.append(Hitbox((1060,256),  (1250,400),     150))
        self.track01_hitboxes.append(Hitbox((320,560),   (1060,640),     150))

        # Graveltraps
        self.track01_hitboxes.append(Hitbox((780,400),   (1050,720),      100))
        self.track01_hitboxes.append(Hitbox((1330,650),  (1590,880),     100))

        ## Checkpoints
        # right
        self.track01_checkpoints.append(Hitbox((1350, 360),   (1580,380),      0,    False,       True))
        # bottom
        self.track01_checkpoints.append(Hitbox((720, 650),   (740,880),      0,    False,       True))
        # left
        self.track01_checkpoints.append(Hitbox((15, 370),   (240,390),      0,    False,       True))
        # start/finish
        self.track01_checkpoints.append(Hitbox((1053, 20),   (1077,234),      0,    False,       True))

        ### Track 2
        self.track02_hitboxes = []
        self.track02_checkpoints = []

        # Checkpoints
        
        # split top 
        self.track02_checkpoints.append(Hitbox((1305, 229),   (1325,367),      0,    False,       True))
        # top middle right
        self.track02_checkpoints.append(Hitbox((1292, 15),   (1312,165),      0,    False,       True))
        # before 1st cross
        self.track02_checkpoints.append(Hitbox((987, 280),   (1140,300),      0,    False,       True))
        # after 1st cross
        self.track02_checkpoints.append(Hitbox((987, 545),   (1140,565),      0,    False,       True))
        # before 2nd cross
        self.track02_checkpoints.append(Hitbox((468, 490),   (620,470),      0,    False,       True))
        # after 2nd cross
        self.track02_checkpoints.append(Hitbox((468, 226),   (620,206),      0,    False,       True))
        # top left
        self.track02_checkpoints.append(Hitbox((195, 34),   (215,193),      0,    False,       True))
        # before merge
        self.track02_checkpoints.append(Hitbox((300, 228),   (320,376),      0,    False,       True))
        # start/finish, passby
        self.track02_checkpoints.append(Hitbox((934, 313),   (957,457),      0,    False,       True))

        # split bottom 
        self.track02_checkpoints.append(Hitbox((1306, 390),   (1326,532),      0,    False,       True))
        # after right turn
        self.track02_checkpoints.append(Hitbox((1290, 717),   (1310,880),      0,    False,       True))
        # after straight
        self.track02_checkpoints.append(Hitbox((320, 717),   (340,880),      0,    False,       True))
        # before merge
        self.track02_checkpoints.append(Hitbox((296, 392),   (316,541),      0,    False,       True))

        # start/finish, actually now
        self.track02_checkpoints.append(Hitbox((934, 313),   (957,457),      0,    False,       True))
        
        

    

        