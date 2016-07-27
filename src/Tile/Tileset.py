__author__ = "Arnaud Girardin"

from PIL import Image
import configparser
from os.path import dirname
class Tileset:
    def __init__(self, tilesetImg, tileWidth, tileHeight):
        self.tilesetImg = Image.open(tilesetImg)
        self.tileWidth = tileWidth    #Largeur d'une tile
        self.tileHeight = tileHeight    #Hauteur d'une tile
        self.tileset = []

        self.generateTileset()

    #Fonction qui genere un tileset avec la tilesetImg
    def generateTileset(self):

        cfg = configparser.ConfigParser()
        cfg.read(dirname(__file__) + '/tileconfig.cfg')

        #Variables contenant la grandeur total de l'image
        (totalWidth, totalHeight) = self.tilesetImg.size
        print(totalWidth, totalHeight)

        #Pour chaque Ligne
        for y in range(0, int(totalHeight/self.tileHeight)):
            #Pour chaque colonne
            for x in range(0, int(totalWidth/self.tileWidth)):

                #Variable pour savoir si la pixel de la tile est transparente
                isTransparent = True
                
                #Si la premiere pixel de la case n'est pas transparente
                for i in self.tilesetImg.getpixel((x*self.tileWidth,y*self.tileHeight)):
                    #print(i)
                    if i != 0:
                        isTransparent = False
                        break

                #Si la tile n'est pas transparente
                if not isTransparent:

                    #Image temporaire pour la tile
                    img = self.tilesetImg.crop((x*self.tileWidth,y*self.tileHeight, (x*self.tileWidth)+self.tileWidth, (y*self.tileHeight)+self.tileHeight))
                    
                    tilecfg = cfg[str((y*10)+x)]
                    
                    self.tileset.append(Tile(tilecfg['name'], tilecfg.getboolean('Walkable'), tilecfg.getboolean('Flyable'), img))
                    
                    #print(self.tileset[len(self.tileset)-1].name, self.tileset[len(self.tileset)-1].isWalkable, self.tileset[len(self.tileset)-1].isFlyable)

                    
                #Le tileset est termine
                else:
                    return

                    
class Tile:
    def __init__(self, name, isWalkable, isFlyable, img):
        self.name = name
        self.isWalkable = isWalkable
        self.isFlyable = isFlyable
        self.img = img
        self.pImg = None
