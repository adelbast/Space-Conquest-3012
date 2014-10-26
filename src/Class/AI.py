from Class.Joueur import Joueur

class AI(Joueur):
    def __init__(self,noJoueur):
        super(AI, self).__init__("AI",noJoueur)
        self.noJoueur = noJoueur
        self.dictionaireAction = {}
        self.compteur = 0

    def faireQqch():
    	self.compteur += 1
    	if(self.compteur%10 == 0):
    		self.listeUnite[0].setDestination( unePosition = (1000,1000))
    	elif(self.compteur%10 == 5):
    		self.listeUnite[0].setDestination( unePosition = (10,1000))