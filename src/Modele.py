from Tile import Tileset
from Tile import Map

class Modele:
    def __init__(self, parent):
        self.parent = parent
        self.map = Map.Map("Tile/map1.csv")
        self.tileset = Tileset.Tileset("Tile/tileset.png", 64, 64)
        print(self.tileset.tileset[0].name)
        
    
        
