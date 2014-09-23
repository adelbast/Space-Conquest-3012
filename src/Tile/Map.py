__author__ = "Arnaud Girardin"

import csv

class Map:
    def __init__(self, path):
        self.map = []
        self.generateMapFromFile(path)

    def generateMapFromFile(self, path):

        #Lecture de la map dans le fichier csv
        with open(path, 'r') as f:
            reader = csv.reader(f)
            
            for row in reader:
                self.map.append(row)

        
        
