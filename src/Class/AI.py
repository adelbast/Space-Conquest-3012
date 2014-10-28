from Class.Joueur import Joueur

class AI(Joueur):
    def __init__(self, parent, noJoueur):
        super(AI, self).__init__(parent, "AI", noJoueur)
        self.parent = parent
        self.noJoueur = noJoueur
        self.dictionaireAction = {}
        self.compteur = 0

    def faireQqch():#bouge automatiquement(arbitrairement) l'unité 0
    	self.compteur += 1
    	if(self.compteur%200 == 0):
    		self.listeUnite[0].setDestination( unePosition = (1000,1000))
    	elif(self.compteur%200 == 100):
    		self.listeUnite[0].setDestination( unePosition = (10,1000))