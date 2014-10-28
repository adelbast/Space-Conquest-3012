from Tile.Map import Map
from Class.Joueur import Joueur
from Class.AI import AI
from Class.Structure import Batiment
import configparser
import math


class Modele(object):
    def __init__(self):
        self.host = False
        self.listeJoueur = []
        self.noJoueurLocal = None
        self.maxUnite = 20  #???
        self.selection = []
        self.listeArtefact = []
        self.dictUnit = {}
        self.dictBatiment = {}
        self.createDict()
        
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

        self.cells = []
        self.mapWidth = self.map.numRow*64
        self.mapHeight = self.map.numCol*64
        self.init_grid_Pathfinding()

    def init_grid_Pathfinding(self): # test avec init sur map ( pas encore Tileset)
        for y in range(self.map.numCol):
            for x in range(self.map.numRow):
                if self.map.map[x][y] == "4":
                    walkable = False
                    flyable = False
                elif self.map.map[x][y] == "0":
                    walkable = True
                    flyable = True
                self.cells.append(self.Cell(x, y, walkable,flyable))

    
    def initPartie(self,noJoueur,listeNomJoueur,host=False):
        self.noJoueurLocal = noJoueur
        for nomJoueur in listeNomJoueur:
            if(nomJoueur == "AI"):
                self.listeJoueur.append(AI(len(self.listeJoueur)))
            else:
                self.listeJoueur.append(Joueur(self,nomJoueur,len(self.listeJoueur)))
        self.host = host
        print("Nom du joueur local : " + self.listeJoueur[self.noJoueurLocal].nom + ", numero : " + str(self.noJoueurLocal))
        self.listeJoueur[0].creerBatiment((100,100),True,"guardTower",self.dictBatiment["guardTower"])
        self.listeJoueur[0].creerBatiment((300,400),True,"HQ",self.dictBatiment["HQ"])
        #self.listeJoueur[self.noJoueurLocal].creerUnite("worker", (200,100), self.dictUnit["worker"])   #nom,position, attributs
        self.listeJoueur[0].creerUnite("worker", (100,300), self.dictUnit["worker"])
        if(len(self.listeJoueur) > 1):
            self.listeJoueur[1].creerBatiment((800,800),True,"guardTower",self.dictBatiment["guardTower"])
            self.listeJoueur[1].creerBatiment((600,800),True,"HQ",self.dictBatiment["HQ"])
            #self.listeJoueur[self.noJoueurLocal].creerUnite("worker", (600,600), self.dictUnit["worker"])  #nom,position, attributs
            self.listeJoueur[1].creerUnite("worker", (600,600), self.dictUnit["worker"])
        if(len(self.listeJoueur) > 2):
            self.listeJoueur[2].creerBatiment((800,800),True,"guardTower",self.dictBatiment["guardTower"])
            self.listeJoueur[2].creerBatiment((600,800),True,"HQ",self.dictBatiment["HQ"])
            #self.listeJoueur[self.noJoueurLocal].creerUnite("worker", (600,600), self.dictUnit["worker"])  #nom,position, attributs
            self.listeJoueur[2].creerUnite("worker", (600,600), self.dictUnit["worker"])
        if(len(self.listeJoueur) > 3):
            self.listeJoueur[3].creerBatiment((800,800),True,"guardTower",self.dictBatiment["guardTower"])
            self.listeJoueur[3].creerBatiment((600,800),True,"HQ",self.dictBatiment["HQ"])
            #self.listeJoueur[self.noJoueurLocal].creerUnite("worker", (600,600), self.dictUnit["worker"])  #nom,position, attributs
            self.listeJoueur[3].creerUnite("worker", (600,600), self.dictUnit["worker"])
        if(len(self.listeJoueur) > 4):
            self.listeJoueur[4].creerBatiment((800,800),True,"guardTower",self.dictBatiment["guardTower"])
            self.listeJoueur[4].creerBatiment((600,800),True,"HQ",self.dictBatiment["HQ"])
            #self.listeJoueur[self.noJoueurLocal].creerUnite("worker", (600,600), self.dictUnit["worker"])  #nom,position, attributs
            self.listeJoueur[4].creerUnite("worker", (600,600), self.dictUnit["worker"])
        if(len(self.listeJoueur) > 5):
            self.listeJoueur[5].creerBatiment((800,800),True,"guardTower",self.dictBatiment["guardTower"])
            self.listeJoueur[5].creerBatiment((600,800),True,"HQ",self.dictBatiment["HQ"])
            #self.listeJoueur[self.noJoueurLocal].creerUnite("worker", (600,600), self.dictUnit["worker"])  #nom,position, attributs
            self.listeJoueur[5].creerUnite("worker", (600,600), self.dictUnit["worker"])

    def gestion(self,dicActionFromServer):
        self.listeJoueur[self.noJoueurLocal].compterRessource()
        ii = 0
        for dic in dicActionFromServer:
            if(dic):
                for clee, listValeur in dic.items():
                    
                    if(clee == "Deplacement"):
                        for valeur in listValeur:
                            noUnit, cibleX, cibleY = valeur
                            print("NbUnit =",len(self.listeJoueur[ii].listeUnite),"NoUnit =", noUnit)
                            self.listeJoueur[ii].listeUnite[noUnit].setDestination( unePosition = [cibleX,cibleY])
                            
                    elif(clee == "DeplacementCible"):
                        #noUnit, noProprio, UvB, noUnitCible
                        for valeur in listValeur:
                            noUnit, noProprio, uvB, noUnitCible = valeur
                            if uvB == 0:
                                self.listeJoueur[ii].listeUnite[ noUnit ].setDestination( unit = self.listeJoueur[ noProprio ].listeUnite[ noUnitCible ])
                            else:
                                self.listeJoueur[ii].listeUnite[ noUnit ].setDestination( batiment = self.listeJoueur[ noProprio ].listeBatiment[ noUnitCible ])
                    
                    elif(clee == "RechercheAge"):
                        for valeur in listValeur:
                            age = valeur

                            self.listeJoueur[ii].ageRendu = age

                        
                    elif(clee == "NewUnit"):
                        for valeur in listValeur:
                            typeUnit, noDuBatimentSpawner = valeur
                            print(self.listeJoueur,ii)
                            print(self.listeJoueur[ii].listeBatiment)
                            self.listeJoueur[ii].creerUnite(typeUnit, self.listeJoueur[ii].listeBatiment[0].position, self.dictUnit[typeUnit]) #nom, position, attributs
                        
                    elif(clee == "NewBatiment"):
                        workerID = 0#TODO
                        typeBatiment, x, y = listValeur
                        self.listeJoueur[ii].creerBatiment((x,y), self.listeJoueur[ii].listeUnite[workerID], typeBatiment, self.dictBatiment[typeBatiment]) #position,worker,nom,attributs
                        
                    elif(clee == "SuppressionBatiment"):
                        for valeur in listValeur:
                            noBatiment = valeur

                            self.listeJoueur[ii].supprimerBatiment[noBatiment]

                        
                        
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
            ii+=1


        

    def ajoutAction(self,clee,tup):
        self.dicAction2Server[clee] = tup




    def actualiser(self): #Appelle les fonctions de game loop du modele
        self.gestionAuto()
        self.incrementerRessource()

        
    def incrementerRessource(self):
        self.listeJoueur[self.noJoueurLocal].compterRessource() #Incremente les ressources du joueur local
            
        
    def gestionAuto(self):
        for joueur in self.listeJoueur:
            for uni in joueur.listeUnite :
                if(uni.actualHP > 0):
                    uni.autoGestion(joueur.listeAllie)#Fait bouger toutes les unitées
                else:
                    del uni
            try:
                joueur.faireQqch() # AI
            except:
                pass


    def gererMouseRelease(self,event,etat):
        if(event.num == 3): #clic droit
            print(self.cells[int(self.releasePosx/64) * self.map.numRow + int(self.releasePosy/64)].walkable,
                self.cells[int(self.releasePosx/64) * self.map.numRow + int(self.releasePosy/64)].x,
                self.cells[int(self.releasePosx/64) * self.map.numRow + int(self.releasePosy/64)].y)

            if(self.selection): #Si le joueur a quelque chose de sélectionné, sinon inutile
                if(self.selection[0].owner == self.noJoueurLocal):
                    try:            #Duck typing
                        self.selection[0].setDestination(None)
                    except Exception as e:#c'est donc un batiment
                        print("impossible de bouger cette entitée")
                    else:#si pas d'exception

                        cible = self.clickCibleOuTile(self.releasePosx,self.releasePosy)
                        if(not cible):
                            cible = (self.releasePosx,self.releasePosy)
                        
                        for unite in self.selection: #Donne un ordre de déplacement à la sélection
                            
                            print("Ordre de déplacement")
                            
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
            if(etat==True):
                #self.listeJoueur[self.noJoueurLocal].creerBatiment([self.releasePosx,self.releasePosy],True,"HQ",self.dictBatiment["HQ"]) # pas bon, event.x,y doit etre changer pour map width et height 
                self.dicAction2Server['NewBatiment']=("HQ",self.releasePosx,self.releasePosy) #packetage de creation batiment
            self.selection[:] = []
            if(self.clickPosx!=self.releasePosx or self.clickPosy!=self.releasePosy):   #self.clickPosx+5 < self.releasePosx or self.clickPosx-5 > self.releasePosx or self.clickPosy+5 < self.releasePosy or self.clickPosy-5 > self.releasePosy
                print(self.clickPosx,self.clickPosy,self.releasePosx,self.releasePosy)
                for unit in self.listeJoueur[self.noJoueurLocal].listeUnite:            #Je prends seulement les unites puisque selection multiple de batiment inutile
                    if(self.pointDansForme([self.releasePosx,self.clickPosx,self.clickPosx,self.releasePosx],[self.clickPosy,self.clickPosy,self.releasePosy,self.releasePosy],unit.position[0],unit.position[1])):#La fonction dont je t'ai parlé sur ts frank...
                        self.selection.append(unit)
                        print(unit.name)
                    else:
                        print("Pas cible")
            else:
                cible = self.clickCibleOuTile(self.releasePosx,self.releasePosy)
                if(cible):
                    self.selection.append(cible)
                    print(cible.name)
                else:
                    print("Pas cible")
            
                
    def clickCibleOuTile(self,x,y): #retourne None pour un tile et la cible pour une cible
    #fonction qui regarde si le clic est sur un batiment ou une unité
        for joueur in self.listeJoueur:
            liste = joueur.listeUnite+joueur.listeBatiment
            for chose in liste:
                if(x < chose.position[0]+chose.size/2):#
                    if(x > chose.position[0]-chose.size/2):#
                        if(y < chose.position[1]+chose.size/2):#
                            if(y > chose.position[1]-chose.size/2):#
                                return chose
        else: return None


    def joueurPasMort(self,joueur):
        if(joueur.listeBatiment):
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
        
        unit = parser.sections()
        unitVe = parserVehicule.sections()
        batiments = parserBatiment.sections()

        for name in unit:
            self.type        = parser.get(name, 'type')
            self.maxHp       = int(parser.get(name, 'hp'))
            self.cost        = [int(parser.get(name,'costFood')), int(parser.get(name,'costMetal')), int(parser.get(name,'costPower'))]
            self.force       = int(parser.get(name,'force'))
            self.vitesse     = int(parser.get(name, 'vitesse'))
            self.rangeVision = int(parser.get(name, 'rangeVision'))
            self.rangeAtt    = int(parser.get(name, 'rangeAtt'))
            self.size        = int(parser.get(name, 'size'))
            self.dictUnit[name] = [self.type, self.maxHp, self.cost, self.force, self.vitesse, self.rangeVision, self.rangeAtt,self.size]

        for name in unitVe:
            self.type        = parserVehicule.get(name, 'type')
            self.maxHp       = int(parserVehicule.get(name, 'hp'))
            self.cost        = [int(parserVehicule.get(name,'costFood')), int(parserVehicule.get(name,'costMetal')), int(parserVehicule.get(name,'costPower'))]
            self.force       = int(parserVehicule.get(name,'force'))
            self.vitesse     = int(parserVehicule.get(name, 'vitesse'))
            self.rangeVision = int(parserVehicule.get(name, 'rangeVision'))
            self.rangeAtt    = int(parserVehicule.get(name, 'rangeAtt'))
            self.size        = int(parserVehicule.get(name, 'size'))
            self.dictUnit[name] = [self.type, self.maxHp, self.cost, self.force, self.vitesse, self.rangeVision, self.rangeAtt,self.size]
        
        for name in batiments:
            self.maxHp       = int(parserBatiment.get(name, 'hp'))
            self.cost        = [int(parserBatiment.get(name,'costFood')), int(parserBatiment.get(name,'costMetal')), int(parserBatiment.get(name,'costPower'))]
            self.production  = int(parserBatiment.get(name, 'production'))
            self.size        = int(parserBatiment.get(name, 'size'))
            self.canBuild	 = [parserBatiment.get(name, 'canBuild')]
            self.dictBatiment[name] = [self.maxHp, self.cost, self.production, self.size, self.canBuild]

    def getAIcount(self):
        retour = 0
        for joueur in self.listeJoueur:
            if(isinstance(joueur,AI)):
                retour+=1
        return retour


    class Cell(object):
        def __init__(self,x,y,walkable,flyable):

            self.walkable = walkable
            self.x = x
            self.y = y
            self.parent = None
            self.g = 0
            self.h = 0
            self.f = 0

        def __lt__(self, other):
            """ necessaire dans python 3.X dans le cas au on doit passer par des objets avant de comparer leur valeur
            le heapq va donc venir voir ici pour determiner la valeur a passer en premier, dans ce cas ci cest les f de chaque cell """
            return self.f < other.f

        

        
