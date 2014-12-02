import configparser
from Class.Structure import *
from Class.Unit import Unit
from Class.Modif import Modif

class Joueur():
    def __init__(self, parent,nom,noJoueur):
        self.nom = nom
        self.parent = parent
        self.noJoueur = noJoueur
        self.listeUnite={}
        self.listeBatiment={}
        self.listeArtefact=[]
        self.listeRessource=[1000,1000,1000] #nourriture,metaux,energie

        self.maxPop=10
        self.ageRendu=1 #il y en a 3
        self.diplomatieStatus=False
        self.nbBatiment=0
        self.nbUnite=0
        self.idCountBatiment=1  #Car le zero est réservé pour le unit de départ
        self.idCountUnit=1      #" "
        self.listeAllie = [self.noJoueur]#self.noJoueur

        
##In dev
        self.currentUnits = ["greenBeret", "trooper", "halfTrack", "tank"]
        self.nbRecherches = 0
        self.availableResearch = []
    
        self.recherches = []
        self.modif = Modif()

        self.remplirRecherches() 


####################################################################Recherches
    def remplirRecherches(self):
        self.availableResearch = []
        for i in self.parent.dictRecherche:
            indx = self.parent.dictRecherche.get(i)
            if indx[4] <= self.nbRecherches:
                if i not in self.recherches :
                    if indx[5] <= self.ageRendu:
                        self.availableResearch.append(i)

    def rechercher(self,nomRecherche):
        indx = self.parent.dictRecherche.get(nomRecherche)
        if self.assezRessources(indx[3]):
            if nomRecherche not in self.recherches:
                self.recherches.append(nomRecherche)
                self.appliquerModif(indx[0], indx[1], indx[2])
                self.nbRecherches += 1 
                self.remplirRecherches()

    def appliquerModif(self, attribute1, attribute2, bonus):
        if attribute1 == "infantryBoost":
            if attribute2 == "force":
                self.modif.infantryBoost[self.modif.FORCE] += bonus
            elif attribute2 == "vitesse":
                self.modif.infantryBoost[self.modif.VITESSE] += bonus
            elif attribute2 == "armor":
                self.modif.infantryBoost[self.modif.ARMOR] += bonus

        elif attribute1 == "rangeBoost":
            if attribute2 == "force":
                self.modif.infantryBoost[self.modif.FORCE] += bonus
            elif attribute2 == "vitesse":
                self.modif.infantryBoost[self.modif.VITESSE] += bonus
            elif attribute2 == "armor":
                self.modif.infantryBoost[self.modif.ARMOR] += bonus
        
        elif attribute1 == "vehiculeBoost":
            if attribute2 == "force":
                self.modif.infantryBoost[self.modif.FORCE] += bonus
            elif attribute2 == "vitesse":
                self.modif.infantryBoost[self.modif.VITESSE] += bonus
            elif attribute2 == "armor":
                self.modif.infantryBoost[self.modif.ARMOR] += bonus

        elif attribute1 == "airBoost":
            if attribute2 == "force":
                self.modif.infantryBoost[self.modif.FORCE] += bonus
            elif attribute2 == "vitesse":
                self.modif.infantryBoost[self.modif.VITESSE] += bonus
            elif attribute2 == "armor":
                self.modif.infantryBoost[self.modif.ARMOR] += bonus

        elif attribute1 == "builderBoost":
            if attribute2 == "force":
                self.modif.builderBoost[self.modif.FORCE] += bonus
            elif attribute2 == "vitesse":
                self.modif.builderBoost[self.modif.VITESSE] += bonus
            elif attribute2 == "armor":
                self.modif.builderBoost[self.modif.ARMOR] += bonus

        elif attribute1 == "generatorProduction":
            if attribute2 == "mine":
                self.modif.generatorProduction[self.modif.MINE] += bonus
            elif attribute2 == "farm":
                self.modif.generatorProduction[self.modif.FARM] += bonus
            elif attribute2 == "solarPanel":
                self.modif.generatorProduction[self.modif.SOLARPANEL] += bonus

        elif attribute1 == "hpBoost":
            if attribute2 == "building":
                self.modif.hp[self.modif.BUILDING] += bonus
            elif attribute2 == "unit":
                self.modif.hp[self.modif.UNIT] += bonus
        
        elif attribute1 == "age_advance1":
            self.changerAge()


