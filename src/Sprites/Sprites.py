__author__ = "Arnaud Girardin"

from PIL import Image
import configparser

class Sprites:
    def __init__(self, spriteW, spriteH, totalW, totalH, cfgPath):
        self.spriteW = spriteW
        self.spriteH = spriteH
        self.totalW = totalW
        self.totalH = totalH
        self.cfgPath = cfgPath
        self.spriteDict = {}

        self.generateSprites()

    def generateSprites(self):

        cfg = configparser.ConfigParser()
        cfg.read(self.cfgPath)


        for unit in cfg.sections() :


            sprites = Image.open("Sprites/Sprites/"+unit+".png")
                
            #Axe verticale pour l'ensemble de spriteset
            for y in range(int(self.totalH/self.spriteH)):

                #Axe horizontale pour l'ensemble  de spriteset
                for x in range(int(self.totalW/self.spriteW)):
                        
                    img = sprites.crop((x*self.spriteW,y*self.spriteH, (x*self.spriteW)+self.spriteW, (y*self.spriteH)+self.spriteH))

                    if(y == 0):
                        if(x == 0):
                            self.spriteDict.update({unit: {'front' : {str(x): img}}})
                        else:
                            self.spriteDict[unit]['front'].update({str(x): img})
                    elif(y == 1):
                        if(x == 0):
                            self.spriteDict[unit].update({'left' : {str(x): img}})
                        else:
                            self.spriteDict[unit]['left'].update({str(x): img})
                    elif(y == 2):
                        if(x == 0):
                            self.spriteDict[unit].update({'right' : {str(x): img}})
                        else:
                            self.spriteDict[unit]['right'].update({str(x): img})
                    elif(y == 3):
                        if(x == 0):
                            self.spriteDict[unit].update({'back' : {str(x): img}})
                        else:
                            self.spriteDict[unit]['back'].update({str(x): img})

                  
            
        

        
