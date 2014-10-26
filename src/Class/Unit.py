import configparser
from math import *

class Unit:    ##Laurence
    def __init__(self, name, xy, owner, attribut, idU, destination = None):
        
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

        self.actualHP    = self.maxHp
                      
                      
        ###Variables Temporaires
        self.currentHp   = self.maxHp
        self.destination = None  # Unit, Bâtiment ou Position(Un tuple)

        self.path        = []

        self.orientation = "front"

        #Différents constantes d'états de l'unité et son etat
        self.IDLE = 0
        self.GOTO_POSITION = 1
        self.GOTO_BATIMENT = 2
        self.FOLLOW = 3
        self.ATTACK = 4
        self.etat = self.IDLE

        self.MODULO = 20
        self.followModulator = 0

        ###Pathfinder Later###
        #if self.destination[0] != self.position[0] or self.destination[1] != self.position[1]:  #Pour savoir s'il faut bouger
         #self.path = definePath()

    def setDestination(self, unit = None, batiment = None, unePosition = None):
        if unit:
            print("Deplacement vers unit")
            self.destination = unit         # Un Unit
            self.etat = self.FOLLOW
        elif batiment:
            print("Deplacement vers batiment")
            self.destination = batiment     # Un Batiment
            self.etat = self.GOTO_BATIMENT
        elif unePosition:
            print("Deplacement vers tile")
            self.destination = unePosition  # Un Tuple
            self.etat = self.GOTO_POSITION
        else:
            return None
        self.calculatePath()
    
    def takeDmg(self,dmg):
        print("Damage Taken")

    def selfDestroy(self):
        self.currentHp = 0
        print("Unit self-destruct")

    def calculatePath(self):
        print("Path Calculated")

    def autoGestion(self,listeJoueurAmi):
        try:
            if self.etat == self.IDLE:
                pass
                # Si c'est un banal déplacement      # Si déplacement vers batiment   # Si déplacement vers unité       # Si la cible est ami                     # Si la cible n'est pas en range
            elif self.etat == self.GOTO_POSITION or self.etat == self.GOTO_BATIMENT or self.etat == self.FOLLOW or (self.destination.owner in listeJoueurAmi) or not self.inRange(self.destination):
                self.move()
                if self.etat == self.FOLLOW:
                    self.followModulator += 1
                    if not self.followModulator%self.MODULO:
                        self.calculatePath()
            else:   # Ce n'est pas un ami et est en range (huhuhu...)
                self.destination.takeDmg(self.force)
        except:
            print("La cible n'existe plus pendant l'etat "+str(self.etat)+" du Unit \ ID \ noProprio : "+self.name+" \ "+str(self.id)+" \ "+str(self.owner))
            self.destination = None
            self.etat = self.IDLE
            self.followModulator = 0

    def move(self): # A modifier
        if self.etat == self.GOTO_POSITION:
            if self.position[0] > self.destination[0]:
                self.position[0] -= 5
            else:
                self.position[0] += 5

            if self.position[1] > self.destination[1]:
                self.position[1] -= 5
            else:
                self.position[1] += 5

            if self.position[0] == self.destination[0] and self.position[1] == self.destination[1]:
                self.etat = self.IDLE
                print("Arrivé tile")

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
                self.etat = self.IDLE
                print("Arrivé sur cible")

    
    def inRange(self,unit):
        if  math.sqrt(abs(self.position[0] - unit.position[0])**2 + abs(self.position[1] - unit.position[1])**2) < self.rangeAtt:
            return True
        return False