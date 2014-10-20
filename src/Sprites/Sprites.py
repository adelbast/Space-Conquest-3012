__author__ = "Arnaud Girardin"

from PIL import Image, ImageTk, ImageEnhance
import configparser

class Sprites:
    def __init__(self):
        self.spriteDict = {}

    def generateSprites(self,spriteW, spriteH, totalW, totalH, cfgPath, folder, brightness):

        cfg = configparser.ConfigParser()
        cfg.read(cfgPath)


        for unit in cfg.sections() :


            sprites = Image.open("Image/sprites/"+folder+"/units/"+unit+".png")
            converter = ImageEnhance.Color(sprites)
            sprites = converter.enhance(brightness)
                
            #Axe verticale pour l'ensemble de spriteset
            for y in range(int(totalH/spriteH)):

                #Axe horizontale pour l'ensemble  de spriteset
                for x in range(int(totalW/spriteW)):
                        
                    img = sprites.crop((x*spriteW,y*spriteH, (x*spriteW)+spriteW, (y*spriteH)+spriteH))

                    if(y == 0):
                        if(x == 0):
                            self.spriteDict.update({unit: {'front' : {str(x): ImageTk.PhotoImage(img)}}})
                        else:
                            self.spriteDict[unit]['front'].update({str(x): ImageTk.PhotoImage(img)})
                    elif(y == 1):
                        if(x == 0):
                            self.spriteDict[unit].update({'left' : {str(x): ImageTk.PhotoImage(img)}})
                        else:
                            self.spriteDict[unit]['left'].update({str(x): ImageTk.PhotoImage(img)})
                    elif(y == 2):
                        if(x == 0):
                            self.spriteDict[unit].update({'right' : {str(x): ImageTk.PhotoImage(img)}})
                        else:
                            self.spriteDict[unit]['right'].update({str(x): ImageTk.PhotoImage(img)})
                    elif(y == 3):
                        if(x == 0):
                            self.spriteDict[unit].update({'back' : {str(x): ImageTk.PhotoImage(img)}})
                        else:
                            self.spriteDict[unit]['back'].update({str(x): ImageTk.PhotoImage(img)})


        #self.spriteDict['trooper']['back']['0'].save("test.png")

    #Fonction qui permet d'obtenir les images   
    def generateBuildingSprites(self, cfgPath, folder, brightness):

        cfg = configparser.ConfigParser()
        cfg.read(cfgPath)


        for building in cfg.sections() :

            sprites = Image.open("Image/sprites/"+folder+"/buildings/"+building+".png")
            converter = ImageEnhance.Color(sprites)
            img = converter.enhance(brightness)

            self.spriteDict.update({building: ImageTk.PhotoImage(img)})

        print(self.spriteDict)
            
            
