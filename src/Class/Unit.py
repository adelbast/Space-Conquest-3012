import configparser
from math import *

class Unit:    ##Laurence
    def __init__(self, name, xy, owner, destination, attribut,idU):
        
        self.owner    = owner
        self.name     = name
        self.position = xy
        self.id = idU

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

        self.moving = False

        ###Pathfinder Later###
        #if self.destination[0] != self.position[0] or self.destination[1] != self.position[1]:  #Pour savoir s'il faut bouger
         #self.path = definePath()

    def setDestination(self, destination):
        if destination :
            self.destination = destination
            self.calculatePath()
            self.moving = True
        
    def takeDmg(self,dmg):
        print("Damage Taken")

    def selfDestroy(self):
        self.currentHp = 0
        print("Unit self-destruct")

    def calculatePath(self):
        print("Path Calculated")
        
    def move(self):   #A modifier
        if self.moving is True:

            if isinstance(self.destination, tuple):
                if self.position[0] > self.destination[0]:
                    self.position[0] -= 5
                else:
                    self.position[0] += 5

                if self.position[1] > self.destination[1]:
                    self.position[1] -= 5
                else:
                    self.position[1] += 5

                if self.position[0] == self.destination[0] and self.position[1] == self.destination[1]:
                    self.moving = False

            else:
                if self.position[0] > self.destination.position[0]:
                    self.position[0] -= 5
                else:
                    self.position[0] += 5

                if self.position[1] > self.destination.position[1]:
                    self.position[1] -= 5
                else:
                    self.position[1] += 5

                if self.position[0] == self.destination.position[0] and self.position[1] == self.destination.position[1]:
                    self.moving = False

                
            


        
    
    def inRange(self,unit):
        if  math.sqrt(abs(self.position[0] - unit.position[0])**2 + abs(self.position[1] - unit.position[1])**2) < self.rangeAtt:
            return True
        return False
    
    def attack(self):
        return self.force












                            
                            
                            
                            

        
            
        


        
        



