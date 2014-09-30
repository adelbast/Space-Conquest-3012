from Tile import Tileset
from Tile import Map

class Modele:
    def __init__(self, parent):
        self.parent = parent
        self.map = Map.Map("Tile/map1.csv")           
        self.tileset = Tileset.Tileset("Tile/tileset.png", 64, 64) #Element visual qui doit aller dans la vue
        print(self.tileset.tileset[0].name)

class Unite():
    def __init__(self,position,noUnite,typeUnite):
        self.nom = typeUnite+ "-"+ str(noUnite) 
                                            #identifiant unique de l'unite : son type +
                                                #noUnite qui est un index dans
                                           #le modele joueur qui est unite et qui sincremente a chaque nouvelle unite
        self.position=position
    
class Ouvrier (Unite):
    def __init__(self,position,noUnite):
        self.type="Ouvrier"
        Unite.__init__(self,position,noUnite,self.type)
        
      
        
        
        
    
        
        
if __name__ == '__main__':
    c=Ouvrier(1,1);
    print(c.nom)
