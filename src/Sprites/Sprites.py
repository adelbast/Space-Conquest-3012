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


        for i in range (0, len(cfg.sections())):

            print(i)
            
            spritecfg = cfg[str(i)]

            sprites = Image.open("Sprites/Sprites/"+spritecfg['name']+".png")
                
            #Axe verticale pour l'ensemble de spriteset
            for y in range(int(self.totalH/self.spriteH)):

                #Axe horizontale pour l'ensemble  de spriteset
                for x in range(int(self.totalW/self.spriteW)):
                        
                    img = sprites.crop((x*self.spriteW,y*self.spriteH, (x*self.spriteW)+self.spriteW, (y*self.spriteH)+self.spriteH))

                    if(y == 0):
                        if(x == 0):
                            self.spriteDict.update({spritecfg['name']: {'front' : {str(x): img}}})
                        else:
                            self.spriteDict[spritecfg['name']]['front'].update({str(x): img})
                    elif(y == 1):
                        if(x == 0):
                            self.spriteDict[spritecfg['name']].update({'left' : {str(x): img}})
                        else:
                            self.spriteDict[spritecfg['name']]['left'].update({str(x): img})
                    elif(y == 2):
                        if(x == 0):
                            self.spriteDict[spritecfg['name']].update({'right' : {str(x): img}})
                        else:
                            self.spriteDict[spritecfg['name']]['right'].update({str(x): img})
                    elif(y == 3):
                        if(x == 0):
                            self.spriteDict[spritecfg['name']].update({'back' : {str(x): img}})
                        else:
                            self.spriteDict[spritecfg['name']]['back'].update({str(x): img})

                  
            
        

        
