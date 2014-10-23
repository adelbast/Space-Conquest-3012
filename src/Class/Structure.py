class Batiment (object):
    def __init__(self,owner,name,xy,attributs,idB):
        self.owner      = owner
        self.name       = name
        self.position   = xy
        self.hp         = attributs[0]
        self.costFood   = attributs[1][0]
        self.costMetal  = attributs[1][1]
        self.costPower  = attributs[1][2]
        self.size       = attributs[3]
        self.canBuild   = attributs[4]
        self.id         = idB
        

    def selfDestroy(self):#Detruire le batiment 
        print("selfDestruct")
        self.hp = 0

    def takeDamage(self,damage):# Faire prendre de degats a un batiment
        print(self.name,"took ", damage, "damage")
        self.hp -= 0



class Generator(Batiment):
    def __init__(self,owner,name,xy,attributs,idB):
        super(Generator,self).__init__(owner,name,xy,attributs,idB)
        self.production = attributs[2]

    def generate(self):#retourne le nombre de ressource  generer
        return self.production

    
class Barrack(Batiment):
    def __init__(self,owner,name,xy,attributs,idB):
        super(Generator,self).__init__(owner,name,xy,attributs,idB)
        self.unitList = UnitList
        
        
    def createUnit(self,unitListID):
        return self.unitList[unitListID]
    
        
        
