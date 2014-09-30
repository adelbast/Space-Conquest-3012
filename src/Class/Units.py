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
        
class Unite():
    def __init__(self,position,noUnite,typeUnite):
        self.nom = typeUnite+ "-"+ str(noUnite) 
                                                

     
        
        

        self.infantry = Sprites.Sprites(32,32,96,128, "Sprites/infantryconfig.cfg")
        self.map = Map.Map("Tile/map1.csv")
        self.tileset = Tileset.Tileset("image/tileset/tileset.png", 64, 64)
