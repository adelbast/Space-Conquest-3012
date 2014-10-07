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
        self.selection = None
        self.listeArtefact = []
        self.DictUnit = {{}}
        self.createListeModeleUnite()
        
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
        self.ClickPosx = 0
        self.ClickPosy = 0
        self.ReleasePosx = 0
        self.ReleasePosy = 0
    
    def initPartie(self,noJoueur,listeNomJoueur,host=False):
        self.noJoueurLocal = noJoueur
        for nomJoueur in listeNomJoueur:
            if(nomJoueur == "AI"):
                self.listeJoueur.append(AI(len(self.listeJoueur)))
            else:
                self.listeJoueur.append(Joueur(nomJoueur,len(self.listeJoueur)))
        self.host = host



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
            print("rightClick")
            if(self.selection): #Si le joueur a quelque chose de sélectionné, sinon inutile
                if(self.selection[0].owner.noJoueur == self.noJoueurLocal):
                    try:            #Duck typing
                        self.selection[0].move(None)
                    except Exception as e:#c'est donc un batiment
                        pass
                    else:#si pas d'exception
                        cible = self.clickCibleOuTile(event.x,event.y)
                        if(not cible):
                            cible = (event.x,event.y)

                        for unite in self.selection:
                            unite.move(cible)
            
        
        elif(event.num == 1): #clic gauche
            self.ReleasePosx = event.x
            self.ReleasePosy = event.y
            print("okay release fait")
            if(self.ClickPosx != self.ReleasePosx and self.ClickPosy != self.ReleasePosy):
                print("selection MULTIPLE!!!!!!!!! DRAG")
                for unit in self.listeJoueur[0].listeUnite: #a changer a joueur actuel plutot que [0], je prends seulement les unites puisque selection multiple de batiment inutile
                    if(pointDansForme([self.ReleasePosx,self.ClickPosx,self.ClickPosx,self.ReleasePosx][self.ClickPosy,self.ClickPosy,self.ReleasePosy,self.ReleasePosy],unit.position[0],unit.position[1])):#La fonction dont je t'ai parlé sur ts frank...
                        self.selection.append(unit)
                    """if (self.ClickPosx < self.ReleasePosx and self.ClickPosy < self.ReleasePosy): # on doit faire 4 different if en fonction de comment le drag a ete fait
                    # de haut Droit a Bas Gauche       de haut gauche a bas droit etc
                        if (unit.x > self.ClickPosx and unit.x < self.ReleasePosx and unit.y > self.ClickPosy and unit.y < self.ReleasePosy ): #HG a BD
                            self.selection.append(unit)
                            print("HG a BD")
                    elif (self.ClickPosx > self.ReleasePosx and self.ClickPosy > self.ReleasePosy):
                        if (unit.x < self.ClickPosx and unit.x > self.ReleasePosx and unit.y < self.ClickPosy and unit.y > self.ReleasePosy ): #BD a HG
                            self.selection.append(unit)
                            print("BD a HG")
                    elif(self.ClickPosx < self.ReleasePosx and self.ClickPosy > self.ReleasePosy):
                        if (unit.x > self.ClickPosx and unit.x < self.ReleasePosx and unit.y < self.ClickPosy and unit.y > self.ReleasePosy ): #BG a HD
                            self.selection.append(unit)
                            print("BG a HD")
                    else:
                        if (unit.x < self.ClickPosx and unit.x > self.ReleasePosx and unit.y < self.ClickPosy and unit.y > self.ReleasePosy ): #BD a HG
                            self.selection.append(unit)
                            print("BD a HG")"""


    def clickCibleOuTile(self,x,y): #retourne None pour un tile et la cible pour une cible
    #fonction qui regarde si le clic est sur un batiment ou une unité
        for joueur in self.listeJoueur:
            liste = joueur.listeUnite+joueur.listeBatiment
            for chose in liste:
                if(x < chose.position[0]+chose.size/2):
                    if(x > chose.position[0]+chose.size/2):
                        if(y < chose.position[1]+chose.size/2):
                            if(y > chose.position[1]+chose.size/2):
                                return chose
        else: return None

    def modifierSelection(self,cible):
        self.selection = cible


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



    def createDictUnit(self):

        parser = configparser.ConfigParser()
        parser.read('AttributUnits.cfg')
        parserVehicule = configparser.ConfigParser()
        parserVehicule.read('AttributeVehicule.cfg')

        unit = parser.sections()
        unitVe = parser.sections()

        for name in unit:
            self.type        = parser.get(name, 'type')
            self.maxHp       = parser.get(name, 'hp')
            self.cost        = (parser.get(name,'costFood'), parser.get(name,'costMetal'), parser.get(name,'costPower'))
            self.force       = parser.get(name,'force')
            self.vitesse     = parser.get(name, 'vitesse')
            self.rangeVision = parser.get(name, 'rangeVision')
            self.rangeAtt    = parser.get(name, 'rangeAtt')
            self.size        = parser.get(name, 'size')
            self.DictUnit.add(name)
            self.DictUnit[name] = [self.type, self.maxHp, self.cost, self.force, self.vitesse, self.rangeVision, self.rangeAtt,self.size]

        for name in unitVe:
            self.type        = parser.get(name, 'type')
            self.maxHp       = parser.get(name, 'hp')
            self.cost        = [parser.get(name,'costFood'), parser.get(name,'costMetal'), parser.get(name,'costPower')]
            self.force       = parser.get(name,'force')
            self.vitesse     = parser.get(name, 'vitesse')
            self.rangeVision = parser.get(name, 'rangeVision')
            self.rangeAtt    = parser.get(name, 'rangeAtt')
            self.size        = parser.get(name, 'size')
            self.DictUnit.add(name)
            self.DictUnit[name] = [self.type, self.maxHp, self.cost, self.force, self.vitesse, self.rangeVision, self.rangeAtt,self.size]
