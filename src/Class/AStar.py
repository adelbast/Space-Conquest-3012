from tkinter import *
import heapq

class Cell(object):
    def __init__(self,x,y,walkable):

        self.walkable = walkable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        """ necessaire dans python 3.X dans le cas au on doit passer par des objets avant de comparer leur valeur
    le heapq va donc venir voir ici pour determiner la valeur a passer en premier, dans ce cas ci cest les f de chaque cell """
        return self.f < other.f

class AStar(object):
    def __init__(self,tabCells,grid_height,grid_width):
        #self.listeOuverte=[]
        #heapq.heapify(self.listeOuverte) # ordonne la liste ouverte en arbre binaire
        #self.listeFermee = set()
        self.cells = tabCells
        self.size = self.gameBoard.size
        self.fait = False

    def get_heuristic(self,cell):
        # methode manhattan : 10 * somme entre la difference entre x arrive et depart et y arrive et depart
        return 10 * (abs(cell.x - self.endingCell.x) + abs(cell.y - self.endingCell.y))


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
        cell = self.endingCell
        while cell.parent is not self.startingCell:
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

    def process(self,tabCells):
        self.cells = tabCells
        self.listeOuverte=[]
        heapq.heapify(self.listeOuverte) # ordonne la liste ouverte en arbre binaire
        self.listeFermee = set()
        heapq.heappush(self.listeOuverte, (self.startingCell.f,self.startingCell))
        while len(self.listeOuverte):
            f,cell = heapq.heappop(self.listeOuverte)
            self.listeFermee.add(cell)
            if cell is self.endingCell:
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



"""
if __name__ == '__main__':
    Ass = AStar()
    Ass.init_grid()
    Ass.process()"""
