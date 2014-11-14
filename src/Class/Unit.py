import configparser
import math, time 
import heapq
import traceback

class Unit:    ##Laurence
    def __init__(self, parent, name, xy, owner, attribut, idU, destination = None):
        
        self.owner    = owner
        self.name     = name
        self.position = [xy[0],xy[1]]
        self.positionFluide = [xy[0],xy[1]]
        self.id = idU
        self.parent = parent

        self.type        = attribut[0]
        self.maxHp       = attribut[1]
        self.cost        = attribut[2]
        self.force       = attribut[3]
        self.vitesse     = attribut[4]
        self.rangeVision = attribut[5]
        self.rangeAtt    = attribut[6]
        self.size        = attribut[7]
        self.canBuild    = attribut[8]
        self.armor       = attribut[9]
        self.attackSpeed = attribut[10]

        self.currentHp   = self.maxHp
        self.currentFrame = '1'
        self.lastFrameTime = None #Le temps doit etre convertit en millisecondes
                      
        self.destination = None  # Unit, Bâtiment ou Position(Un tuple)
        self.depassementVertical = False #Booleen qui indique que l'unité est rendu ou a dépassé son node d'objectif
        self.depassementHorizontal = False
        self.path        = []

        self.orientation = "front"

        #Différents constantes d'états de l'unité et son etat
        self.IDLE           = 0
        self.GOTO_POSITION  = 1
        self.GOTO_BATIMENT  = 2
        self.FOLLOW     = 3
        self.etat       = self.IDLE
        self.isWalking  = False
        self.isAmi      = True

        self.reloading = 0
        self.tempsAnimation = 0
        self.MODULO = 40
        self.followModulator = 0

        self.deleteCallDone = False #Variable d'état de suppression pour éviter de caller deux fois le serveur pour supprimer la meme unité

        ###Pathfinder Later###
        #if self.destination[0] != self.position[0] or self.destination[1] != self.position[1]:  #Pour savoir s'il faut bouger
         #self.path = definePath()
        #
        #self.step = 5 ;

    def setDestination(self, listeJoueurAmi = None, unit = None, batiment = None, unePosition = None):

        #On set un temps initial pour l'animation
        self.lastFrameTime = int(round(time.time()*1000))
        #add condition si destination est nodeCoupe
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

        if(self.type != "air"):
            self.calculatePath()
        else:
            try:
                self.position[0] = self.destination[0]
                self.position[1] = self.destination[1]
            except:
                self.position[0] = self.destination.position[0]
                self.position[1] = self.destination.position[1]
                if(self.destination.owner not in listeJoueurAmi):
                    self.isAmi = False
                else:
                    self.isAmi = True

        self.depassementHorizontal = False
        self.depassementVertical   = False


    def selfDestroy(self): #Detruit la unit
        self.currentHp = 0
        print("Unit self-destruct")


    def autoGestion(self):
        try:
            if self.etat == self.IDLE:
                pass
            elif(self.etat != self.GOTO_POSITION and not self.isAmi and self.inRange(self.destination)):
             	if(self.reloading <= 0):
                    self.attaque()
                    self.tempsAnimation = self.attackSpeed/2
                    self.reloading = self.attackSpeed
                    print("attaque")
            elif(self.tempsAnimation <= 0):
                if(self.etat == self.FOLLOW):
                    self.followModulator += 1
                    if (self.destination.isWalking and not self.followModulator%self.MODULO and self.type != "air"):
                        self.calculatePath()
                self.move()
            self.tempsAnimation -= 1
            self.reloading -= 1

        except AttributeError as e:
            print(traceback.print_exc())
            print("La cible n'existe plus pendant l'etat "+str(self.etat)+" du Unit \ ID \ noProprio : "+self.name+" \ "+str(self.id)+" \ "+str(self.owner))
            self.destination = None
            self.etat = self.IDLE
            self.followModulator = 0


    def move(self):
        if ((self.depassementHorizontal or self.positionFluide[0] == self.position[0]) and (self.depassementVertical or self.positionFluide[1] == self.position[1])):
            if( self.path and self.type != "air" ):
                newX = self.path[0].x*32
                newY = self.path[0].y*32
                if(not abs(newX-self.positionFluide[0]) < self.vitesse):
                    self.position[0] = newX
                    self.depassementHorizontal = False
                if(not abs(newY-self.positionFluide[1]) < self.vitesse):
                    self.position[1] = newY
                    self.depassementVertical   = False
                self.path.pop(0)
                if(self.path):
                    if(self.getNode(self.path[0].x,self.path[0].y) in self.parent.cutNodes):
                        self.calculatePath()
            else:
                self.positionFluide[0] = self.position[0]
                self.positionFluide[1] = self.position[1]
                self.isWalking = False
                self.currentFrame = '1'
                if(self.etat == self.GOTO_POSITION):
                    self.etat = self.IDLE
                return 1

        self.isWalking = True
        if  (not self.depassementHorizontal and self.positionFluide[0] > self.position[0]):
            self.positionFluide[0] = self.positionFluide[0]-self.vitesse
            self.orientation = "left"
            if (self.positionFluide[0] <= self.position[0]):
                self.depassementHorizontal = True

        elif(not self.depassementHorizontal and self.positionFluide[0] < self.position[0]):
            self.positionFluide[0] = self.positionFluide[0]+self.vitesse
            self.orientation = "right"
            if (self.positionFluide[0] >= self.position[0]):
                self.depassementHorizontal = True

        if  (not self.depassementVertical and self.positionFluide[1] > self.position[1]):
            self.positionFluide[1] = self.positionFluide[1]-self.vitesse
            self.orientation = "back"
            if (self.positionFluide[1] <= self.position[1]):
                self.depassementVertical = True

        elif(not self.depassementVertical and self.positionFluide[1] < self.position[1]):
            self.positionFluide[1] = self.positionFluide[1]+self.vitesse
            self.orientation = "front"
            if (self.positionFluide[1] >= self.position[1]):
                self.depassementVertical = True
        

    def attaque(self):
        if(self.type == "builder"):
            if(self.destination.type == "builder"):    # ==
                self.destination.currentHp -= self.force-self.destination.armor
            elif(self.destination.type == "infantry"):  # >
                self.destination.currentHp -= self.force-self.destination.armor
            elif(self.destination.type == "air"):       # > peut pas attaquer
                pass
            elif(self.destination.type == "vehicule"):  # >
                self.destination.currentHp -= self.force-self.destination.armor
            elif(self.destination.type == "range"):     # >
                self.destination.currentHp -= self.force-self.destination.armor
        elif(self.type == "infantry"):
            if(self.destination.type == "builder"):    # ==
                self.destination.currentHp -= self.force-self.destination.armor
            elif(self.destination.type == "infantry"):    # ==
                self.destination.currentHp -= self.force-self.destination.armor
            elif(self.destination.type == "air"):       # > peut pas attaquer
                pass
            elif(self.destination.type == "vehicule"):  # >
                self.destination.currentHp -= self.force-self.destination.armor*2
            elif(self.destination.type == "range"):     # <
                self.destination.currentHp -= self.force*.5
        elif(self.type == "range"):
            if(self.destination.type == "builder"):    # ==
                self.destination.currentHp -= self.force-self.destination.armor
            elif(self.destination.type == "infantry"):    # <
                self.destination.currentHp -= self.force
            elif(self.destination.type == "air"):       # <
                self.destination.currentHp -= self.force-self.destination.armor
            elif(self.destination.type == "vehicule"):  # >
                self.destination.currentHp -= self.force-self.destination.armor*2
            elif(self.destination.type == "range"):     # ==
                self.destination.currentHp -= self.force-self.destination.armor
        elif(self.type == "air"):
            print("Vehicule Aerien Attaque")
            if(self.destination.type == "builder"):    # ==
                self.destination.currentHp -= self.force-self.destination.armor
            if(self.destination.type == "infantry"):    # >
                self.destination.currentHp -= self.force-self.destination.armor
            elif(self.destination.type == "air"):       # ==
                self.destination.currentHp -= self.force-self.destination.armor
            elif(self.destination.type == "vehicule"):  # <
                self.destination.currentHp -= self.force-self.destination.armor
            elif(self.destination.type == "range"):     # <
                self.destination.currentHp -= self.force-self.destination.armor
        elif(self.type == "vehicule"):
            print("Attacker : ", self.name, "Target : ", self.destination.type)
            if(self.destination.type == "builder"):    # ==
                self.destination.currentHp -= self.force-self.destination.armor
            if(self.destination.type == "infantry"):    # <
                self.destination.currentHp -= self.force-self.destination.armor
            elif(self.destination.type == "air"):       # >
                self.destination.currentHp -= self.force/2-self.destination.armor
            elif(self.destination.type == "vehicule"):  # ==
                self.destination.currentHp -= self.force-self.destination.armor
            elif(self.destination.type == "range"):     # <
                self.destination.currentHp -= self.force-self.destination.armor
        if(self.destination.currentHp<0):
            self.destination.currentHp=0
    
    def inRange(self,unit):
        if  math.sqrt(abs(self.positionFluide[0] - unit.positionFluide[0])**2 + abs(self.positionFluide[1] - unit.positionFluide[1])**2) < self.rangeAtt:
            return True
        return False

