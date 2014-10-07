import configparser
from Class.Structure import Batiment
from Class.Unit import Unit

class Joueur():
    def __init__(self,nom,noJoueur):
        self.nom = nom
        self.noJoueur = noJoueur
        self.listeUnite=[]
        self.listeBatiment=[]
        self.listeArtefact=[]
        self.listeRessource=[10000,10000,10000] #nourriture,metaux.energie
        self.maxPop=None
        self.ageRendu=None
        self.diplomatieStatus=False
        self.nbBatiment=0
        self.nbUnite=0
        print("Joueur " + self.nom + ", numero " + str(noJoueur))
        

    def creerBatiment(self,position,worker,nom,attributs): #fr
        if self.assezRessources(nom,attributs[1]): #pour savoir si assezRessource
                self.listeBatiment.append(Batiment(nom,position,attributs ))
                self.listeRessource[0] -= attributs[1][0] #food
                self.listeRessource[1] -= attributs[1][1] #metaux
                self.listeRessource[2] -= attributs[1][2] #energie
                return print("batiment cree")

    def assezRessources(self,nom,couts): #fr
        if(self.listeRessource[0] < couts[0]
           or self.listeRessource[1] < couts[1]
           or self.listeRessource[2] < couts[2]):
            return False;
        return True;
            
    def supprimerBatiment(self,idbatiment): #fr
        count =0
        for i in self.listeBatiment:
            if (i.id == idbatiment):
                self.listeBatiment.pop(count)
                return print("batiment supprime")
            count+=1

    def creerUnite(self,nom,position, attributs):###A modif
        self.listeUnite.append(Unit(nom,position,self.noJoueur,[100,200],attributs))

    def supprimerUnite(self,unite):
        if unite.proprio==self.NoJoueur:
            self.listeUnite.remove(unite)
            
        return print("unite supprimee")
    
    def compterRessource(self):
        for i in self.batiment:
            if i.nom == "ferme":
                self.listeRessource[0]+= i.generate()*self.mods()   
            if i.nom == "mine":
                self.listeRessource[1]+= i.generate()*self.mods()
            if i.nom == "solarPanel":
                self.listeRessource[2]+= i.generate()*self.mods()
                

    def compterUnite(self):
        return self.unite.__len__()
        
    def mods(self):
        return ("mods additionnes aux ressources")
        
        
 
