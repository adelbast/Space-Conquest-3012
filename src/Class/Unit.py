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
        self.FOLLOW         = 3
        self.etat           = self.IDLE
        self.isWalking      = False
        self.isAmi          = True
        self.isbuildMission = False

        self.isCut = False ;
        self.reloading = 0
        self.tempsAnimation = 0
        self.MODULO = 30
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
        
        if unit:
            print("Deplacement vers unit")
            self.destination = unit         # Un Unit
            self.etat = self.FOLLOW

        elif batiment:
            print("Deplacement vers batiment")
            self.destination = batiment     # Un Batiment
            self.etat = self.GOTO_BATIMENT
            if(self.type == "builder" and self.isAmi and self.destination.currentHp < self.destination.maxHp):
                self.isbuildMission = True
        elif unePosition:
            print("Deplacement vers tile")
            self.destination = unePosition  # Un Tuple
            self.etat = self.GOTO_POSITION
            self.isCut = False
            if self.getNode(int(self.destination[0]/32),int(self.destination[1]/32)).voisins is None:
                self.isCut = True 
            
        else:
            return None
            
        try:
            if(self.destination.owner not in listeJoueurAmi):
                self.isAmi = False
            else:
                self.isAmi = True
        except:#la destination n'a pas de owner
            pass

        if(self.type != "air"):
            self.calculatePath()
        else:
            try:
                self.position[0] = self.destination[0]
                self.position[1] = self.destination[1]
            except:
                self.position[0] = self.destination.position[0]
                self.position[1] = self.destination.position[1]

        self.depassementHorizontal = False
        self.depassementVertical   = False


    def selfDestroy(self): #Detruit la unit
        self.currentHp = 0
        print("Unit self-destruct")


    def autoGestion(self, listeJoueur):
        try:
            if self.etat == self.IDLE:
                for joueur in listeJoueur:
                    if joueur.noJoueur not in listeJoueur[self.owner].listeAllie:
                        for _, unite in joueur.listeUnite.items():
                            #print("estAmi",unite.owner not in listeJoueur[self.owner].listeAllie,"enRangfe",self.inRange(unite))
                            if self.inRange(unite):
                                self.setDestination(listeJoueurAmi = listeJoueur[self.owner].listeAllie, unit = unite)
                #listeUnite = [unite for _, unite in  if unite.owner not in listeJoueur[self.owner].listeAllie and self.inRange(unite)]
                #if(listeUnite):
                #    self.setDestination(listeJoueurAmi = listeJoueur[self.owner].listeAllie, unit = listeUnite[0])
            elif(self.etat != self.GOTO_POSITION and not self.isAmi and self.inRange(self.destination)):
                if(self.reloading <= 0):
                    self.attaque()
                    self.tempsAnimation = self.attackSpeed/2
                    self.reloading = self.attackSpeed
                    #print("attaque")
                #else:print("reloading")
            elif(self.tempsAnimation <= 0):
                if(self.etat == self.FOLLOW):
                    self.followModulator += 1
                    if (self.destination.isWalking and not self.followModulator%self.MODULO and self.type != "air"):
                        self.calculatePath()
                self.move(listeJoueur)
            self.tempsAnimation -= 1
            self.reloading -= 1

        except AttributeError as e:
            print(traceback.print_exc())
            print("La cible n'existe plus pendant l'etat "+str(self.etat)+" du Unit \ ID \ noProprio : "+self.name+" \ "+str(self.id)+" \ "+str(self.owner))
            self.destination = None
            self.etat = self.IDLE
            self.followModulator = 0


    def move(self,listeJoueur):
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
                    if(self.getNode(self.path[0].x,self.path[0].y).voisins is None):
                        self.calculatePath()
            else:
                self.positionFluide[0] = self.position[0]
                self.positionFluide[1] = self.position[1]
                self.isWalking = False
                self.currentFrame = '1'
                if(self.etat == self.GOTO_POSITION):

                    #for unit in [ u for _, u in [joueur.listeUnite.items() for joueur in listeJoueur] if self.positionFluide[0] == u.positionFluide[0] and self.positionFluide[1] == u.positionFluide[1]]
                    newDestination = None#self.unitFormation() #A debug svp
                    #print(newDestination)
                    
                    #Si la unit doit se mettre en formation
                    if(newDestination is not None):
                        #print("Formation", self.destination, newDestination)
                        self.destination = newDestination
                        self.calculatePath()
                           
                    else:
                        #print("Pas de formation")
                        self.etat = self.IDLE

                elif(self.etat == self.FOLLOW):
                    self.position[0] = self.destination.position[0]
                    self.position[1] = self.destination.position[1]

                elif(self.type == "builder" and self.isAmi and self.destination.currentHp < self.destination.maxHp):
                       self.destination.construire()

                return 1

        self.isWalking = True

        bonus = 0 

        own = self.parent.listeJoueur[self.owner]
        print(self.type)
        print
        if self.type == "infantry":
            bonus = own.modif.infantryBoost[own.modif.VITESSE]
        elif self.type == "range":
            bonus = own.modif.rangeBoost[own.modif.VITESSE]
        elif self.type == "vehicule":
             bonus = own.modif.builderBoost[own.modif.VITESSE]
        elif self.type == "air":
            bonus = own.modif.airBoost[own.modif.VITESSE]
        elif self.type == "builder":
            bonus = own.modif.builderBoost[own.modif.VITESSE]

       

        vitesseTempo = self.vitesse + bonus

        if  (not self.depassementHorizontal and self.positionFluide[0] > self.position[0]):
            self.positionFluide[0] = self.positionFluide[0]-vitesseTempo
            self.orientation = "left"
            if (self.positionFluide[0] <= self.position[0]):
                self.depassementHorizontal = True

        elif(not self.depassementHorizontal and self.positionFluide[0] < self.position[0]):
            self.positionFluide[0] = self.positionFluide[0]+vitesseTempo
            self.orientation = "right"
            if (self.positionFluide[0] >= self.position[0]):
                self.depassementHorizontal = True

        if  (not self.depassementVertical and self.positionFluide[1] > self.position[1]):
            self.positionFluide[1] = self.positionFluide[1]-vitesseTempo
            self.orientation = "back"
            if (self.positionFluide[1] <= self.position[1]):
                self.depassementVertical = True

        elif(not self.depassementVertical and self.positionFluide[1] < self.position[1]):
            self.positionFluide[1] = self.positionFluide[1]+vitesseTempo
            self.orientation = "front"
            if (self.positionFluide[1] >= self.position[1]):
                self.depassementVertical = True
        

    def attaque(self):
        if(self.destination.currentHp > 0):
            try:
                if(self.type == "builder"):
                    bonus = 0 
                    own = self.parent.listeJoueur[self.owner]

                    if self.type == "infantry":
                        bonus = own.modif.infantryBoost[own.modif.FORCE]
                    elif self.type == "range":
                        bonus = own.modif.rangeBoost[own.modif.FORCE]
                    elif self.type == "vehicule":
                        bonus = own.modif.vehiculeBoost[own.modif.FORCE]
                    elif self.type == "air":
                        bonus = own.modif.airBoost[own.modif.FORCE]
                    elif self.type == "builder":
                        bonus = own.modif.builderBoost[own.modif.FORCE]

                    forceTemp = self.force + bonus

                    if(self.destination.type == "builder"):    # ==
                        self.destination.currentHp -= forceTemp-self.destination.armor
                    elif(self.destination.type == "infantry"):  # >
                        self.destination.currentHp -= forceTemp-self.destination.armor
                    elif(self.destination.type == "air"):       # > peut pas attaquer
                        pass
                    elif(self.destination.type == "vehicule"):  # >
                        self.destination.currentHp -= forceTemp-self.destination.armor
                    elif(self.destination.type == "range"):     # >
                        self.destination.currentHp -= forceTemp-self.destination.armor
                elif(self.type == "infantry"):
                    if(self.destination.type == "builder"):    # ==
                        self.destination.currentHp -= forceTemp-self.destination.armor
                    elif(self.destination.type == "infantry"):    # ==
                        self.destination.currentHp -= forceTemp-self.destination.armor
                    elif(self.destination.type == "air"):       # > peut pas attaquer
                        pass
                    elif(self.destination.type == "vehicule"):  # >
                        self.destination.currentHp -= forceTemp-self.destination.armor*2
                    elif(self.destination.type == "range"):     # <
                        self.destination.currentHp -= forceTemp*.5
                elif(self.type == "range"):
                    if(self.destination.type == "builder"):    # ==
                        self.destination.currentHp -= forceTemp-self.destination.armor
                    elif(self.destination.type == "infantry"):    # <
                        self.destination.currentHp -= forceTemp
                    elif(self.destination.type == "air"):       # <
                        self.destination.currentHp -= forceTemp-self.destination.armor
                    elif(self.destination.type == "vehicule"):  # >
                        self.destination.currentHp -= forceTemp-self.destination.armor*2
                    elif(self.destination.type == "range"):     # ==
                        self.destination.currentHp -= forceTemp-self.destination.armor
                elif(self.type == "air"):
                    #print("Vehicule Aerien Attaque")
                    if(self.destination.type == "builder"):    # ==
                        self.destination.currentHp -= forceTemp-self.destination.armor
                    if(self.destination.type == "infantry"):    # >
                        self.destination.currentHp -= forceTemp-self.destination.armor
                    elif(self.destination.type == "air"):       # ==
                        self.destination.currentHp -= forceTemp-self.destination.armor
                    elif(self.destination.type == "vehicule"):  # <
                        self.destination.currentHp -= forceTemp-self.destination.armor
                    elif(self.destination.type == "range"):     # <
                        self.destination.currentHp -= forceTemp-self.destination.armor
                elif(self.type == "vehicule"):
                    #print("Attacker : ", self.name, "Target : ", self.destination.type)
                    if(self.destination.type == "builder"):    # ==
                        self.destination.currentHp -= forceTemp-self.destination.armor
                    if(self.destination.type == "infantry"):    # <
                        self.destination.currentHp -= forceTemp-self.destination.armor
                    elif(self.destination.type == "air"):       # >
                        self.destination.currentHp -= forceTemp/2-self.destination.armor
                    elif(self.destination.type == "vehicule"):  # ==
                        self.destination.currentHp -= forceTemp-self.destination.armor
                    elif(self.destination.type == "range"):     # <
                        self.destination.currentHp -= forceTemp-self.destination.armor
            except:
                    #print("dans attaque de batiment")
                    self.destination.currentHp -= forceTemp

            if(self.destination.currentHp<0):
                self.destination.currentHp=-1
        else:
            self.etat = self.IDLE
    
    def inRange(self,unit):
        try:
            if  math.sqrt(abs(self.positionFluide[0] - unit.positionFluide[0])**2 + abs(self.positionFluide[1] - unit.positionFluide[1])**2) < self.rangeAtt:
                return True
        except:
            if  math.sqrt(abs(self.position[0] - unit.position[0])**2 + abs(self.position[1] - unit.position[1])**2) < self.rangeAtt:
                return True
        return False

    #Place les units en formation
    def unitFormation(self):
        
        newDestination = None

        #Position du Unit
        pX = self.position[0]
        pY = self.position[1]

        #Compteurs
        compteurX = 0
        compteurY = 0

        numOption = (1)+1 #Le +1 est en fait -1 + 2, parce qu'il faut aller un cube en haut (-1) et il faut rajouter 2 pour aller 1 cube en bas
        
        #Regarde si la case choisit est valide
        if(self.parent.getNode(int(pX/32), int(pY/32)) not in self.parent.cutNodes):
            #Compare les autres unites du joueur
            for _,unit in self.parent.listeJoueur[self.parent.noJoueurLocal].listeUnite.items():
                node1, node2 = self.parent.getNode(int(pX/32), int(pY/32)), self.parent.getNode(int(unit.position[0]/32), int(unit.position[1]/32))

                if((node1.x == node2.x and node1.y == node2.y) and self.id != unit.id):
                    validatePosition = False
                    pX -= 32
                    pY -= 32
                    break
                else:
                    validatePosition = True


        while(not validatePosition):

            #En partant du coin en haut a gauche du batiment
            if(compteurX == 0 and compteurY < numOption):
                #print("bas")
                pY = pY + self.size
                compteurY += 1
                
            #En partant du coin en bas a gauche du batiment
            elif (compteurX < numOption and compteurY == numOption):
                #print("droite")
                pX = pX + self.size
                compteurX += 1
                
            #En partant du coin en bas a gauche du batiment
            elif(compteurX == numOption and compteurY > 0):
                #print("haut")
                pY = pY - self.size
                compteurY -= 1
                
            #En partant du coin en haut a droite
            elif(compteurY == 0 and compteurX > 1):
                #print("droite")
                pX = pX - self.size
                compteurX -= 1

            #Si on a finit de regarder toutes les positions posibles
            elif(compteurX == 1 and compteurY == 0):
                numOption += 2
                pX = pX - self.size*2
                pY = pY - self.size
                compteurX = 0
                compteurY = 0
                
            
            if(node1.x == node2.x and node1.y == node2.y and self.id != unit.id):
                #print("Invalide")
                validatePosition = False
                node2 = self.parent.getNode(int(unit.position[0]/32), int(unit.position[1]/32))
                break
            else:
                #print("Valide")
                validatePosition = True
                        
        if(self.destination != (pX,pY)):
            newDestination = (pX, pY)
                
        return newDestination