######################################################################################################Fonctions du pathfinder

    def calculatePath(self):
        ####  Va chercher le node du graphe qui correspond a la destination
        if isinstance(self.destination, tuple) or isinstance(self.destination, list):
            self.goal = self.getNode(int(self.destination[0]/32)
                                     ,int(self.destination[1]/32))
        else:
            self.goal = self.getNode(int(self.destination.position[0]/32),
                                     int(self.destination.position[1]/32))
        ###

        ###Calcule le path
        try:
            cf, cost_so_far = self.a_star_search(self.parent.graph, self.getNode(math.trunc(self.position[0]/32),
                                                                                 math.trunc(self.position[1]/32)),
                                                 self.goal)
            self.liste = [] 
            self.liste1 = cost_so_far
            self.liste2 = self.reconstruct_path(cf, self.getNode(math.trunc(self.position[0]/32),
                                                                 math.trunc(self.position[1]/32)),
                                                 self.goal)

            for i in self.liste2:
               self.liste.insert(0,Node(i.x,i.y))

            self.path = self.liste
            self.path.pop(0)
            
        except:
            print(traceback.print_exc())
            print("pas de path valide")
        
        #print("VALUEEES")
        #print(self.path[0].x ,self.path[0].y)
        #print(self.path[len(self.path)-1].x, self.path[len(self.path)-1].y)

        ####
                        
    def getNode(self, x, y):
        return self.parent.graph[x*(self.parent.map.numRow*2)+y]

    def heuristic(self, a, b):
       return abs(a.x - b.x) + abs(a.y - b.y)
      
    def a_star_search(self,graph, start, goal):     #Algorithme de path finder
       frontier = PriorityQueue()
       frontier.put(start, 0)
       came_from = {}
       cost_so_far = {}
       came_from[start] = None
       cost_so_far[start] = 0
   
       while not frontier.empty():
          current = frontier.get()
          if current == goal:
             break
          if current.voisins != None:
             for next in current.voisins:
                if next != 0:
                   new_cost = cost_so_far[current] + 1
                   if self.getNode(next[0],next[1]) not in cost_so_far or new_cost < cost_so_far[self.getNode(next[0],next[1])]:
                      cost_so_far[self.getNode(next[0],next[1])] = new_cost
                      priority = new_cost + self.heuristic(goal, self.getNode(next[0],next[1]))
                      frontier.put(self.getNode(next[0],next[1]), priority)
                      came_from[self.getNode(next[0],next[1])] = current
                
       return came_from, cost_so_far

    def reconstruct_path(self, came_from, start, goal): #Reconstruit le chemin trouve par le path finder
       current = goal
       path = [current]
       while current != start:
          current = came_from[current]
          path.append(current)
       return path

    
###################
class PriorityQueue:
   def __init__(self):
      self.elements = []
      self.index = 0
   
   def empty(self):
      return len(self.elements) == 0
   
   def put(self, item, priority):
      heapq.heappush(self.elements, (priority, self.index, item))
      self.index = self.index+1
   
   def get(self):
      return heapq.heappop(self.elements)[2]
####################


    #Cette classe devrait etre mise dans un fichier a part verifier les imports puis retirer
class Node:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.voisins = []
        self.defineNeighbors()

    def defineNeighbors(self):
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [-1, -1],[1, -1]]
        for dir in dirs:    #attention, dir est un keyword de python...
            if self.x + dir[0] >= 0:
                if  self.y + dir[1] >= 0:
                    self.voisins.append([self.x + dir[0], self.y + dir[1]])
                else:
                    self.voisins.append([0,0])
            else:
                self.voisins.append([0,0])
   

   

