from Tile.Map import Map
from Class.Joueur import Joueur
from Class.AI import AI
import configparser


class Modele(object):
    def __init__(self):
        self.host = False
        self.listeJoueur = []
        self.noJoueurLocal = None
        self.maxUnite = 20  #???
        self.selection = []
        self.listeArtefact = []
        self.dictUnit = {}
        self.dicBatiment = {}
        self.createDict()
        
        self.map = Map("Tile/map1.csv")

        self.dicAction2Server = {}
        self.dicActionFromServer = [{#joueur1
                                    "Deplacement":     (0, 500,500),#(noUnit, cibleX, cibleY)
                                    "DeplacementCible":(1, 2, 1, 0),#(noUnit, noProprio, 0:unité/1:batiment , noUnitCible)
                                    "RechercheAge": 1,          #si changement d'âge
                                    "NewUnit":      (0,0),      #(type d'unité, noDuBatimentSpawner)
                                    "NewBatiment":    (2,200,200),#(typeBatiment, posX, posY)
                                    "SuppressionBatiment":1,    #noBatiment
                                    "SuppressionUnit":2,        #noUnit
                                    "CaptureArtefact":0,        #noArtefact
                                    "PerteArtefact":1},
                                    
                                    {#joueur2

                                    },
                                    {},#joueur3
                                    {}]#joueur4...
        # facilite la gestion de la souris
        self.clickPosx = 0
        self.clickPosy = 0
        self.releasePosx = 0
        self.releasePosy = 0
    
    def initPartie(self,noJoueur,listeNomJoueur,host=False):
        print(listeNomJoueur)
        self.noJoueurLocal = noJoueur
        for nomJoueur in listeNomJoueur:
            if(nomJoueur == "AI"):
                self.listeJoueur.append(AI(len(self.listeJoueur)))
            else:
                self.listeJoueur.append(Joueur(nomJoueur,len(self.listeJoueur)))
        self.host = host

        print("Joueur:", self.noJoueurLocal)
        print(self.listeJoueur)
        self.listeJoueur[self.noJoueurLocal].creerBatiment((400,400),True,"wall",self.dicBatiment["wall"])
        self.listeJoueur[self.noJoueurLocal].creerUnite("worker", (100,100), self.dictUnit["trooper"])



    def gestion(self,dicActionFromServer):
        self.listeJoueur[self.noJoueurLocal].compterRessource()
        ii = 0
        for dic in dicActionFromServer:
            if(dic):
                if(ii != noJoueurLocal):
                    if(self.joueurPasMort(self.listeJoueur[ii])):
                        for clee, valeur in d.items():
                            if(clee == "Deplacement"):
                                
                                for i in valeur:            #i[0] = noUnit i[1] i [2] xy
                                    self.listeJoueur[ii].listeUnite[i[0]].setDestination((i[1],i[2]))
                                    
                            elif(clee == "DeplacementCible"):
                                #noUnit, noProprio, UvB, noUnitCible

                                for i in valeur:
                                    if i[2] == 0:
                                        self.listeJoueur[ii].listeUnite[i[0]].setDestination(self.listeJoueur[1].listeUnite[3])
                                    else:
                                        self.listeJoueur[ii].listeUnite[i[0]].setDestination(self.listeJoueur[1].listeBatiment[3])
                            
                            elif(clee == "RechercheAge"):
                                age = valeur

                                self.listeJoueur[ii].ageRendu = age

                                
                            elif(clee == "NewUnit"):
                                
                                typeUnit, noDuBatimentSpawner = valeur

                                self.listeJoueur[ii].creerUnit(typeUnit, self.listeJoueur[ii].listeBatiment[noDuBatimentSpawner].position,
                                                               self.listeJoueur[ii].listeBatiment[noDuBatimentSpawner].position)
                                
                                
                            elif(clee == "NewBatiment"):
                                typeBatiment, x, y = valeur

                                self.listeJoueur[ii].creerBatiment(typeBatiment, (x,y))

                                
                            elif(clee == "SuppressionBatiment"):
                                noBatiment = valeur

                                supprimerBatiment(self.listeJoueur[ii].listeBatiment[noBatiment])
                                
                            elif(clee == "SuppressionUnit"):
                                noUnit = valeur

                                supprimerUnite(self.listeJoueur[ii].listeBatiment[noBatiment])
                                
                            elif(clee == "CaptureArtefact"):
                                noArtefact = valeur
                            elif(clee == "PerteArtefact"):
                                noArtefact = valeur
            ii+=1


        for ind in self.listeJoueur:            #Fait bouger toutes les unitées
            for uni in ind.listeUnite :
                uni.move()


    def gererMouseRelease(self,event):
        if(event.num == 3): #clic droit
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
                            unite.setDestination(cible)
                            print("Ordre de déplacement")
            
        
        elif(event.num == 1): #clic gauche
            self.selection[:] = [] #Vide la liste
            if(self.clickPosx!=self.releasePosx or self.clickPosy!=self.releasePosy):#self.clickPosx+5 < self.releasePosx or self.clickPosx-5 > self.releasePosx or self.clickPosy+5 < self.releasePosy or self.clickPosy-5 > self.releasePosy
                print(self.clickPosx,self.clickPosy,self.releasePosx,self.releasePosy)
                for unit in self.listeJoueur[self.noJoueurLocal].listeUnite: #a changer a joueur actuel plutot que [0], je prends seulement les unites puisque selection multiple de batiment inutile
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
        joueur.compterBatiment()
        if(not joueur.nbBatiment):
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
            self.dicBatiment[name] = [self.maxHp, self.cost, self.production, self.size]

       

        

        
