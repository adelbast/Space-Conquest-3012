import configparser
from Class.Structure import *
from Class.Unit import Unit

class Joueur():
    def __init__(self, parent,nom,noJoueur):
        self.nom = nom
        self.parent = parent
        self.noJoueur = noJoueur
        self.listeUnite={}
        self.listeBatiment={}
        self.listeArtefact=[]
        self.listeRessource=[10000,10000,10000] #nourriture,metaux,energie
        self.maxPop=None
        self.ageRendu=None
        self.diplomatieStatus=False
        self.nbBatiment=0
        self.nbUnite=0
        self.idCountBatiment=0
        self.idCountUnit=0
        self.listeAllie = [self.noJoueur]#self.noJoueur
        

    def creerBatiment(self,position,worker,nom,attributs): #fr
        if self.assezRessources(attributs[1]): #pour savoir si assezRessource
            print("1")
            if self.positionCreationValide(position,attributs[3]):
                print("2")
                if nom == "ferme" or nom == "mine" or nom == "solarPanel":
                    self.listeBatiment[self.idCountBatiment] = Generator(self.noJoueur, nom, position, attributs, self.idCountBatiment)
                else:
                    print("1")
                    self.listeBatiment[self.idCountBatiment] = Batiment(self.noJoueur, nom, position, attributs, self.idCountBatiment)
                self.idCountBatiment+=1
                self.listeRessource[0] -= attributs[1][0] #food
                self.listeRessource[1] -= attributs[1][1] #metaux
                self.listeRessource[2] -= attributs[1][2] #energie
                #changer value des tiles sur lequel le batiment est ici ?? ou dans modele?

                return print("batiment cree")
    
    def positionCreationValide(self,position,attribut):
        x = int(position[0]/32)
        y = int(position[1]/32)
        valide = True

        for joueur in self.parent.listeJoueur:
            print(joueur.nom)
            for _, unit in joueur.listeUnite.items():
                if(int(unit.position[0]/32) == x and int(unit.position[1]/32) == y):
                    valide = False
        
        if self.parent.getNode(x,y) in self.parent.cutNodes:
            valide = False
        
        if(valide and attribut == 64):
            if (self.parent.getNode(x-1,y-1) in self.parent.cutNodes 
                or self.parent.getNode(x-1,y) in self.parent.cutNodes 
                or self.parent.getNode(x,y-1) in self.parent.cutNodes):
                valide = False
            elif(valide):
                for joueur in self.parent.listeJoueur:
                    print(joueur.nom)
                    for _, unit in joueur.listeUnite.items():
                        if(int(unit.position[0]/32) == x and int(unit.position[1]/32) == y
                            or int(unit.position[0]/32) == x-1 and int(unit.position[1]/32) == y-1
                            or int(unit.position[0]/32) == x-1 and int(unit.position[1]/32) == y
                            or int(unit.position[0]/32) == x and int(unit.position[1]/32) == y-1 ):
                            valide = False
            else:
                self.parent.cutNode(self.parent.getNode(x-1,y-1))
                self.parent.cutNode(self.parent.getNode(x-1,y))
                self.parent.cutNode(self.parent.getNode(x,y-1))
        
        if (valide and attribut == 128):
            if (self.parent.getNode(x+1,y+1) in self.parent.cutNodes 
                or self.parent.getNode(x-2,y+1) in self.parent.cutNodes 
                or self.parent.getNode(x+1,y-2) in self.parent.cutNodes 
                or self.parent.getNode(x-2,y-2) in self.parent.cutNodes
                or self.parent.getNode(x-2,y) in self.parent.cutNodes
                or self.parent.getNode(x-2,y-1) in self.parent.cutNodes
                or self.parent.getNode(x-1,y-2) in self.parent.cutNodes
                or self.parent.getNode(x,y-2) in self.parent.cutNodes
                or self.parent.getNode(x-2,y-2) in self.parent.cutNodes
                or self.parent.getNode(x+1,y) in self.parent.cutNodes
                or self.parent.getNode(x-2,y-2) in self.parent.cutNodes
                or self.parent.getNode(x+1,y-1) in self.parent.cutNodes
                or self.parent.getNode(x,y+1) in self.parent.cutNodes
                or self.parent.getNode(x-1,y+1) in self.parent.cutNodes):
                valide = False
            elif(valide):
                for joueur in self.parent.listeJoueur:
                    print(joueur.nom)
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
            else:
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
        if valide:
            self.parent.cutNode(self.parent.getNode(x,y))
        
        return valide
        
    def assezRessources(self,couts): #fr
        if(self.listeRessource[0] < couts[0]
           or self.listeRessource[1] < couts[1]
           or self.listeRessource[2] < couts[2]):
            return False;
        return True;
            
    def supprimerBatiment(self,idBatiment): #fr
        try:    
            del self.listeBatiment[idBatiment]
            print("batiment supprime")
        except KeyError:
            pass

    def creerUnite(self,nom,position, attributs):### donner une destination en arg par rapport a la pos du batiment qui l'a cree ou autre ?
        if(self.assezRessources(attributs[2])):
            self.listeUnite[self.idCountUnit] = Unit(self.parent,nom, (position[0],position[1]), self.noJoueur, attributs, self.idCountUnit)   #name, xy, owner, attribut, idU, destination = None
            self.idCountUnit+=1
            self.listeRessource[0] -= attributs[2][0] #food
            self.listeRessource[1] -= attributs[2][1] #metaux
            self.listeRessource[2] -= attributs[2][2] #energie
            print(self.listeUnite[self.idCountUnit-1].name,"cree")
            return 1
        else:
            print("Ressource insuffisante")
            return 0

    def supprimerUnite(self,idUnite):
        try:
            del self.listeUnite[idUnite]
            print("unite supprime")
        except KeyError:
            pass

    def changerAge(self):
        self.ageRendu += 1
        maxPop += maxPop
    
    def compterRessource (self):
        for _, i in self.listeBatiment.items():
            if i.name == "ferme":
                self.listeRessource[0]+= self.generateFerme(i)
            elif i.name == "mine":
                self.listeRessource[1]+= self.generateMine(i)
            elif i.name == "solarPanel":
                self.listeRessource[2]+= self.generateSolar(i)



    def generateFerme(self,ferme):
        self.ressource=ferme.generate()
        for i in self.listeArtefact:
            if (i == "Corne_abondance"):
                self.ressource = self.ressource * 1.5
        return self.ressource

    def generateMine(self,mine):
        self.ressource=mine.generate()
        for i in self.listeArtefact:
            if (i == "Marteau_de_gnome"):
                self.ressource = self.ressource * 1.5
        return self.ressource

    def generateSolar(self,solar):
        self.ressource=solar.generate()
        for i in self.listeArtefact:
            if (i == "Miroir_des_dieux"):
                self.ressource = self.ressource * 1.5
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
        
        
 
