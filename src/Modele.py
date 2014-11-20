from Tile.Map import Map
from Class.Joueur import Joueur
from Class.AI import AI
from Class.Structure import Batiment
from Class.Unit import *


import configparser
import math



class Modele(object):
    def __init__(self,parent):
        self.host = False
        self.parent = parent
        self.listeJoueur = []
        self.noJoueurLocal = None
        self.maxUnite = 20  #???
        self.selection = []
        self.listeArtefact = []
        self.dictUnit = {}            #dicte combiencoute chaque unit
        self.dictBatiment = {}        #dicte combiencoute chaque batiment  
        self.dictArtefact = {}
        self.dictRecherche = {} #Contient un modele de toutes les recherches
        self.createDict()
    
        
        self.idB=0
        self.map = Map("Tile/map1.csv")

        self.dicAction2Server = {}
        self.dicActionFromServer = []

        """Architecture du dictionaire se trouvant dans la liste dicActionFromServer:

        "Deplacement":      [(0, 500,500)], # (noUnit, cibleX, cibleY)
        "DeplacementCible": [(1, 2, 1, 0)], # (noUnit, noProprioCible, 0:unité/1:batiment , noUnitCible)
        "RechercheAge":     [1],            # si changement d'âge
        "NewUnit":          [(0,0)],        # (type d'unité, noDuBatimentSpawner)
        "NewBatiment":      [(HQ,3,200,200)], # (typeBatiment, workerID, posX, posY)
        "SuppressionBatiment":[1],          # noBatiment
        "SuppressionUnit":  [2],            # noUnit
        "CaptureArtefact":  [0],            # noArtefact
        "PerteArtefact":    [1]"""



        # facilite la gestion de la souris
        self.clickPosx = 0
        self.clickPosy = 0
        self.releasePosx = 0
        self.releasePosy = 0


        self.height =  self.map.numRow*2
        self.width = self.map.numCol*2
          

        self.graph = []
        self.cutNodes = []
        self.cells = []
        self.mapWidth = self.map.numRow*64
        self.mapHeight = self.map.numCol*64
        


    
    def initPartie(self,noJoueur,listeNomJoueur,host=False):
        self.noJoueurLocal = noJoueur
        for nomJoueur in listeNomJoueur:
            if(nomJoueur == "AI"):
                self.listeJoueur.append(AI(self, len(self.listeJoueur)))
            else:
                self.listeJoueur.append(Joueur(self, nomJoueur, len(self.listeJoueur)))
        self.host = host

        print("Nom du joueur local : " + self.listeJoueur[self.noJoueurLocal].nom + ", numero : " + str(self.noJoueurLocal))
        for i in range(len(self.listeJoueur)):
            positionDepartxy =[self.map.startingPoint[i][0]*64,self.map.startingPoint[i][1]*64]
            self.listeJoueur[i].listeBatiment[0] = Batiment(self.noJoueurLocal, "HQ", positionDepartxy, self.dictBatiment["HQ"], 0) #owner,name,xy,attributs,idB, initialisation = True
            self.listeJoueur[i].listeUnite[0] = Unit(self, "worker", (positionDepartxy[0]+96,positionDepartxy[1]+96), self.noJoueurLocal, self.dictUnit["worker"], 0)    #parent, name, xy, owner, attribut, idU, destination = None



    def gestion(self,dicActionFromServer):
        self.listeJoueur[self.noJoueurLocal].compterRessource()
        ii = 0
        for dic in dicActionFromServer:
            if(dic):
                for clee, listValeur in dic.items():
                    
                    if(clee == "Deplacement"):
                        for valeur in listValeur:
                            noUnit, cibleX, cibleY = valeur
                            try:
                                self.listeJoueur[ii].listeUnite[noUnit].setDestination( unePosition = (cibleX,cibleY) )
                            except KeyError as e:
                                print(e)
                                print("Déplacement a chier")
                            
                    elif(clee == "DeplacementCible"):
                        #noUnit, noProprio, UvB, noUnitCible
                        for valeur in listValeur:
                            noUnit, noProprio, uvB, noUnitCible = valeur
                            try:
                                if uvB == 0:
                                    self.listeJoueur[ii].listeUnite[ noUnit ].setDestination(listeJoueurAmi = self.listeJoueur[ii].listeAllie, unit = self.listeJoueur[ noProprio ].listeUnite[ noUnitCible ])
                                else:
                                    self.listeJoueur[ii].listeUnite[ noUnit ].setDestination(listeJoueurAmi = self.listeJoueur[ii].listeAllie, batiment = self.listeJoueur[ noProprio ].listeBatiment[ noUnitCible ])
                            except KeyError:
                                pass
                    
                    elif(clee == "RechercheAge"):
                        for valeur in listValeur:
                            age = valeur

                            self.listeJoueur[ii].ageRendu = age

                        
                    elif(clee == "NewUnit"):
                        for valeur in listValeur:
                            typeUnit, spawnPosition = valeur
                            try:
                                self.listeJoueur[ii].creerUnite(typeUnit, spawnPosition, self.dictUnit[typeUnit]) #nom, position, attributs
                            except KeyError:
                                pass
                        
                    elif(clee == "NewBatiment"):
                        for valeur in listValeur:
                            typeBatiment, workerID, x, y = valeur
                            try:
                                idNewBatiment = self.listeJoueur[ii].creerBatiment((x,y), typeBatiment, self.dictBatiment[typeBatiment]) #position,nom,attributs
                                self.listeJoueur[ii].listeUnite[workerID].setDestination(listeJoueurAmi = self.listeJoueur[ ii ].listeAllie, batiment = self.listeJoueur[ ii ].listeBatiment[ idNewBatiment ])
                            except KeyError:
                                pass

                    elif(clee == "SuppressionBatiment"):
                        for valeur in listValeur:
                            noBatiment = valeur
                            self.listeJoueur[ii].supprimerBatiment(noBatiment)
                        
                        
                    elif(clee == "SuppressionUnit"):
                        for valeur in listValeur:
                            noUnit = valeur
                            self.listeJoueur[ii].supprimerUnite(noUnit)
                        
                    elif(clee == "CaptureArtefact"):
                        for valeur in listValeur:
                            noArtefact = valeur

                            self.listeJoueur[ii].listeArtefact.append(self.listeArtefact[noArtefact])

                        
                    elif(clee == "PerteArtefact"):
                        for valeur in listValeur:
                            noArtefact = valeur

                            self.listeJoueur[ii].listeArtefact.remove(self.listeArtefact[noArtefact])
                    elif(clee == 'Recherche'):      #A tester
                        for valeur in listeValeur:
                            recherche = valeur

                            self.listeJoueur[ii].rechercher(valeur)
            ii+=1


        

    def ajoutAction(self,clee,tup):
        self.dicAction2Server[clee] = tup

    def actualiser(self): #Appelle les fonctions de game loop du modele
        self.gestionAuto()
        self.incrementerRessource()

        
    def incrementerRessource(self):
        self.listeJoueur[self.noJoueurLocal].compterRessource() #Incremente les ressources du joueur local
            
        
    def gestionAuto(self):
        #ajout suppression de batiments
        for joueur in self.listeJoueur:
            for _, uni in joueur.listeUnite.items():
                if(uni.currentHp > 0):
                    uni.autoGestion()#Fait bouger toutes les unitées
                elif(joueur.noJoueur == self.noJoueurLocal and not uni.deleteCallDone):
                    self.supprimerUnit(uni.id)
                    uni.deleteCallDone = True
            try:
                joueur.faireQqch() # AI
            except:
                pass
            for _, batiment in joueur.listeBatiment.items():
                if(batiment.currentHp < 0):
                    self.supprimerBatiment(batiment.id)


    def gererMouseRelease(self, event, etat, info):
        if(event.num == 3): #clic droit
            if(self.selection): #Si le joueur a quelque chose de sélectionné, sinon inutile
                if(self.selection[0].owner == self.noJoueurLocal):
                    try:            #Duck typing
                        self.selection[0].setDestination(None)
                    except Exception as e:#c'est donc un batiment
                        print("impossible de bouger cette entitée")
                    else:#si pas d'exception

                        cible = self.clickCibleOuTile(self.releasePosx,self.releasePosy)
                        if(not cible):#voir si ou on clique est un node couper
                            cible = (self.releasePosx,self.releasePosy)

                        if(cible):    
                            for unite in self.selection: #Donne un ordre de déplacement à la sélection
                                try:
                                    if isinstance (cible, Batiment):
                                        if 'DeplacementCible' not in self.dicAction2Server:
                                            self.dicAction2Server['DeplacementCible'] = []
                                        self.dicAction2Server['DeplacementCible'].append((unite.id, cible.owner, 1, cible.id))#(noUnit, noProprioCible, 0:unité/1:batiment , noUnitCible)
                                        #unite.setDestination(batiment = cible)
                                    else:
                                        cible.owner = cible.owner
                                        if 'DeplacementCible' not in self.dicAction2Server:
                                            self.dicAction2Server['DeplacementCible'] = []
                                        self.dicAction2Server['DeplacementCible'].append((unite.id, cible.owner, 0, cible.id))
                                        #unite.setDestination(unit = cible)
                                except:
                                    if 'Deplacement' not in self.dicAction2Server:
                                        self.dicAction2Server['Deplacement'] = []
                                    self.dicAction2Server['Deplacement'].append((unite.id, cible[0], cible[1]))
                                    #unite.setDestination(unePosition = cible)
            
        elif(event.num == 1): #clic gauche
            if(etat==True and info != None and self.selection[0].type == "builder"):
                if('NewBatiment' not in self.dicAction2Server):
                    self.dicAction2Server['NewBatiment']=[] #*La fonction gestion prend des dictionaire "contenant des listes!"
                self.dicAction2Server['NewBatiment'].append( (info, self.selection[0].id, int(self.releasePosx/32)*32, int(self.releasePosy/32)*32) ) #packetage de creation batiment ## quessé ça x/23*32?
                self.parent.etatCreation = False
                self.parent.infoCreation = None
                return
            self.selection[:] = []
            if(self.clickPosx!=self.releasePosx or self.clickPosy!=self.releasePosy):
                print(self.clickPosx,self.clickPosy,self.releasePosx,self.releasePosy)
                for _, unit in self.listeJoueur[self.noJoueurLocal].listeUnite.items(): #Je prends seulement les unites puisque selection multiple de batiment inutile
                    if(self.pointDansForme([self.releasePosx,self.clickPosx,self.clickPosx,self.releasePosx],[self.clickPosy,self.clickPosy,self.releasePosy,self.releasePosy],unit.position[0],unit.position[1])):#La fonction dont je t'ai parlé sur ts frank...
                        self.selection.append(unit)
                        print(unit.name)
                    else:
                        pass#print("Pas cible")
            else:
                cible = self.clickCibleOuTile(self.releasePosx,self.releasePosy)
                if(cible):
                    self.selection.append(cible)
                    print(cible.name)
                else:
                    pass#print("Pas cible")
            
                
    def clickCibleOuTile(self,x,y): #retourne None pour un tile et la cible pour une cible
    #fonction qui regarde si le clic est sur un batiment ou une unité
        for joueur in self.listeJoueur:
            for _, chose in joueur.listeUnite.items():
                if(x < chose.positionFluide[0]+chose.size):
                    if(x > chose.positionFluide[0]):
                        if(y < chose.positionFluide[1]+chose.size):
                            if(y > chose.positionFluide[1]):
                                return chose
            for _, chose in joueur.listeBatiment.items():
                if(x < chose.position[0]+chose.size/2):
                    if(x > chose.position[0]-chose.size/2):
                        if(y < chose.position[1]+chose.size/2):
                            if(y > chose.position[1]-chose.size/2):
                                return chose
        return None


    def joueurPasMort(self,joueur):   #Retourne si un joueur est mort ou non
        if(not joueur.listeBatiment):
            print(joueur.nom+" est mort")   
            return False
        return True

    def pointDansForme(self, listePointX, listePointY, x, y):
        nbCoin = len(listePointX)
        i = -1
        etat = False
        while i < nbCoin-1:
            i+=1
            j = (i+1)%nbCoin
            if ((((listePointY[i]<=y) and (y<listePointY[j])) or ((listePointY[j]<=y) and (y<listePointY[i]))) and (x < (listePointX[j] - listePointX[i]) * (y - listePointY[i]) / (listePointY[j] - listePointY[i]) + listePointX[i])):
                etat = not etat
        return etat



    def createDict(self):

        parser = configparser.ConfigParser()
        parser.read('Config/AttributeInfantryUnits.cfg')
        
        parserVehicule = configparser.ConfigParser()
        parserVehicule.read('Config/AttributeVehicule.cfg')
        
        parserBatiment = configparser.ConfigParser()
        parserBatiment.read('Config/AttributeBuilding.cfg')

        parserArtefact = configparser.ConfigParser()
        parserArtefact.read('Config/AttributeArtefact.cfg')

        parserRecherche = configparser.ConfigParser()
        parserRecherche.read('Config/AttributeRecherche.cfg')
        
        
        unit = parser.sections()
        unitVe = parserVehicule.sections()
        batiments = parserBatiment.sections()
        artefacts = parserArtefact.sections()
        recherches = parserRecherche.sections()
        
        for name in unit:
            self.type        = parser.get(name, 'type')
            self.maxHp       = int(parser.get(name, 'hp'))
            self.cost        = [int(parser.get(name,'costFood')), int(parser.get(name,'costMetal')), int(parser.get(name,'costPower'))]
            self.force       = int(parser.get(name,'force'))
            self.vitesse     = int(parser.get(name, 'vitesse'))
            self.rangeVision = int(parser.get(name, 'rangeVision'))
            self.rangeAtt    = int(parser.get(name, 'rangeAtt'))
            self.size        = int(parser.get(name, 'size'))
            self.armor       = int(parser.get(name, 'armor'))
            self.vitesseAtt  = int(parser.get(name, 'vitesseAttaque'))
            try:
                self.canBuild    = parser.get(name, 'canBuild').split(",")
            except:
                self.canBuild    = []

            self.dictUnit[name] = [self.type, self.maxHp, self.cost, self.force, self.vitesse, self.rangeVision, self.rangeAtt,self.size, self.canBuild, self.armor, self.vitesseAtt]

        for name in unitVe:
            self.type        = parserVehicule.get(name, 'type')
            self.maxHp       = int(parserVehicule.get(name, 'hp'))
            self.cost        = [int(parserVehicule.get(name,'costFood')), int(parserVehicule.get(name,'costMetal')), int(parserVehicule.get(name,'costPower'))]
            self.force       = int(parserVehicule.get(name,'force'))
            self.vitesse     = int(parserVehicule.get(name, 'vitesse'))
            self.rangeVision = int(parserVehicule.get(name, 'rangeVision'))
            self.rangeAtt    = int(parserVehicule.get(name, 'rangeAtt'))
            self.size        = int(parserVehicule.get(name, 'size'))
            self.armor       = int(parserVehicule.get(name, 'armor'))
            self.vitesseAtt  = int(parserVehicule.get(name, 'vitesseAttaque'))
            try:
                self.canBuild    = parserBatiment.get(name, 'canBuild').split(",")
            except:
                self.canBuild    = []
                
            self.dictUnit[name] = [self.type, self.maxHp, self.cost, self.force, self.vitesse, self.rangeVision, self.rangeAtt,self.size, self.canBuild, self.armor, self.vitesseAtt]
        
        for name in batiments:
            self.maxHp       = int(parserBatiment.get(name, 'hp'))
            self.cost        = [int(parserBatiment.get(name,'costFood')), int(parserBatiment.get(name,'costMetal')), int(parserBatiment.get(name,'costPower'))]
            self.production  = int(parserBatiment.get(name, 'production'))
            self.size        = int(parserBatiment.get(name, 'size'))
            
            try:
                self.canBuild    = parserBatiment.get(name, 'canBuild').split(",")
            except:
                self.canBuild    = []
                
            self.dictBatiment[name] = [self.maxHp, self.cost, self.production, self.size, self.canBuild]

        for name in artefacts:
            self.positionX      = int (parserArtefact.get(name,'positionX'))
            self.positionY      = int (parserArtefact.get(name,'positionY'))
            self.size           = int (parserArtefact.get(name, 'size'))
            self.bonus          = float (parserArtefact.get(name, 'bonus'))

            self.type           = str(parserArtefact.get(name, 'type'))
            self.attribute      = str (parserArtefact.get(name,'attribute'))
            
            self.dictArtefact[name] = [self.positionX,self.positionX, self.size,self.bonus, self.type, self.attribute]

        for name in recherches:
            self.type       = str (parserRecherche.get(name,'type'))
            self.attribute  = str (parserRecherche.get(name,'attribute'))
            self.bonus      = float (parserRecherche.get(name, 'bonus'))
            self.cost       = [int(parserRecherche.get(name,'costFood')), int(parserRecherche.get(name,'costMetal')), int(parserRecherche.get(name,'costPower'))]
            self.req        = int (parserRecherche.get(name, 'req'))
            self.dictRecherche[name] = [self.type, self.attribute, self.bonus, self.cost, self.req]
            
    def getAIcount(self):
        retour = 0
        for joueur in self.listeJoueur:
            if(isinstance(joueur,AI)):
                retour+=1
        return retour

    def supprimerBatiment (self,idBatiment):
        if 'SuppressionBatiment' not in self.dicAction2Server:
            self.dicAction2Server['SuppressionBatiment'] = []
        self.dicAction2Server['SuppressionBatiment'].append(idBatiment)

    def supprimerUnit (self,idUnite):
        if 'SuppressionUnit' not in self.dicAction2Server:
            self.dicAction2Server['SuppressionUnit'] = []
        self.dicAction2Server["SuppressionUnit"].append(idUnite)

    def rechercher (self,recherche):  #Passe une string (le nom de la recherche
        if 'Rechercher' not in self.dicAction2Server:
            self.dicAction2Server['Rechercher'] = []
        self.dicAction2Server["Rechercher"].append((recherche,))
            
    def changerAge (self):
        self.dicAction2Server["RechercheAge"]+= 1

    def capturerArtefact(self,noArtefact):
        self.dicAction2Serveur["captureArtefact"].append(noArtefact)

    def perteArtefact(self,noArtefact):
        self.dicAction2Serveur["PerteArtefact"].append(noArtefact)

