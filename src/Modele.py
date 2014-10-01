from Tile import Map


class Modele:
    def __init__(self):
        self.maxUnite = 20  #???
        self.listeJoueur = []
        self.listeUniteSelectionne = []
        self.noJoueurLocal = None
        self.map = Map.Map("Tile/map1.csv")
        self.dicAction2Server = {}
        self.dicActionFromServer = {

        }

    def initPartie(self):
        pass

    def gestion(self):
        for joueur in self.listeJoueur
        self.check4death()
        self.listeJoueur[self.noJoueurLocal].compterRessource()




    def gererMouseClick(self,event):
        pass
    def gererMouseDrag(self,event):
        pass
    def modifierSelection(self):
        pass
    def check4death(self):
        pass