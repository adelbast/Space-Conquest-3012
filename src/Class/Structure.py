class Batiment (object):
    def __init__(self,name,xy,attributs):
        self.name = name
        self.position = xy
        self.size = 128
        
        '''self.cost = cost
        self.hp =hp
        self.image =img
        self.size = size
        self.owner = owner'''

    def selfDestroy(self):#Detruire le batiment 
        print("selfDestruct")
        self.hp = 0

    def takeDamage(self,damage):# Faire prendre de degats a un batiment
        print(self.name,"took ", damage, "damage")
        self.hp -= 0



class Generator(Batiment):
    def __init__(self, genType,amountGen,name,xy,cost,hp,img,size,owner):
        super(Generator,self).__init__(name,xy,cost,hp,img,size,owner)
        self.genType = genType
        self.amountGen = amountGen

    def generate(self):#retourne le nombre de ressource  generer
        print("returning ",self.amountGen,"de type: ",genType)
        return self.amountGen

    
class Barrack(Batiment):
    def __init__(self,unitList,amountGen,name,xy,cost,hp,img,size,owner):
        self.unitList = UnitList
        super(Generator,self).__init__(name,xy,cost,hp,img,size,owner)
        
    def createUnit(self,unitListID):
        return self.unitList[unitListID]
    
        
        
