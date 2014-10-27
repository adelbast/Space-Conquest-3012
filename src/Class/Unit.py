import configparser
from math import *
import heapq

class Unit:    ##Laurence
    def __init__(self, parent, name, xy, owner, attribut, idU, destination = None):
        
        self.owner    = owner
        self.name     = name
        self.position = xy
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
        #self.process()
    
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
                #print("IDLE")
                pass
                # Si c'est un banal déplacement      # Si déplacement vers batiment   # Si déplacement vers unité       # Si la cible est ami                     # Si la cible n'est pas en range
            else:
                #if self.etat == self.GOTO_POSITION or self.etat == self.GOTO_BATIMENT or self.etat == self.FOLLOW or (self.destination.owner in listeJoueurAmi) or not self.inRange(self.destination):
                
                self.move()
                if self.etat == self.FOLLOW:
                    self.followModulator += 1
                    if not self.followModulator%self.MODULO:
                        self.calculatePath()
            #else:   # Ce n'est pas un ami et est en range (huhuhu...)
            #    self.destination.takeDmg(self.force)
        except Exception as e:
            print(traceback.print_exc())
            print("La cible n'existe plus pendant l'etat "+str(self.etat)+" du Unit \ ID \ noProprio : "+self.name+" \ "+str(self.id)+" \ "+str(self.owner))
            self.destination = None
            self.etat = self.IDLE
            self.followModulator = 0

    def move(self): # A modifier
        if self.etat == self.GOTO_POSITION:
            if self.position[0] > self.destination[0]:
                self.position = (self.position[0]-5,self.position[1])
            else:
                self.position = (self.position[0]+5,self.position[1])

            if (self.position[1] > self.destination[1]):
                self.position = (self.position[0],self.position[1]-5)
            else:
                self.position = (self.position[0],self.position[1]+5)

            if self.position[0] == self.destination[0] and self.position[1] == self.destination[1]:
                self.etat = self.IDLE
                print("Arrivé tile")

        else:
            if self.position[0] > self.destination.position[0]:
                self.position = (self.position[0]-5,self.position[1])
            else:
                self.position = (self.position[0]+5,self.position[1])

            if self.position[1] > self.destination.position[1]:
                self.position = (self.position[0],self.position[1]-5)
            else:
                self.position = (self.position[0],self.position[1]+5)

            if self.position[0] == self.destination.position[0] and self.position[1] == self.destination.position[1]:
                self.etat = self.IDLE
                print("Arrivé sur cible")

    
    def inRange(self,unit):
        if  math.sqrt(abs(self.position[0] - unit.position[0])**2 + abs(self.position[1] - unit.position[1])**2) < self.rangeAtt:
            return True
        return False

    def get_heuristic(self,cell):
        # methode manhattan : 10 * somme entre la difference entre x arrive et depart et y arrive et depart
        return 10 * (abs(cell.x - self.arrive.x) + abs(cell.y - self.arrive.y))


    def get_cell(self ,x ,y):
        return self.cells[x * self.grid_height + y]
        """ on fait * la hauteur de la grid pour aller chercher dans la bonne "rangee" """

    # pour optimisation, calculer une seule fois pour toute les cases avec le init_grid... a voir
    def get_adjacent_cells(self,cell):
        cells=[]
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1,cell.y))
        if cell.x < self.grid_width-1 and cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x+1,cell.y+1))
            #print("hd")
        if cell.x < self.grid_width-1 and cell.y > 0 :
            cells.append(self.get_cell(cell.x+1,cell.y-1))
            #print("bd")
        if cell.x > 0 and cell.y > 0 :
            cells.append(self.get_cell(cell.x-1,cell.y-1))
            #print("bg")
        if cell.x > 0 and cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x-1,cell.y+1))
            #print("hg")
        if cell.y > 0:
            cells.append(self.get_cell(cell.x,cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1,cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x,cell.y+1))

        return cells

    def display_path(self):
        cell = self.arrive
        while cell.parent is not self.arrive:
            cell = cell.parent
            print ('path: cell: %d,%d' % (cell.x, cell.y))
            #print ("valeur de f :" + str(cell.f))
            #print ("valeur de g :" + str(cell.g))
        print("done")

    def get_path(self):
        #reverse display path pour faire debut jusqu'a fin plutot que fin jusqu'a debut
        path = []
        return path

    def update_cell(self,adj,cell):
        if adj.x != cell.x and adj.y != cell.y:
            adj.g = cell.g+14
            #print("move diagonal")
        else:
            adj.g = cell.g+10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        self.cells = self.parent.cells
        self.grid_height = self.parent.map.numRow
        self.grid_width = self.parent.map.numCol
        self.depart = self.get_cell(int(self.position[0]/64),int(self.position[1]/64))
        self.arrive = self.get_cell(int(self.destination[0]/64),int(self.destination[1]/64))
        self.listeOuverte=[]
        heapq.heapify(self.listeOuverte) # ordonne la liste ouverte en arbre binaire
        self.listeFermee = set()
        heapq.heappush(self.listeOuverte, (self.depart.f,self.depart))
        while len(self.listeOuverte):
            f,cell = heapq.heappop(self.listeOuverte)
            self.listeFermee.add(cell)
            if cell is self.arrive:
                self.display_path()
                break
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.walkable and adj_cell not in self.listeFermee:
                    if(adj_cell.f, adj_cell) in self.listeOuverte:
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell,cell)
                    else:
                        self.update_cell(adj_cell,cell)
                        heapq.heappush(self.listeOuverte, (adj_cell.f, adj_cell) )