####################################################################


    def creerBatiment(self,position,nom,attributs):
        attributs[0] += self.modif.hp[self.modif.BUILDING]
        if nom == "farm" or nom == "mine" or nom == "solarPanel":
            self.listeBatiment[self.idCountBatiment] = Generator(self.noJoueur, nom, position, attributs, self.idCountBatiment, initialisation = False)
        else:
            self.listeBatiment[self.idCountBatiment] = Batiment(self.noJoueur, nom, position, attributs, self.idCountBatiment, initialisation = False)
        self.cutNodeBatiment(self.idCountBatiment)
        self.idCountBatiment+=1
        print("batiment cree")
        return self.idCountBatiment-1 #Ce retour sert dans gestion pour que le builder qui doit le construire connaisse le id de sa cible
    
    def positionCreationValide(self,position,attribut):
        x = int(position[0]/32)
        y = int(position[1]/32)
        valide = True

        for joueur in self.parent.listeJoueur:
            for _, unit in joueur.listeUnite.items():
                if(int(unit.position[0]/32) == x and int(unit.position[1]/32) == y):
                    valide = False
        
        if self.parent.getNode(x,y).voisins is None:
            valide = False
        
        if(valide and attribut == 64):
            if (self.parent.getNode(x-1,y-1).voisins is None 
                or self.parent.getNode(x-1,y).voisins is None
                or self.parent.getNode(x,y-1).voisins is None):
                valide = False
            if(valide):
                for joueur in self.parent.listeJoueur:
                    for _, unit in joueur.listeUnite.items():
                        if(int(unit.position[0]/32) == x and int(unit.position[1]/32) == y
                            or int(unit.position[0]/32) == x-1 and int(unit.position[1]/32) == y-1
                            or int(unit.position[0]/32) == x-1 and int(unit.position[1]/32) == y
                            or int(unit.position[0]/32) == x and int(unit.position[1]/32) == y-1 ):
                            valide = False
        
        if (valide and attribut == 128):
            
            if (self.parent.getNode(x+1,y+1).voisins is None
                or self.parent.getNode(x-2,y+1).voisins is None 
                or self.parent.getNode(x+1,y-2).voisins is None
                or self.parent.getNode(x-2,y-2).voisins is None
                or self.parent.getNode(x-2,y).voisins is None
                or self.parent.getNode(x-2,y-1).voisins is None
                or self.parent.getNode(x-1,y-2).voisins is None
                or self.parent.getNode(x,y-2).voisins is None
                or self.parent.getNode(x-2,y-2).voisins is None
                or self.parent.getNode(x+1,y).voisins is None
                or self.parent.getNode(x-2,y-2).voisins is None
                or self.parent.getNode(x+1,y-1).voisins is None
                or self.parent.getNode(x,y+1).voisins is None
                or self.parent.getNode(x-1,y+1).voisins is None):
                valide = False
            
            if(valide):
                for joueur in self.parent.listeJoueur:
                    for _, unit in joueur.listeUnite.items():
                        if(int(unit.position[0]/32) == x and int(unit.position[1]/32) == y
                            or int(unit.position[0]/32) == x-1 and int(unit.position[1]/32) == y-1
                            or int(unit.position[0]/32) == x-1 and int(unit.position[1]/32) == y
                            or int(unit.position[0]/32) == x and int(unit.position[1]/32) == y-1
                            or int(unit.position[0]/32) == x+1 and int(unit.position[1]/32) == y+1
                            or int(unit.position[0]/32) == x+1 and int(unit.position[1]/32) == y
                            or int(unit.position[0]/32) == x+1 and int(unit.position[1]/32) == y-1 
                            or int(unit.position[0]/32) == x-1 and int(unit.position[1]/32) == y
                            or int(unit.position[0]/32) == x-1 and int(unit.position[1]/32) == y+1
                            or int(unit.position[0]/32) == x and int(unit.position[1]/32) == y+1
                            or int(unit.position[0]/32) == x-2 and int(unit.position[1]/32) == y-2
                            or int(unit.position[0]/32) == x-1 and int(unit.position[1]/32) == y-2
                            or int(unit.position[0]/32) == x and int(unit.position[1]/32) == y-2
                            or int(unit.position[0]/32) == x+1 and int(unit.position[1]/32) == y-2
                            or int(unit.position[0]/32) == x-2 and int(unit.position[1]/32) == y-1
                            or int(unit.position[0]/32) == x-2 and int(unit.position[1]/32) == y
                            or int(unit.position[0]/32) == x-2 and int(unit.position[1]/32) == y+1):
                            valide = False
        
        return valide

    def cutNodeBatiment(self, idBatiment):
        grosseur = self.listeBatiment[idBatiment].size
        x = int(self.listeBatiment[idBatiment].position[0]/32)
        y = int(self.listeBatiment[idBatiment].position[1]/32)
        if(grosseur == 64):
            self.parent.cutNode(self.parent.getNode(x-1,y-1))
            self.parent.cutNode(self.parent.getNode(x-1,y))
            self.parent.cutNode(self.parent.getNode(x,y-1))
        if(grosseur == 128):
            self.parent.cutNode(self.parent.getNode(x-1,y-1))
            self.parent.cutNode(self.parent.getNode(x-1,y))
            self.parent.cutNode(self.parent.getNode(x,y-1))

            self.parent.cutNode(self.parent.getNode(x+1,y+1))
            self.parent.cutNode(self.parent.getNode(x+1,y))
            self.parent.cutNode(self.parent.getNode(x+1,y-1))
            self.parent.cutNode(self.parent.getNode(x-1,y))
            self.parent.cutNode(self.parent.getNode(x-1,y+1))
            self.parent.cutNode(self.parent.getNode(x,y+1))

            self.parent.cutNode(self.parent.getNode(x-2,y-2))
            self.parent.cutNode(self.parent.getNode(x-1,y-2))
            self.parent.cutNode(self.parent.getNode(x,y-2))
            self.parent.cutNode(self.parent.getNode(x+1,y-2))
            self.parent.cutNode(self.parent.getNode(x-2,y-1))
            self.parent.cutNode(self.parent.getNode(x-2,y))
            self.parent.cutNode(self.parent.getNode(x-2,y+1))

        self.parent.cutNode(self.parent.getNode(x,y))
        
    def assezRessources(self,couts): #fr
        if(self.listeRessource[0] < couts[0]
           or self.listeRessource[1] < couts[1]
           or self.listeRessource[2] < couts[2]):
            print("Ressources insuffisantes")
            return False;
        return True;
            
    def supprimerBatiment(self,idBatiment): #fr
        try:
            size = self.listeBatiment[idBatiment].size
            x = int(self.listeBatiment[idBatiment].position[0]/32)
            y = int(self.listeBatiment[idBatiment].position[1]/32)
            print(y)
            if(size == 32):
                self.parent.reattachNode(x,y)
            
            if(size == 64):
                self.parent.reattachNode(x,y)
                self.parent.reattachNode(x-1,y-1)
                self.parent.reattachNode(x-1,y)
                self.parent.reattachNode(x,y-1)
            
            if(size == 128):
                self.parent.reattachNode(x,y)

                self.parent.reattachNode(x-1,y-1)
                self.parent.reattachNode(x-1,y)
                self.parent.reattachNode(x,y-1)

                self.parent.reattachNode(x+1,y+1)
                self.parent.reattachNode(x+1,y)
                self.parent.reattachNode(x+1,y-1)
                self.parent.reattachNode(x-1,y+1)
                self.parent.reattachNode(x,y+1)
                self.parent.reattachNode(x-2,y-2)
                self.parent.reattachNode(x-1,y-2)
                self.parent.reattachNode(x,y-2)
                self.parent.reattachNode(x+1,y-2)
                self.parent.reattachNode(x-2,y-1)
                self.parent.reattachNode(x-2,y)
                self.parent.reattachNode(x-2,y+1)
            
            del self.listeBatiment[idBatiment]
            #print("batiment supprime")
        
        except KeyError:
            pass

    def creerUnite(self,nom,position, attributs):### donner une destination en arg par rapport a la pos du batiment qui l'a cree ou autre ?
        self.listeUnite[self.idCountUnit] = Unit(self.parent, nom, (position[0],position[1]), self.noJoueur, attributs, self.idCountUnit)   #name, xy, owner, attribut, idU, destination = None
        self.idCountUnit+=1
        print(self.listeUnite[self.idCountUnit-1].name,"cree")

    def supprimerUnite(self,idUnite):
        try:
            del self.listeUnite[idUnite]
            print("unite supprime")
        except KeyError:
            pass

    def soustraireRessource(self, attributRessource):
        self.listeRessource[0] -= attributRessource[0] #food
        self.listeRessource[1] -= attributRessource[1] #metaux
        self.listeRessource[2] -= attributRessource[2] #energie

    def changerAge(self):
        self.ageRendu += 1
        self.maxPop += 15
    
    def compterRessource (self):
        for _, i in self.listeBatiment.items():
            if i.name == "farm":
                self.listeRessource[0]+= self.generateFerme(i)
            elif i.name == "mine":
                self.listeRessource[1]+= self.generateMine(i)
            elif i.name == "solarPanel":
                self.listeRessource[2]+= self.generateSolar(i)



    def generateFerme(self,ferme):
        self.ressource=ferme.generate()
        self.ressource = self.ressource * self.modif.generatorProduction[self.modif.FARM]
        return self.ressource

    def generateMine(self,mine):
        self.ressource=mine.generate()
        self.ressource = self.ressource * self.modif.generatorProduction[self.modif.MINE]
        return self.ressource

    def generateSolar(self,solar):
        self.ressource=solar.generate()
        self.ressource = self.ressource * self.modif.generatorProduction[self.modif.SOLARPANEL]
        return self.ressource

    
        
    def compterUnite(self):#wtf is that?
        return self.unite.__len__()
        
    def mods(self):
        #@Antoine
        #Ce code n'est pas fonctionnel... Il multiplie la force par 1.5 a chaque tour de boucle... 
        #Pour une force de 10, au bout de 10 tour de boucle l'unité va fesser de 864...
        for i in self.listeArtefact:
            if (i == "Statue_de_Hera"):
                for ii in listeUnite.items():
                    force *= 1.5
            elif (i == "Corne_abondance"):
                self.listeRessource[0] += 100


    def ajoutAllier(self,idAllier):
        self.listeAllier.append(idAllier)

    def retirerAllier(self,idAllier):
        self.listeAllier.remove(idAllier)
