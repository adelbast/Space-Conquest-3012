class Node:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.voisins = []
        self.defineNeighbors()

    def defineNeighbors(self):
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [-1, -1],[1, -1]]
        for dir in dirs:
            if self.x + dir[0] >= 0:
                if  self.y + dir[1] >= 0:
                    self.voisins.append([self.x + dir[0], self.y + dir[1]])
                else:
                    self.voisins.append(0)
            else:
                self.voisins.append(0)
