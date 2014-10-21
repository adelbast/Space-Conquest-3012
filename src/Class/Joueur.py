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
        self.listeRessource=[10000,10000,10000] #nourriture,metaux,energie
        self.maxPop=None
        self.ageRendu=None
        self.diplomatieStatus=False
        self.nbBatiment=0
        self.nbUnite=0
        self.idCount=0
        

    def creerBatiment(self,position,worker,nom,attributs): #fr
        if self.assezRessources(attributs[1]): #pour savoir si assezRessource
                self.listeBatiment.append(Batiment(self.noJoueur,nom,position,attributs,self.idCount ))
                self.idCount+=1
                self.listeRessource[0] -= attributs[1][0] #food
                self.listeRessource[1] -= attributs[1][1] #metaux
                self.listeRessource[2] -= attributs[1][2] #energie
                return print("batiment cree")

    def assezRessources(self,couts): #fr
        if(self.listeRessource[0] < couts[0]
           or self.listeRessource[1] < couts[1]
           or self.listeRessource[2] < couts[2]):
            return False;
        return True;
            
    def supprimerBatiment(self,idBatiment): #fr
        count =0
        for i in self.listeBatiment:
            if (i.id == idBatiment):
                self.listeBatiment.pop(count)
                return print("batiment supprime")
            count+=1

    def creerUnite(self,nom,position, attributs):### donner une destination en arg par rapport a la pos du batiment qui l'a cree ou autre ?
        if(self.assezRessources(attributs[2])):
            self.listeUnite.append(Unit(nom,position,self.noJoueur,(100,200),attributs,self.idCount))
            self.idCount+=1
            self.listeRessource[0] -= attributs[2][0] #food
            self.listeRessource[1] -= attributs[2][1] #metaux
            self.listeRessource[2] -= attributs[2][2] #energie
            return print("unite cree")


    def supprimerUnite(self,idUnite):
        count = 0
        for i in self.listeUnite:
            if(i.id == idUnite):
                self.listeUnite.pop(count)
                return print("unite supprime")
            count +=1
    
    def compterRessource(self): # a mettre dans le modele ??
        for i in self.listeBatiment:
            if i.name == "ferme":
                self.listeRessource[0]+= i.generate()*self.mods()   
            if i.name == "mine":
                self.listeRessource[1]+= i.generate()*self.mods()
            if i.name == "solarPanel":
                self.listeRessource[2]+= i.generate()*self.mods()
                

    def compterUnite(self):
        return self.unite.__len__()
        
    def mods(self):
        return ("mods additionnes aux ressources")
        
        
 
