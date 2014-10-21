class Batiment (object):
    def __init__(self,owner,name,xy,attributs,idB):
        self.owner = owner
        self.name = name
        self.position = xy
        self.size = 128
        self.id = idB
        '''self.cost = cost
        
        self.image =img
        self.size = size
        self.owner = owner'''
        self.maxHp = attribut[0]
        self.cost = attribut[1]
        
        self.hp = self.maxHp

        self.size = attribut[3]
        

    def selfDestroy(self):#Detruire le batiment 
        print("selfDestruct")
        self.hp = 0

    def takeDamage(self,damage):# Faire prendre de degats a un batiment
        print(self.name,"took ", damage, "damage")
        self.hp -= 0



class Generator(Batiment):
    def __init__(self,owner,name,xy,attributs,idB, genType):
        super(Generator,self).__init__(owner,name,xyxy,attributs,idB)
        self.amountGen = attributs[2]

    def generate(self):#retourne le nombre de ressource  generer
        print("returning ",self.amountGen,"de type: ",genType)
        return self.amountGen

    
class Barrack(Batiment):
    def __init__(self,unitList,amountGen,name,xy,cost,hp,img,size,owner):
        self.unitList = UnitList
        super(Generator,self).__init__(name,xy,cost,hp,img,size,owner)
        
    def createUnit(self,unitListID):
        return self.unitList[unitListID]
    
        
        
