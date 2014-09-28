from Tile import Tileset
from Tile import Map
from Sprites import Sprites

class Modele:
    def __init__(self, parent):
        self.parent = parent
        self.infantry = Sprites.Sprites(32,32,96,128, "Sprites/infantryconfig.cfg")
        self.map = Map.Map("Tile/map1.csv")
        self.tileset = Tileset.Tileset("image/tileset/tileset.png", 64, 64)
        
        print(self.infantry.spriteDict)
        
