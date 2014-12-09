from tkinter import *
import math
from PIL import ImageTk, Image
from Tile import Tileset
from Sprites.Sprites import Sprites
from Class.Unit import *
from Class.Structure import *
import time
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

        #THumbnails
        self.thumbnails = {}

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

        #Image pour le HUD
        self.imageHUD = Image.open("image/gui/gui.png")
        self.photoImageHUD = ImageTk.PhotoImage(self.imageHUD)
        self.boutonUP = Image.open("image/gui/boutonUP.png")
        self.photoImageBoutonUP = ImageTk.PhotoImage(self.boutonUP)
        self.cover = Image.open("image/gui/cover.png")
        self.photoImageCover = ImageTk.PhotoImage(self.cover)

        #Creation des Thumbnails
        directories = os.listdir("Image/gui/thumbnails")

        for d in directories:
            #Creation des images
            if(d != "thumbRecherche"):
                image = Image.open("image/gui/thumbnails/"+d)
                photoImage = ImageTk.PhotoImage(image)

            #Insertion des images dans un dictionnaire
            index1 = d.find("_")+1
            index2 = d.find(".")
            name = d[index1:index2]
            self.thumbnails[name] = [image, photoImage]
            print(name)

        #Pour transferer les images en PhotoImage
        for tile in self.tileset.tileset: 
            tile.pImg = ImageTk.PhotoImage(tile.img)
            
        #Initialisation de la surface de jeu
        self.hud = Canvas(self.root,height=250, width=1200,highlightthickness=0)
        self.miniMap = Canvas(self.root, width=self.miniMapW, height=self.miniMapH, bg='black', highlightthickness=0)
        self.surfaceJeu = Canvas(self.root, width=self.surfaceW, height=self.surfaceH, bg='white', highlightthickness=0)
        self.surfaceJeu.configure(scrollregion=(0,0,len(self.parent.modele.map.map[0])*64,len(self.parent.modele.map.map)*64))
        
        #Pour la fermeture de la fenetre de jeu (afin de pouvoir compléter des actions avant de quitter le programme)
        #self.root.protocol( "WM_DELETE_WINDOW", self.parent.fermeture )

        #Pour que le canvas scroll lorsquon click
        self.root.bind("<Key>", self.scroll_move)

        #Pour le click sur le hud
        self.hud.bind("<Button-1>", self.getBuildInfo)

        #Pour le click sur la map
        self.miniMap.bind("<Button-1>", self.miniMapClick)
        self.miniMap.bind("<B1-Motion>", self.miniMapClick)
        self.miniMap.bind("<Button-3>", self.parent.moveUnitWithMinimap)

        #Pour les clicks sur la surface de jeu
        self.surfaceJeu.bind("<B1-Motion>", self.parent.gererMouseDrag)
        self.surfaceJeu.bind("<Motion>",self.displayShadow)
        self.surfaceJeu.bind("<Button-1>",self.parent.gererMouseClick)
        self.surfaceJeu.bind("<ButtonRelease-1>",self.parent.gererMouseRelease)
        self.surfaceJeu.bind("<ButtonRelease-3>", self.parent.gererMouseRelease)

        #Widgets pour l'affichage de la liste de serveur/Joueur
        self.buttonJoin = Button(self.root, text="Join Server", state=DISABLED, command=self.parent.joinLobby)
        self.serverList = Listbox(self.root)
        self.buttonCreate = Button(self.root, text="Create Server", state=DISABLED, command=self.parent.createLobby)
        self.registreVerifEntry = self.root.register(self.verifEntry)
        self.entreClient = Entry(self.root)
        self.entreClient.insert(0, "Entrez votre nom")
        self.entreClient.config(validate="key", validatecommand=(self.registreVerifEntry, '%P', '%W', '%S', '%d'))
        self.entreServeur = Entry(self.root)
        self.entreServeur.insert(0, "Nom de votre serveur")
        self.entreServeur.config(validate="key", validatecommand=(self.registreVerifEntry, '%P', '%W', '%S', '%d'))
        self.entreClientOK = False
        self.entreServeurOK = False
        self.labelFrameSpinBox = LabelFrame(self.root, text="Nombre d'IA", width=50)
        self.spinBox = Spinbox(self.labelFrameSpinBox, from_=0, to=8)

        #Configuration du Grid Layout
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        
        #Widgets pour l'affichage du Lobby
        self.playerList = Listbox(self.root)
        self.buttonStart = Button(self.root, text="Start Game", command=self.parent.lancerPartie)
        

    #Deplacement de la map avec WASD
    def scroll_move(self, event):
        variation = 1
        
        if(event.char == 'w'):
            #print('up')
            self.surfaceJeu.yview('scroll', -variation, 'units')

        elif(event.char == 's'):
            #print("down")
            self.surfaceJeu.yview('scroll', variation, 'units')

        elif(event.char == 'a'):
            #print("left")
            self.surfaceJeu.xview('scroll', -variation, 'units')
            
        elif(event.char == 'd'):
            #print("right")
            self.surfaceJeu.xview('scroll', variation, 'units')

        self.updateMiniMap()

    def getSurfacePos(self):
        return (self.surfaceJeu.canvasx(0), self.surfaceJeu.canvasy(0))

    """def BindUnbindCreation(self):
        if(self.etatCreation==True):
            self.surfaceJeu.bind("<Enter>",self.dessinerShadowBatiment)
        else:
            self.surfaceJeu.unbind("<Enter>",self.dessinerShadowBatiment)"""

    #Display un rectangle a la position ou l'on veut deposer une structure
    def displayShadow(self, event):
        self.surfaceJeu.delete("shadow")
        if(self.parent.etatCreation == True):
            x = int((event.x+self.surfaceJeu.canvasx(0))/32)*32
            y = int((event.y+self.surfaceJeu.canvasy(0))/32)*32
            
            size = self.parent.getSizeBatiment(self.parent.infoCreation)[3]
            
            if(size != 32):
                self.surfaceJeu.create_rectangle(x-(size/2), y-(size/2), x+(size/2), y+(size/2), fill="red", tags="shadow")
            else:
                self.surfaceJeu.create_rectangle(x, y, x+size, y+size, fill="red", tags="shadow")


    #Deplacer la camera lorsqu'on clique sur le canvas de la minimap
    def miniMapClick(self, event):

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

        #print((posx*(len(self.parent.modele.map.map[0])*64))/self.miniMapW, (posy*(len(self.parent.modele.map.map)*64))/self.miniMapH)

        self.surfaceJeu.xview_moveto(posx*1/self.miniMapW)
        self.surfaceJeu.yview_moveto(posy*1/self.miniMapH)

    #Animation des unites
    def animateSprites(self, unit):
        
        speed = 200 #Vitesse Millisecondes
        currentTime = int(round(time.time()*1000))

        #print("Temps Courrant : ", currentTime, "Temps Dernier Frame : ", unit.lastFrameTime, "Difference : ", currentTime - unit.lastFrameTime)

        if((currentTime - unit.lastFrameTime) >= speed):
            if(unit.currentFrame == '0'):
                unit.currentFrame = '2'
            else:
                unit.currentFrame = '0'

            unit.lastFrameTime = int(round(time.time()*1000))   #Reset le last frame time

        #print("Current Frame : ", unit.currentFrame)
               
        

    #Generation des sprites pour chacun des joueurs
    def generateSpriteSet(self, noLocal):
        directories = os.listdir("Image/sprites")

        for d in directories:
            
            s = Sprites()
            
            #Generation des infantries
            s.generateSprites(32,32,96,128,"Config/AttributeInfantryUnits.cfg", d, 1)
            #Generation des vehicules
            s.generateSprites(64,64,192,256,"Config/AttributeVehicule.cfg", d, 1)
            #Generation des buildings
            s.generateBuildingSprites("Config/AttributeBuilding.cfg", d, 1)

            #Si on est au directory du joueur local, il faut creer une autre version des sprites pour la selection
            if(directories.index(d) == noLocal):
                ss = Sprites()


                #Generation des infantries
                ss.generateSprites(32,32,96,128,"Config/AttributeInfantryUnits.cfg", d, 3)
                #Generation des vehicules
                ss.generateSprites(64,64,192,256,"Config/AttributeVehicule.cfg", d, 3)
                #Generation des buildings
                ss.generateBuildingSprites("Config/AttributeBuilding.cfg", d, 3)
                
                self.sprites.append((s, ss))
                

                
            else:
                self.sprites.append(s)
            
    #Affiche les nodes du pathfinder 
    def displayNodes(self, nodes):
        self.surfaceJeu.delete("Nodes")
        size = 32
        
        for node in nodes:
            self.surfaceJeu.create_rectangle(node.x*32, node.y*32,(node.x*32)+size, (node.y*32)+size, fill="red",tags="Nodes")

    #Affiche les informations sur l'unité
    def displayInfoUnit(self, unit, noLocal):

        self.hud.delete("build")
        self.hud.delete("infos")
        self.hud.delete("button")
        self.hud.delete("thumbnail")

        offset=0

        #Affichage de l'image de l'unité
        try:
            if(unit.owner == noLocal):
                thumbnail = self.sprites[noLocal][0].spriteDict[unit.name]['front']['1']
            else:
                thumbnail = self.sprites[unit.owner].spriteDict[unit.name]['front']['1']
        except:
           thumbnail = self.sprites[unit.owner][0].spriteDict[unit.name]
        
        if(thumbnail.width() != 128):
            #print(thumbnail.width())
            offset = (128-thumbnail.width())/2

        self.hud.create_text(320, 40, anchor=NW, text=unit.name, font=("Stencil", 12), tags="infos")
            
        self.hud.create_rectangle(310, 60, 438, 188, fill='red')
        
        self.hud.create_image(310+offset,60+offset, anchor=NW, image=thumbnail, tags="infos")

        #Affichage de la barre de vie
        conversionVie = (128*unit.currentHp)/unit.maxHp
        
        self.hud.create_rectangle(310, 200, 438, 210, fill='black', tags="infos")
        self.hud.create_rectangle(310, 200, 310+conversionVie, 210, fill='green', tags="infos")

        #Afficher le bouton pour le delete
        self.hud.create_image(490, 168, anchor=NW, image=self.photoImageBoutonUP, tags=("infos", "delete"))
        self.hud.create_image(490, 168, anchor=NW, image=self.thumbnails["delete"][1], tags=("infos", "delete"))
        self.hud.create_image(490, 168, anchor=NW, image=self.photoImageCover, tags=("infos", "delete"))
        
        
        #Affichage des stats
        if isinstance (unit, Unit):
            self.hud.create_text(448, 60, anchor=NW, text="Power : "+str(unit.force), font=("Stencil", 12), tags="infos")
            self.hud.create_text(448, 85, anchor=NW, text="Range Vision : "+str(unit.rangeVision), font=("Stencil", 12), tags="infos")
            self.hud.create_text(448, 110, anchor=NW, text="Range Attack : "+str(unit.rangeAtt), font=("Stencil", 12), tags="infos")
            self.hud.create_text(448, 135, anchor=NW, text="Vitesse : "+str(unit.vitesse), font=("Stencil", 12), tags="infos")

        if isinstance (unit, Unit):#Décide de ce que construit le "unit"
            build_type = "structure"
        else:
            build_type = "unit"

        if(unit.owner == noLocal and ( build_type == "structure" or unit.estConstruit )):

            
            if(unit.name == "researchCenter"):
                build_type = "research"

                
                margin = 5
                startX = 600
                startY = 25
                size = 64
                row = 0
                column = 0

                self.hud.create_rectangle(600, 25, 881, 237, fill='black', tags="infos")

                #print("Construction", self.parent.getResearch(noLocal))

                for u in self.parent.getResearch(noLocal):

                    print(u)
                    
                    #print(u)
                    self.hud.create_image(startX+((column*size)+margin*(column+1)), startY+((row*size)+margin*(row+1)), anchor=NW, image=self.photoImageBoutonUP, tags=("button", u, build_type))

                    try:
                        self.hud.create_image(startX+((column*size)+margin*(column+1)), startY+((row*size)+margin*(row+1)), anchor=NW, image=self.thumbnails[u][1], tags=("thumbnail", u, build_type))
                    except:
                        pass

                    self.hud.create_image(startX+((column*size)+margin*(column+1)), startY+((row*size)+margin*(row+1)), anchor=NW, image=self.photoImageCover, tags=("button", u, build_type))
                    
                    if(column%3 == 0 and column != 0):
                        #print("row : ",row)
                        row +=1
                        #print("column : ", column)
                        column = 0
                    else:
                        column += 1

            #Afficher les unités qui peuvent être produites
            elif( len(unit.canBuild) > 0 ):

                margin = 5
                startX = 600
                startY = 25
                size = 64
                row = 0
                column = 0

                self.hud.create_rectangle(600, 25, 881, 237, fill='black', tags="infos")

                for u in unit.canBuild:
                
                    #print(u)
                    self.hud.create_image(startX+((column*size)+margin*(column+1)), startY+((row*size)+margin*(row+1)), anchor=NW, image=self.photoImageBoutonUP, tags=("button", u, build_type))
                    try:
                        self.hud.create_image(startX+((column*size)+margin*(column+1)), startY+((row*size)+margin*(row+1)), anchor=NW, image=self.thumbnails[u][1], tags=("thumbnail", u, build_type))
                    except:
                        pass

                    self.hud.create_image(startX+((column*size)+margin*(column+1)), startY+((row*size)+margin*(row+1)), anchor=NW, image=self.photoImageCover, tags=("button", u, build_type))
                    
                    if(column%3 == 0 and column != 0):
                        #print("row : ",row)
                        row +=1
                        #print("column : ", column)
                        column = 0
                    else:
                        column += 1
                
            else:
                self.hud.delete("button")
                self.hud.delete("thumbnail")
        
    
    #Afficher la population du joueur
    def displayPop(self, joueur):
        self.hud.delete("pop")
        pop = "Population : "+str(len(joueur.listeUnite))+"/"+str(joueur.maxPop)
        self.hud.create_text(300, 230, font=("Stencil", 12), text=pop, anchor=NW, tags="pop")
        
    #Affiche les ressources
    def displayRessources(self, ressources):
        self.hud.delete("ressources")
        self.hud.create_text(350, 0, font=("Stencil", 12), text="Food : "+str(round(ressources[0])), anchor=NW, tags="ressources")
        self.hud.create_text(550, 0, font=("Stencil", 12), text="Metal : "+str(round(ressources[1])), anchor=NW, tags="ressources")
        self.hud.create_text(750, 0, font=("Stencil", 12), text="Power : "+str(round(ressources[2])), anchor=NW, tags="ressources")

    def displaySelection(self, initialClick, event):
        self.surfaceJeu.delete("selection")
        self.surfaceJeu.create_rectangle(initialClick[0], initialClick[1], event.x+self.surfaceJeu.canvasx(0), event.y+self.surfaceJeu.canvasy(0), outline='blue', tags="selection")
        
    def eraseSelection(self):
        self.surfaceJeu.delete("selection")

    def removeGridDisplay(self):
        for child in self.root.winfo_children():
            child.grid_forget()

    def verifEntry(self, currentValue, nomWidget, changement, action):
        if(str(self.entreClient) == nomWidget and currentValue != "" and not re.search("[ ]", currentValue)):
            self.buttonJoin.config(state=NORMAL)
            self.entreClientOK = True
            if(self.entreServeurOK):
                self.buttonCreate.config(state=NORMAL)
        elif(str(self.entreClient) == nomWidget):
            self.entreClientOK = False
            self.buttonJoin.config(state=DISABLED)
            self.buttonCreate.config(state=DISABLED)

        if(self.entreClientOK and str(self.entreServeur) == nomWidget and currentValue != "" and not re.search("[ ]", currentValue) ):
            self.buttonCreate.config(state=NORMAL)
            self.entreServeurOK = True
        elif(str(self.entreServeur) == nomWidget):
            self.entreServeurOK = False
            self.buttonCreate.config(state=DISABLED)

        if(action == 1): #0:suppression, 1:ajout
            if(re.search("[ ]", currentValue)):
                return False
        return True

    #Affichage de la liste de serveur disponible
    def displayServers(self, serverList):
        #self.root.grid_propagate(0)
        self.entreClient.grid(row=0, column=0, sticky=N+S+E+W)
        self.entreServeur.grid(row=0, column=1, sticky=N+S+E+W)
        self.serverList.grid(row=1, column=0, sticky=N+S+E+W)
        self.buttonJoin.grid(row=2, column=0, sticky=N+S+E+W)
        self.buttonCreate.grid(row=2, column=1, sticky=N+S+E+W)

    def refreshServers(self, serverList):
        self.serverList.delete(0, END)

        for server in serverList:
            print(server)
            self.serverList.insert(END, server)

        
    #Affichage du Lobby avant de debuter une partie
    def displayLobby(self, isHost):
        self.playerList.grid(row=0, column=0, sticky=N+S+E+W)
        
        if(isHost):
            self.labelFrameSpinBox.grid(row=0, column=1, sticky=N+S+E+W)
            self.spinBox.grid(row=0, column=0)
            self.buttonStart.grid(row=1, column=0, sticky=N+S+E+W)

    def refreshLobby(self, listeClients):
        self.playerList.delete(0, END)
        for nom in listeClients:
            self.playerList.insert(END, nom)

        


    #Affiche la map
    def displayMap(self, mapObj):
        self.surfaceJeu.place(x=0, y=0)
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
        
        self.surfaceJeu.delete("unit","structure","artefact", "healthbars")
        self.miniMap.delete("unit", "structure")

        #Affichage des artefacts
        for a in artefacts:
            #self.surfaceJeu.create_image(a.position[0], a.position[1], anchor=NW, image=, tags="artefact")
            self.surfaceJeu.create_oval(b.position[0],b.position[1], b.position[0]+b.size, b.position[1]+b.size, fill='red', tags="artefact")

        #Iteration sur chacun des joueurs
        for joueur in joueurs:

            #Affiche les batiments
            for _, b in joueur.listeBatiment.items():# _ == placeholder pour la clée

                pX = int((b.position[0]*self.miniMapW) / (len(self.parent.modele.map.map[0])*64))
                pY = int((b.position[1]*self.miniMapH) / (len(self.parent.modele.map.map)*64))
                rSize = int(b.size*self.miniMapW / (len(self.parent.modele.map.map[0])*64))

                if((b.position[0] <= self.surfaceJeu.canvasx(0)+self.surfaceW and b.position[0] >= self.surfaceJeu.canvasx(0))and
                       (b.position[1] <= self.surfaceJeu.canvasy(0)+self.surfaceH and b.position[1] >= self.surfaceJeu.canvasy(0))):
                    

                    if(b.currentHp < b.maxHp):
                        conversionVie = (b.size*b.currentHp)/b.maxHp
                        offsetY = (b.size/2)+6
                        if(b.size != 32):
                            offsetX = b.size/2
                        else:
                            offsetX =0
                        height = 3
                
                        self.surfaceJeu.create_rectangle(b.position[0]-offsetX, (b.position[1])-offsetY, (b.position[0])+b.size-offsetX, (b.position[1])+(height-offsetY), fill="red", width=0, tags="healthbars")
                        self.surfaceJeu.create_rectangle(b.position[0]-offsetX, (b.position[1])-offsetY, (b.position[0])+conversionVie-offsetX, (b.position[1])+(height-offsetY), fill="blue", width=0, tags="healthbars")


                
                
                    #Si l'unite est au joueur local
                    if(joueur.noJoueur == noLocal):

                        #Si l'unite est selectionnee
                        if(b in selection):
                            if(b.size != 32):
                                self.surfaceJeu.create_image(b.position[0]-b.size/2, b.position[1]-b.size/2, anchor=NW, image=self.sprites[joueur.noJoueur][1].spriteDict[b.name], tags="structure")
                            else:
                                self.surfaceJeu.create_image(b.position[0], b.position[1], anchor=NW, image=self.sprites[joueur.noJoueur][1].spriteDict[b.name], tags="structure")      
                        #Si l'unite n'est pas selectionnee
                        else:
                            if(b.size != 32):
                                self.surfaceJeu.create_image(b.position[0]-b.size/2, b.position[1]-b.size/2, anchor=NW, image=self.sprites[joueur.noJoueur][0].spriteDict[b.name], tags="structure")
                            else:
                                self.surfaceJeu.create_image(b.position[0], b.position[1], anchor=NW, image=self.sprites[joueur.noJoueur][0].spriteDict[b.name], tags="structure")

                    #Sinon si l'unite est a un autre joueur
                    else:
                        self.surfaceJeu.create_image(b.position[0]-b.size/2, b.position[1]-b.size/2, anchor=NW, image=self.sprites[joueur.noJoueur].spriteDict[b.name], tags="structure")

                    if(b.currentHp < b.maxHp):
                        conversionVie = (b.size*b.currentHp)/b.maxHp
                        offsetY = (b.size/2)+6
                        if(b.size != 32):
                            offsetX = b.size/2
                        else:
                            offsetX =0
                        height = 3
                
                        self.surfaceJeu.create_rectangle(b.position[0]-offsetX, (b.position[1])-offsetY, (b.position[0])+b.size-offsetX, (b.position[1])+(height-offsetY), fill="red", width=0, tags="healthbars")
                        self.surfaceJeu.create_rectangle(b.position[0]-offsetX, (b.position[1])-offsetY, (b.position[0])+conversionVie-offsetX, (b.position[1])+(height-offsetY), fill="blue", width=0, tags="healthbars")

                #Afficher les unites sur la minimap
                if(joueur.noJoueur == noLocal):
                   self.miniMap.create_rectangle(pX, pY, pX+rSize, pY+rSize, fill="yellow", width=0, tags="structure")
                else:
                    self.miniMap.create_rectangle(pX, pY, pX+rSize, pY+rSize, fill="red", width=0, tags="structure")

                
                    
            #Affiche les unités
            for _, u in joueur.listeUnite.items():# _ == placeholder pour la clée

                pX = int((u.positionFluide[0]*self.miniMapW) / (len(self.parent.modele.map.map[0])*64))
                pY = int((u.positionFluide[1]*self.miniMapH) / (len(self.parent.modele.map.map)*64))
                rSize = int(u.size*self.miniMapW / (len(self.parent.modele.map.map[0])*64))


                if((u.position[0] <= self.surfaceJeu.canvasx(0)+self.surfaceW and u.position[0] >= self.surfaceJeu.canvasx(0))and
                       (u.position[1] <= self.surfaceJeu.canvasy(0)+self.surfaceH and u.position[1] >= self.surfaceJeu.canvasy(0))):
                
                    if(u.isWalking):
                        self.animateSprites(u)

                    #Si l'unite est au joueur local
                    if(joueur.noJoueur == noLocal):

                        #Si l'unite est selectionnee
                        if(u in selection):
                            self.surfaceJeu.create_image(u.positionFluide[0], u.positionFluide[1], anchor=NW, image=self.sprites[joueur.noJoueur][1].spriteDict[u.name][u.orientation][u.currentFrame], tags="unit")
                        #Si l'unite n'est pas selectionnee
                        else:
                            self.surfaceJeu.create_image(u.positionFluide[0], u.positionFluide[1], anchor=NW, image=self.sprites[joueur.noJoueur][0].spriteDict[u.name][u.orientation][u.currentFrame], tags="unit")

                    #Sinon si l'unite est a un autre joueur
                    else:
                        self.surfaceJeu.create_image(u.positionFluide[0], u.positionFluide[1], anchor=NW, image=self.sprites[joueur.noJoueur].spriteDict[u.name][u.orientation][u.currentFrame], tags="unit")

                    if(u.currentHp < u.maxHp):
                        conversionVie = (u.size*u.currentHp)/u.maxHp
                        offsetY = 6
                        height = 3
                
                        self.surfaceJeu.create_rectangle(u.positionFluide[0], (u.positionFluide[1])-offsetY, (u.positionFluide[0])+u.size, (u.positionFluide[1])+(height-offsetY), fill="red", width=0, tags="healthbars")
                        self.surfaceJeu.create_rectangle(u.positionFluide[0], (u.positionFluide[1])-offsetY, (u.positionFluide[0])+conversionVie, (u.positionFluide[1])+(height-offsetY), fill="blue", width=0, tags="healthbars")
                    
                    
                #Afficher les unites sur la minimap
                if(joueur.noJoueur == noLocal):
                   self.miniMap.create_rectangle(pX, pY, pX+rSize, pY+rSize, fill="yellow", width=0, tags="unit")
                else:
                    self.miniMap.create_rectangle(pX, pY, pX+rSize, pY+rSize, fill="red", width=0, tags="unit")
    
    #Get les tags des boutons appuyé sur le hud et lance les états nécéssaires au type de bouton appuyé
    def getBuildInfo(self, event):
        item = self.hud.find_closest(event.x, event.y)[0]
        #print("ID : ", item)
        #print("ThingToBuild : ", self.hud.gettags(item)[1], "Type : ", self.hud.gettags(item)[2])
        #print("Below : ", self.hud.find_below(item))
        #try:
        if(self.hud.gettags(item)[2] == "structure"):
            self.parent.etatCreation = True
            self.parent.infoCreation = self.hud.gettags(item)[1]
        elif(self.hud.gettags(item)[2] == "research"):
            print("Recherche : ", self.hud.gettags(item)[1],", dans la fonction getBuildInfo() de la Vue")
            self.parent.modele.rechercher(self.hud.gettags(item)[1])
        elif(self.hud.gettags(item)[1] == "delete"):
            print("Delete unit")
            try:
                if(isinstance(self.parent.modele.selection[0],Unit)):
                    self.parent.modele.supprimerUnit(self.parent.modele.selection[0].id)
                elif(isinstance(self.parent.modele.selection[0],Batiment)):
                    self.parent.modele.supprimerBatiment(self.parent.modele.selection[0].id)
                #On enleve tous ses boutons
                self.hud.delete("button")
                self.hud.delete("thumbnail")
                self.hud.delete("infos")
            except:
                print("rien de selectionner")
        else:
            print("Spawn")
            self.parent.spawnUnit(self.hud.gettags(item)[1])
        #except:
        #print("Aucun choix de construction selectionne")
        
        
              
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
    
    
