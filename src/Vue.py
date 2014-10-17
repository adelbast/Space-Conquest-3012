from tkinter import *
import math
from PIL import ImageTk, Image
from Tile import Tileset
from Sprites.Sprites import Sprites
import os

class Vue:
    def __init__(self, parent):    
        self.parent = parent #Pour l'heritage provenant du Controleur
        self.root = Tk()
        self.root.resizable(0,0)
        self.root.title("Space Conquest 3012")

        #Creation du Tileset
        self.tileset = Tileset.Tileset("Image/tileset/tileset.png",64,64)

        self.sprites = []

        #Mesures de la fenetre
        self.windowWidth = 1200
        self.windowHeight = 800

        #Mesures de la minimap
        self.miniMapW = 250
        self.miniMapH = 150
        self.miniMapImage = None

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
        for tile in self.tileset.tileset: 
            tile.pImg = ImageTk.PhotoImage(tile.img)
            
        #Initialisation de la surface de jeu
        self.hud = Canvas(self.root,height=250, width=1200,highlightthickness=0)
        self.miniMap = Canvas(self.root, width=self.miniMapW, height=self.miniMapH, bg='black', highlightthickness=0)
        self.surfaceJeu = Canvas(self.root, width=self.surfaceW, height=self.surfaceH, bg='white', highlightthickness=0)
        self.surfaceJeu.configure(scrollregion=(0,0,len(self.parent.modele.map.map[0])*64,len(self.parent.modele.map.map)*64))
        print("Map size:", len(self.parent.modele.map.map[0])*64, len(self.parent.modele.map.map)*64)
        self.surfaceJeu.place(x=0, y=0)
        
        #Pour la fermeture de la fenetre de jeu (afin de pouvoir compléter des actions avant de quitter le programme)
        self.root.protocol( "WM_DELETE_WINDOW", self.parent.fermeture )

        #Pour que le canvas scroll lorsquon click
        self.root.bind("<Key>", self.scroll_move)

        #Pour le click sur la map
        self.miniMap.bind("<Button-1>", self.miniMapClick)
        self.miniMap.bind("<B1-Motion>", self.miniMapClick)

        #Pour les clicks sur la surface de jeu
        self.surfaceJeu.bind("<B1-Motion>", self.parent.gererMouseDrag)
        self.surfaceJeu.bind("<Button-1>",self.parent.gererMouseClick)
        self.surfaceJeu.bind("<ButtonRelease-1>",self.parent.gererMouseRelease)
        self.surfaceJeu.bind("<ButtonRelease-3>", self.parent.gererMouseRelease)

        #TEST BOUTON HUD JUSTE TEST, PAS DEFINITIF
        boutonCreerUnit = Button(self.hud,text="creerUnite",command=lambda:self.parent.modele.listeJoueur[1].creerUnite("psychonaut",(300,300) , self.parent.modele.dictUnit["psychonaut"] ))
        boutonCreerUnit.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
        boutonCreerUnit_window = self.hud.create_window(320, 40, anchor=NW, window=boutonCreerUnit)

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

    def getSurfacePos(self):
        return (self.surfaceJeu.canvasx(0), self.surfaceJeu.canvasy(0))

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

    #Generation des sprites pour chacun des joueurs
    def generateSpriteSet(self, noLocal):
        directories = os.listdir("Sprites/Sprites")

        for d in directories:

            print(d)
            
            s = Sprites()
            
            #Generation des infantries
            s.generateSprites(32,32,96,128,"Config/AttributeInfantryUnits.cfg", d, 1)
            #Generation des vehicules
            s.generateSprites(64,64,192,256,"Config/AttributeVehicules.cfg", d, 1)

            #Si on est au directory du joueur local, il faut creer une autre version des sprites pour la selection
            if(directories.index(d) == noLocal):
                ss = Sprites()


                #Generation des infantries
                ss.generateSprites(32,32,96,128,"Config/AttributeInfantryUnits.cfg", d, 3)
                #Generation des vehicules
                ss.generateSprites(64,64,192,256,"Config/AttributeVehicules.cfg", d, 3)

                self.sprites.append((s, ss))
                

                
            else:
                self.sprites.append(s)

        print(self.sprites)  
            
        
        

    #Affiche les informations sur l'unité
    def displayInfoUnit(self, unit):
        pass

    #Affiche les ressources
    def displayRessources(self, food, metal, power):
        pass

    def displaySelection(self, initialClick, event):
        self.surfaceJeu.delete("selection")
        self.surfaceJeu.create_rectangle(initialClick[0], initialClick[1], event.x+self.surfaceJeu.canvasx(0), event.y+self.surfaceJeu.canvasy(0), outline='blue', tags="selection")
        
    def eraseSelection(self):
        self.surfaceJeu.delete("selection")
        
    #Affiche la map
    def displayMap(self, mapObj):

        self.miniMapImage = Image.new('RGB', (len(mapObj.map[0])*64,len(mapObj.map)*64))
        
        #Pour chaque ligne
        for y in range(0, len(mapObj.map)):

            #Pour chaque colone
            for x in range(0, len(mapObj.map[0])):

                temp = self.tileset.tileset[int(mapObj.map[y][x])].img
                self.miniMapImage.paste(temp, (x*64, y*64))

                self.surfaceJeu.create_image(x*64,y*64,anchor=NW, image=self.tileset.tileset[int(mapObj.map[y][x])].pImg, tags="tile")

        self.miniMapImage = self.miniMapImage.resize((self.miniMapW,self.miniMapH), Image.BILINEAR)
        self.miniMapImage = ImageTk.PhotoImage(self.miniMapImage)

        self.displayMiniMap()
        self.updateMiniMap()

        #self.surfaceJeu.create_image(0,0, anchor=NW, image=self.sprites.spriteDict['trooper']['front']['1'])

    #Affichage des objets sur la surface                                                                                                 
    def displayObject(self, joueurs, artefacts, noLocal, selection):
        
        self.surfaceJeu.delete("unit","structure","artefact")

        #Affichage des artefacts
        for a in artefacts:
            #self.surfaceJeu.create_image(a.position[0], a.position[1], anchor=NW, image=, tags="artefact")
            self.surfaceJeu.create_oval(b.position[0],b.position[1], b.position[0]+b.size, b.position[1]+b.size, fill='red', tags="artefact")

        #Iteration sur chacun des joueurs
        for joueur in joueurs:
                   
            #Affiche les unités
            for u in joueur.listeUnite:

                #Si l'unite est au joueur local
                if(joueur.noJoueur == noLocal):

                    #Si l'unite est selectionnee
                    if(u in selection):
                        self.surfaceJeu.create_image(u.position[0]-u.size/2, u.position[1]-u.size/2, anchor=NW, image=self.sprites[joueur.noJoueur][1].spriteDict[u.name][u.orientation]['1'], tags="unit")
                    #Si l'unite n'est pas selectionnee
                    else:
                        self.surfaceJeu.create_image(u.position[0]-u.size/2, u.position[1]-u.size/2, anchor=NW, image=self.sprites[joueur.noJoueur][0].spriteDict[u.name][u.orientation]['1'], tags="unit")

                #Sinon si l'unite est a un autre joueur
                else:
                    self.surfaceJeu.create_image(u.position[0]-u.size/2, u.position[1]-u.size/2, anchor=NW, image=self.sprites[joueur.noJoueur].spriteDict[u.name][u.orientation]['1'], tags="unit")

            #Affiche les batiments
            for b in joueur.listeBatiment:
                #self.surfaceJeu.create_image(i.position[0],anchor=NW,image =i.position[1],name = sprites[i.name],tags="structure")
                self.surfaceJeu.create_rectangle(b.position[0]-b.size/2,b.position[1]-b.size/2, b.position[0]+b.size/2, b.position[1]+b.size/2, fill='blue', tags="structure")
    
        
        
              
    #Affiche le HUD
    def displayHUD(self):
        self.hud.create_image(0,0,anchor=NW,image=self.photoImageHUD, tags="hud")
        self.hud.place(x=0, y=550)

    #Affiche la minimap a la bonne position
    def displayMiniMap(self):      
        self.miniMap.place(x=928, y=600)
        self.miniMap.create_image(0,0, anchor=NW, image=self.miniMapImage, tags="miniMapImage")

    #Update la camera sur la minimap et aussi l'affichage des unites
    def updateMiniMap(self):
        self.miniMap.delete("region")

        #Conversion des positions
        posx = math.floor(self.surfaceJeu.canvasx(0)*self.miniMapW/(len(self.parent.modele.map.map[0])*64))
        posy = math.floor(self.surfaceJeu.canvasy(0)*self.miniMapH/(len(self.parent.modele.map.map)*64))
        
        self.miniMap.create_rectangle(posx, posy, posx + self.relativeW, posy + self.relativeH, outline='red', tags="region")
    
    