########################################################################################
    def init_grid_Pathfinding(self,parent): #Initialise le graphe
        for x in range(self.map.numCol*2):
            for y in range(self.map.numRow*2):
                self.graph.append(Node(x,y,self))    #Cree des nodes
                
        print("row and col")
        print(self.map.numCol, self.map.numRow)
                    
        for y in range(self.map.numCol):
            for x in range(self.map.numRow):
                if parent.vue.tileset.tileset[(int)(self.map.map[x][y])].isWalkable is False:   #Coupe les nodes des tiles qui ne sont pas walkable
                    print("Nodes Cutting")
                    print(x, y)
                    self.cutNode(self.getNode(y*2,x*2))
                    self.cutNode(self.getNode(y*2+1,x*2))
                    self.cutNode(self.getNode(y*2,x*2+1))
                    self.cutNode(self.getNode(y*2+1,x*2+1))

        self.cutNode(self.getNode(0,0))            
        #print("Cut Nodes")
        #print(len(self.cutNodes))           
      
    def getNode(self, x, y):  #Retourne un node au x y donnee du graphe
        return self.graph[x*self.height+y]
    
    def reattachNode(self,x,y): # juste passer un node a la place de x,y (encore en tests)
        print("dans recreateNode")
        try:
            self.cutNodes.remove(self.getNode(x,y))
        except ValueError as e:
            print("erreur dans dans cutNodes")
        nodeAjouter = self.getNode(x,y)
        nodeAjouter.voisins = []
        nodeAjouter.defineNeighbors()  ##Si on appelle defineNeighbors on risque de refaire des liens non existant -> voir la fonction relink
        # on a attacher le node a ses voisins, maintenant doit attacher les voisins au node si ils ne sont pas dans cutNodes
        if(self.getNode(x+1,y).voisins):
            self.getNode(x+1,y).voisins[2] = [nodeAjouter.x,nodeAjouter.y]
        
        if(self.getNode(x+1,y-1).voisins):
            self.getNode(x+1,y-1).voisins[5] = [nodeAjouter.x,nodeAjouter.y]
        
        if(self.getNode(x,y-1).voisins):
            self.getNode(x,y-1).voisins[1] = [nodeAjouter.x,nodeAjouter.y]
        
        if(self.getNode(x-1,y-1).voisins):
            self.getNode(x-1,y-1).voisins[4] = [nodeAjouter.x,nodeAjouter.y]
        
        if(self.getNode(x-1,y).voisins):
            self.getNode(x-1,y).voisins[0] = [nodeAjouter.x,nodeAjouter.y]
        
        if(self.getNode(x-1,y+1).voisins):
            self.getNode(x-1,y+1).voisins[7] = [nodeAjouter.x,nodeAjouter.y]
        
        if(self.getNode(x,y+1).voisins):
            self.getNode(x,y+1).voisins[3] = [nodeAjouter.x,nodeAjouter.y]
        
        if(self.getNode(x+1,y+1).voisins):
            self.getNode(x+1,y+1).voisins[6] = [nodeAjouter.x,nodeAjouter.y]



    def cutNode(self, node):            #Coupe un node pour qu'il devienne un obstacle
        x = 0
        if isinstance(node.voisins, list) :
            try:
                if isinstance(self.getNode(node.voisins[0][0], node.voisins[0][1]).voisins, list):
                   self.getNode(node.voisins[0][0], node.voisins[0][1]).voisins[2] = [0,0]
                   x+=1
            except:
                print("INDEX ERROR")
            if isinstance(self.getNode(node.voisins[1][0], node.voisins[1][1]).voisins, list):
                self.getNode(node.voisins[1][0], node.voisins[1][1]).voisins[3] = [0,0]
                x+=1
            if isinstance(self.getNode(node.voisins[2][0], node.voisins[2][1]).voisins, list):
                self.getNode(node.voisins[2][0], node.voisins[2][1]).voisins[0] = [0,0]
                x+=1
            if isinstance(self.getNode(node.voisins[3][0], node.voisins[3][1]).voisins, list):
                self.getNode(node.voisins[3][0], node.voisins[3][1]).voisins[1] = [0,0]
                x+=1
            try:
                if isinstance(self.getNode(node.voisins[4][0], node.voisins[4][1]).voisins, list):
                   self.getNode(node.voisins[4][0], node.voisins[4][1]).voisins[6] = [0,0]
                   x+=1
            except:
                print("INDEX ERROR")
            if isinstance(self.getNode(node.voisins[5][0], node.voisins[5][1]).voisins, list):
                self.getNode(node.voisins[5][0], node.voisins[5][1]).voisins[7] = [0,0]
                x+=1
            if isinstance(self.getNode(node.voisins[6][0], node.voisins[6][1]).voisins, list):
                self.getNode(node.voisins[6][0], node.voisins[6][1]).voisins[4] = [0,0]
                x+=1
            try:
                if isinstance(self.getNode(node.voisins[7][0], node.voisins[7][1]).voisins, list):
                   self.getNode(node.voisins[7][0], node.voisins[7][1]).voisins[5] = [0,0]
            except:
                print("INDEX ERROR")

            #print("Node cut")
            #print(node.x, node.y)
            node.voisins = None
            self.cutNodes.append(node)
            
        #print("Node failed to cut")
        #print(node.x, node.y)
        

 
