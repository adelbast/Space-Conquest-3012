import configparser


class Unit:    ##Laurence
    def __init__(self, name, xy, owner, destination):
        
        self.owner    = owner
        self.name     = name
        self.position = xy

        ####Variables lues a partir d'un fichier de config
        parser = configparser.ConfigParser()
        parser.read('AttributUnits.cfg')

        self.type        = parser.get(name, 'type')
        self.maxHp       = parser.get(name, 'hp')
        self.cost        = [parser.get(name,'costFood'), parser.get(name,'costMetal'), parser.get(name,'costPower')]
        self.force       = parser.get(name,'force')
        self.vitesse     = parser.get(name, 'vitesse')
        self.rangeVision = parser.get(name, 'rangeVision')
        self.rangeAtt    = parser.get(name, 'rangeAtt')
                      
                      
        ###Variables Temporaires
        self.currentHp   = self.maxHp
        self.destination = destination
        self.path        = []

        ###Pathfinder Later###
        #if self.destination[0] != self.position[0] or self.destination[1] != self.position[1]:  #Pour savoir s'il faut bouger
         #self.path = definePath()

        
    def takeDmg(self,dmg):
        print("Damage Taken")

    def selfDestroy(self):
        self.currentHp = 0
        print("Unit self-destruct")

    def calculatePath(self):
        print("Path Calculated")
        
    def move(self):
        print("Unit moving")
    
    def inRange(self,unit):
        return True
    
    def attack(self):
        return 0












                            
                            
                            
                            

        
            
        


        
        



