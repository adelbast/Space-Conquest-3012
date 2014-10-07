import configparser


class Unit:    ##Laurence
    def __init__(self, name, xy, owner, destination, attribut):
        
        self.owner    = owner
        self.name     = name
        self.position = xy

        self.type        = attribut[0]
        self.maxHp       = attribut[1]
        self.cost        = attribut[2]
        self.force       = attribut[3]
        self.vitesse     = attribut[4]
        self.rangeVision = attribut[5]
        self.rangeAtt    = attribut[6]
        self.size        = attribut[7]
                      
                      
        ###Variables Temporaires
        self.currentHp   = self.maxHp
        self.destination = destination  ##Soit un tuple (x,y), un batiment ou un Unit
        self.path        = []

        self.orientation = "front"

        ###Pathfinder Later###
        #if self.destination[0] != self.position[0] or self.destination[1] != self.position[1]:  #Pour savoir s'il faut bouger
         #self.path = definePath()

    def setDestination(self, destination):
        if destination :
            self.destination = destination
            self.calculatePath()
        
    def takeDmg(self,dmg):
        print("Damage Taken")

    def selfDestroy(self):
        self.currentHp = 0
        print("Unit self-destruct")

    def calculatePath(self):
        print("Path Calculated")
        
    def move(self):   #A modifier

        if isinstance(self.destination, tuple):
            if self.position[0] > self.destination[0]:
                self.position[0] += 1
            else:
                self.position[0] -= 1

            if self.position[1] > self.destination[1]:
                self.position[1] += 1
            else:
                self.position[1] -= 1

        else:
            if self.position[0] > self.destination.position[0]:
                self.position[0] += 1
            else:
                self.position[0] -= 1

            if self.position[1] > self.destination.position[1]:
                self.position[1] += 1
            else:
                self.position[1] -= 1


        
    
    def inRange(self,unit):
        return True
    
    def attack(self):
        return 0












                            
                            
                            
                            

        
            
        


        
        