######################################################################################################Fonctions du pathfinder

    def calculatePath(self):
        ####  Va chercher le node du graphe qui correspond a la destination
        if self.etat == self.GOTO_POSITION:
            if self.isCut :
                self.goal = self.recalibrerDestination(self.parent.graph, self.getNode(int(self.destination[0]/32)
                                     ,int(self.destination[1]/32)),self.getNode(math.trunc(self.position[0]/32), math.trunc(self.position[1])/32))
            else:
                self.goal = self.getNode(int(self.destination[0]/32)
                                         ,int(self.destination[1]/32))
        elif self.etat == self.GOTO_BATIMENT:
            self.goal = self.recalibrerDestination(self.parent.graph, self.getNode(int(self.destination.position[0]/32)
                                     ,int(self.destination.position[1]/32)),self.getNode(math.trunc(self.position[0]/32), math.trunc(self.position[1])/32))
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
               self.liste.insert(0,self.getNode(i.x,i.y))

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
        
        return self.parent.graph[int(x)*(self.parent.map.numRow*2)+int(y)]

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


    def recalibrerDestination(self,graph, start, goal):     #Algorithme pathfinder modifie, retourne une destination// Arguments : Node[] graph, Node start, Node goal
       frontier = PriorityQueue()
       frontier.put(start, 0)
       came_from = {}
       cost_so_far = {}
       came_from[start] = None
       cost_so_far[start] = 0
       dirs = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [-1, -1],[1, -1]]
       current = None
   
       while not frontier.empty():
          #print("not empty")
          current = frontier.get()
          print(current.voisins)
          if current.voisins is not None:
             #print("valid")
             #print(current.x, current.y)
             break
          for next in dirs:
                if next != 0:
                   new_cost = cost_so_far[current] +1
                   if self.getNode(  next[0]+current.x,   next[1]+current.y) not in cost_so_far or new_cost < cost_so_far[self.getNode(   next[0]+current.x,  next[1]+current.y)]:
                      cost_so_far[self.getNode(  next[0]+current.x,   next[1]+current.y)] = new_cost
                      priority = new_cost + self.heuristic(goal, self.getNode(   next[0]+current.x,   next[1]+current.y  ))
                      frontier.put(self.getNode(  next[0]+current.x,  next[1] +current.y), priority)
                      came_from[self.getNode(  next[0]+ current.x  ,  next[1]+current.y)  ] = current
                
       return current

    
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
    def __init__(self,x,y,parent):
        self.x = x
        self.y = y
        self.voisins = []
        self.defineNeighbors()
        self.parent = parent

    def defineNeighbors(self):
        #print("bien dans define")
        self.dirs = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [-1, -1],[1, -1]]
        for dir in self.dirs:    #attention, dir est un keyword de python...
            if self.x + dir[0] >= 0:
                if  self.y + dir[1] >= 0:
                    self.voisins.append([self.x + dir[0], self.y + dir[1]])
                else:
                    self.voisins.append([0,0])
            else:
                self.voisins.append([0,0])

    def relink(self):
        for i in self.dirs:
            if self.parent.getNode(i[0]+self.x,i[1]+self.y).voisins is not None:
                self.voisins.append([i[0]+self.x,i[1]+self.y])
            else:
                self.voisins.append([0,0])
                
   

   

