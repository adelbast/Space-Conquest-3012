from tkinter import *
import math
from PIL import ImageTk, Image

class Vue:
    def __init__(self, parent):    
        self.parent = parent #Pour l'heritage provenant du Controleur
        self.root = Tk()
        self.root.resizable(0,0)
        self.root.title("RTS")
        self.width = 1200
        self.height = 800
        self.miniMapW = 250
        self.miniMapH = 150
        self.root.geometry(str(self.width)+"x"+str(self.height))

        #Mesures reduites par rapport au canvas original
        self.relativeW = math.floor(self.width*self.miniMapW/(len(self.parent.modele.map.map[0])*64))
        self.relativeH = math.floor(self.height*self.miniMapH/(len(self.parent.modele.map.map)*64))

        #Image pour le HUD
        self.imageHUD = Image.open("gui/gui.png")
        self.photoImageHUD = ImageTk.PhotoImage(self.imageHUD)

        #Pour transferer les images en PhotoImage
        for tile in self.parent.modele.tileset.tileset:
            tile.img = ImageTk.PhotoImage(tile.img)
            
        #Initialisation de la surface de jeu
        self.hud = Canvas(self.root,height=250, width=1200,highlightthickness=0)
        self.miniMap = Canvas(self.root, width=self.miniMapW, height=self.miniMapH, bg='black', highlightthickness=0)
        self.surfaceJeu = Canvas(self.root, width=1200, height=550, bg='white', highlightthickness=0)
        self.surfaceJeu.configure(scrollregion=(0,0,len(self.parent.modele.map.map[0])*64,len(self.parent.modele.map.map)*64))
        print("Map size:", len(self.parent.modele.map.map[0])*64, len(self.parent.modele.map.map)*64)
        self.surfaceJeu.place(x=0, y=0)
        
        self.displayMap()
        self.displayMiniMap()
        self.updateMiniMap()
        self.displayHUD()
        

        #Pour que le canvas scroll lorsquon click
        self.root.bind("<Key>", self.scroll_move)
        
    

    def scroll_move(self, event):
        variation = 1
        
        if(event.char == 'w'):
            print('up')
            self.surfaceJeu.yview('scroll', -variation, 'units')

        if(event.char == 's'):
            print("down")
            self.surfaceJeu.yview('scroll', variation, 'units')

        if(event.char == 'a'):
            print("left")
            self.surfaceJeu.xview('scroll', -variation, 'units')
            
        if(event.char == 'd'):
            print("right")
            self.surfaceJeu.xview('scroll', variation, 'units')

        print(self.surfaceJeu.canvasx(0), self.surfaceJeu.canvasy(0))

        self.updateMiniMap()
        
       
        

    def displayMap(self):
        
        #Pour chaque ligne
        for y in range(0, len(self.parent.modele.map.map)):

            #Pour chaque colone
            for x in range(0, len(self.parent.modele.map.map[0])):

             
                self.surfaceJeu.create_image(x*64,y*64,anchor=NW, image=self.parent.modele.tileset.tileset[int(self.parent.modele.map.map[y][x])].img, tags="tile")

                
    def displayHUD(self):
        self.hud.create_image(0,0,anchor=NW,image=self.photoImageHUD, tags="hud")
        self.hud.place(x=0, y=550)

    def displayMiniMap(self):      
        self.miniMap.place(x=928, y=600)
    
    def updateMiniMap(self):
        self.miniMap.delete("region")

        #Conversion des positions
        posx = math.floor(self.surfaceJeu.canvasx(0)*self.miniMapW/(len(self.parent.modele.map.map[0])*64))
        posy = math.floor(self.surfaceJeu.canvasy(0)*self.miniMapH/(len(self.parent.modele.map.map)*64))
        
        self.miniMap.create_rectangle(posx, posy, posx + self.relativeW, posy + self.relativeH - 12, outline='red', tags="region")
        
        
