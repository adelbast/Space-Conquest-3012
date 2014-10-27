__author__ = "Arnaud Girardin"

import csv

class Map:
    def __init__(self, path):
        self.map = []
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

        
        
