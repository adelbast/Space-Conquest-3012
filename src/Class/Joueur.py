import configparser

class Joueur():
    def __init__(self,nom,noJoueur):
        self.nom = nom
        self.noJoueur = noJoueur
        self.listeUnite=[]
        self.listeBatiment=[]
        self.listeArtefact=[]
        self.listeRessoure=[] #nourriture,metaux.energie
        self.maxPop=None
        self.ageRendu=None
        self.diplomatieStatus=False
        self.nbBatiment=0
        self.nbUnite=0
        self.idUnite=0
        self.idBatiment=0
        print("Joueur " + self.nom + ", numero " + str(noJoueur))
        

    def creerBatiment(self,typeBatiment,position,pathConfig):
        
        if self.batimentPossible(self,nomBatiment,self.listeRessource):
            if modele.caseDisponible(position):
                self.listeBatiment.append(typeBatiment,position)
                

            for key,value in modele.DictConfigBatiment[typeBatiment]:
                if key == "costFood":
                    self.listeRessource[0]-=value
                if key == "costMetal":
                    self.listeRessource[1]-=value
                if key == "costPower":
                    self.listeRessource[2]-=value

        return print("batiment cree")

    def supprimerBatiment(self,batiment):
        if batiment.owner==self.NoJoueur:
            batiment.selfDestroy()

            return print("batiment supprime")

    def creerInfanterie(self,typeUnite,position):
        
        if unitePossible(self,typeUnite,self.listeRessource):
            if modele.caseDisponible(position):
                self.listeUnite.append(typeUnite,position)

            for key,value in modele.DictConfigInfanterie[typeBatiment]:
                if key == "costFood":
                    self.listeRessource[0]-=value
                if key == "costMetal":
                    self.listeRessource[1]-=value
                if key == "costPower":
                    self.listeRessource[2]-=value
                    
            return print("infanterie cree")
        
    def creerVehicule(self,typeUnite,position):
        
        if unitePossible(self,typeUnite,self.listeRessource):
            if modele.caseDisponible(position):
                self.listeUnite.append(typeUnite,position)

            for key,value in modele.DictConfigVehicule[typeBatiment]:
                if key == "costFood":
                    self.listeRessource[0]-=value
                if key == "costMetal":
                    self.listeRessource[1]-=value
                if key == "costPower":
                    self.listeRessource[2]-=value
                    
            return print("vehicule cree")

    

    def supprimerBatiment(self,batiment):
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

    def compterBatiment(self):
        for i in self.batiment:
            nbBatiment+=1

    def compterUnite(self):
        for i in self.batiment:
            nbUnite+=1

    def mods(self):
        return ("mods additionnes aux ressources")
        
        
 
