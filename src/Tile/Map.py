__author__ = "Arnaud Girardin &Alexandre Laplante-Turpin"

import csv

class Map:
    def __init__(self, path):
        self.map = []
        self.startingPoint =[] 
        self.numRow = 0
        self.numCol = 0
        self.generateMapFromFile(path)

    def generateMapFromFile(self, path):

        #Lecture de la map dans le fichier csv
        with open(path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.numCol = len(row)
                self.map.append(row)
                self.numRow +=1
                
            self.startingPoint.append((4,4))
            self.startingPoint.append((self.numCol-4,self.numRow-4))
            self.startingPoint.append((self.numCol-4,int(self.numRow/2)))
            self.startingPoint.append((self.numCol-4,4))
            self.startingPoint.append((int(self.numCol/2),self.numRow-4))
            self.startingPoint.append((int(self.numCol/2),int(self.numRow/2)))
            self.startingPoint.append((int(self.numCol/2),4))
            self.startingPoint.append((4,self.numRow-4))
            self.startingPoint.append((4,int(self.numRow/2)))

            

        
        
