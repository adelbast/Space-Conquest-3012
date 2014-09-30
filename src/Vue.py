from tkinter import *
import math
from PIL import ImageTk, Image
import os

class Vue:
    def __init__(self, parent):    
        self.parent = parent #Pour l'heritage provenant du Controleur
        self.root = Tk()
        self.root.resizable(0,0)
        self.root.title("RTS")

        #Mesures de la fenetre
        self.windowWidth = 1200
        self.windowHeight = 800

        #Mesures de la minimap
        self.miniMapW = 250
        self.miniMapH = 150

        #Mesures de la surface de jeu
        self.surfaceW = 1200
        self.surfaceH = 550

        self.root.geometry(str(self.windowWidth)+"x"+str(self.windowHeight))

        #Mesures reduites par rapport au canvas original
        self.relativeW = math.floor(self.surfaceW*self.miniMapW/(len(self.parent.modele.map.map[0])*64))
        self.relativeH = math.floor(self.surfaceH*self.miniMapH/(len(self.parent.modele.map.map)*64))

        print(self.relativeW, self.relativeH)

        #Image pour le HUD
        self.imageHUD = Image.open("image/gui/gui.png")
        self.photoImageHUD = ImageTk.PhotoImage(self.imageHUD)

        #Pour transferer les images en PhotoImage
        for tile in self.parent.modele.tileset.tileset:
            tile.img = ImageTk.PhotoImage(tile.img)
            
        #Initialisation de la surface de jeu
        self.hud = Canvas(self.root,height=250, width=1200,highlightthickness=0)
        self.miniMap = Canvas(self.root, width=self.miniMapW, height=self.miniMapH, bg='black', highlightthickness=0)
        self.surfaceJeu = Canvas(self.root, width=self.surfaceW, height=self.surfaceH, bg='white', highlightthickness=0)
        self.surfaceJeu.configure(scrollregion=(0,0,len(self.parent.modele.map.map[0])*64,len(self.parent.modele.map.map)*64))
        print("Map size:", len(self.parent.modele.map.map[0])*64, len(self.parent.modele.map.map)*64)
        self.surfaceJeu.place(x=0, y=0)
        
        self.displayMap()
        self.displayMiniMap()
        self.updateMiniMap()
        self.displayHUD()
        

        #Pour que le canvas scroll lorsquon click
        self.root.bind("<Key>", self.scroll_move)

        #Pour le click sur la map
        self.miniMap.bind("<Button-1>", self.miniMapClick)
        
    

    #Deplacement de la map avec WASD
    def scroll_move(self, event):
        variation = 1
        
        if(event.char == 'w'):
            print('up')
            self.surfaceJeu.yview('scroll', -variation, 'units')

        elif(event.char == 's'):
            print("down")
            self.surfaceJeu.yview('scroll', variation, 'units')

        elif(event.char == 'a'):
            print("left")
            self.surfaceJeu.xview('scroll', -variation, 'units')
            
        elif(event.char == 'd'):
            print("right")
            self.surfaceJeu.xview('scroll', variation, 'units')

        print(self.surfaceJeu.canvasx(0), self.surfaceJeu.canvasy(0))

        self.updateMiniMap()

    #Deplacer la camera lorsqu'on clique sur le canvas de la minimap
    def miniMapClick(self, event):
        print(event.x, event.y)

        #Calcule le coin en haut a gauche du rectangle pour que le point clique soit le centre
        posx = event.x-(self.relativeW/2)
        posy = event.y-(self.relativeH/2)

        if(posx < 0):
            posx = 0
            
        elif(posx > self.miniMapW-(self.relativeW)):
            posx = self.miniMapW-self.relativeW-1

        if(posy < 0):
            posy = 0
            
        elif(posy > self.miniMapH-(self.relativeH)):
            posy = self.miniMapH-self.relativeH-1
            

        self.miniMap.delete("region")
        self.miniMap.create_rectangle(posx, posy, posx + self.relativeW, posy + self.relativeH, outline='red', tags="region")

        print((posx*(len(self.parent.modele.map.map[0])*64))/self.miniMapW, (posy*(len(self.parent.modele.map.map)*64))/self.miniMapH)

        self.surfaceJeu.xview_moveto(posx*1/self.miniMapW)
        self.surfaceJeu.yview_moveto(posy*1/self.miniMapH)
       
        
    #Affiche la map
    def displayMap(self):
        
        #Pour chaque ligne
        for y in range(0, len(self.parent.modele.map.map)):

            #Pour chaque colone
            for x in range(0, len(self.parent.modele.map.map[0])):

             
                self.surfaceJeu.create_image(x*64,y*64,anchor=NW, image=self.parent.modele.tileset.tileset[int(self.parent.modele.map.map[y][x])].img, tags="tile")

              
    #Affiche le HUD
    def displayHUD(self):
        self.hud.create_image(0,0,anchor=NW,image=self.photoImageHUD, tags="hud")
        self.hud.place(x=0, y=550)

    #Affiche la minimap a la bonne position
    def displayMiniMap(self):      
        self.miniMap.place(x=928, y=600)

    #Update la camera sur la minimap et aussi l'affichage des unites
    def updateMiniMap(self):
        self.miniMap.delete("region")

        #Conversion des positions
        posx = math.floor(self.surfaceJeu.canvasx(0)*self.miniMapW/(len(self.parent.modele.map.map[0])*64))
        posy = math.floor(self.surfaceJeu.canvasy(0)*self.miniMapH/(len(self.parent.modele.map.map)*64))
        
        self.miniMap.create_rectangle(posx, posy, posx + self.relativeW, posy + self.relativeH, outline='red', tags="region")
        
        
