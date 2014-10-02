from Tile.Map import Map
from Class.Joueur import Joueur
from Class.AI import AI


class Modele(object):
    def __init__(self):
        self.host = False
        self.listeJoueur = []
        self.noJoueurLocal = None

        self.maxUnite = 20  #???
        self.listeUniteSelectionne = []
        
        self.map = Map("Tile/map1.csv")

        self.dicAction2Server = {}
        self.dicActionFromServer = [{#joueur1
                                    "Deplacement":     (0, 500,500),#(noUnit, cibleX, cibleY)
                                    "DeplacementCible":(1, 2, 1, 0),#(noUnit, noProprio, 0:unité/1:structure , noUnitCible)
                                    "RechercheAge": 1,          #si changement d'âge
                                    "NewUnit":      (0,0),      #(type d'unité, noDuBatimentSpawner)
                                    "NewStruct":    (2,200,200),#(typeBatiment, posX, posY)
                                    "SuppressionBatiment":1,    #noBatiment
                                    "SuppressionUnit":2},       #noUnit
                                    
                                    {#joueur2

                                    },
                                    {},#joueur3
                                    {}]#joueur4...

    def initPartie(self,noJoueur,listeNomJoueur,host=False):
        self.noJoueurLocal = noJoueur
        for nomJoueur in listeNomJoueur:
            if(nomJoueur == "AI"):
                self.listeJoueur.append(AI(len(self.listeJoueur)))
            else:
                self.listeJoueur.append(Joueur(nomJoueur,len(self.listeJoueur)))
        self.host = host



    def gestion(self,dicActionFromServer):

        for joueur in self.listeJoueur:
            self.check4death(joueur)
        self.listeJoueur[self.noJoueurLocal].compterRessource()


    def gererMouseClick(self,event):
        pass
    def gererMouseDrag(self,event):
        pass
    def modifierSelection(self):
        pass

    def check4death(self,joueur):
        joueur.compterBatiment()
        if(not joueur.nbBatiment):
            print(joueur.nom+" est mort")
