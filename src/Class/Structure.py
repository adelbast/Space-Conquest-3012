class Batiment (object):
    def __init__(self,owner,name,xy,attributs,idB, initialisation = True):
        self.owner      = owner
        self.name       = name
        self.position   = xy
        self.maxHp      = attributs[0]
        self.costFood   = attributs[1][0]
        self.costMetal  = attributs[1][1]
        self.costPower  = attributs[1][2]
        self.size       = attributs[3]
        self.canBuild   = attributs[4]
        self.id         = idB
        self.currentHp  = self.maxHp
        self.estConstruit = True
        self.deleteCallDone = False
        if(not initialisation):
            self.currentHp  = 1
            self.estConstruit = False
        self.moduloConstruction = 5
        self.compteurConstruction = 0
        
        
    def construire(self):
        if(not self.compteurConstruction%self.moduloConstruction):
            self.currentHp += 5
            if(self.currentHp >= self.maxHp):
                self.estConstruit = True
                self.currentHp = self.maxHp

    def selfDestroy(self):#Detruire le batiment 
        print("selfDestruct")
        self.currentHP = 0

    def takeDamage(self,damage):# Faire prendre de degats a un batiment
        print(self.name,"took ", damage, "damage")
        self.currentHp -= 0



class Generator(Batiment):
    def __init__(self,owner,name,xy,attributs,idB, initialisation = True):
        super(Generator,self).__init__(owner,name,xy,attributs,idB,initialisation)
        self.production = attributs[2]

    def generate(self):#retourne le nombre de ressource  generer
        if(self.estConstruit):
            return self.production
        return 0
