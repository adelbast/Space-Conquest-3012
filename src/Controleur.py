from Vue    import Vue
from Modele import Modele
from Class.Server import Server
from Class.Client import Client

class Controleur:
    def __init__(self):
        self.modele = Modele()
        self.vue = Vue(self)
        self.client = None
        self.serveur = None
        self.lancerPartie()
        self.vue.root.mainloop()

    def creeClient(self,noJoueur):
        self.client = Client(noJoueur)

    def creeServer(self):
        self.serveur = Serveur.Serveur(nomPartie,nomJoueur)

    def chercherServeur(self):
        pass

    def lancerPartie(self):
        self.vue.displayMap(self.modele.map)
        self.vue.displayHUD()
        self.modele.initPartie(0,["Xavier","Antoine","AI","Laurence","Arnaud","Francis","Alexandre","AI"],True)

    def gameLoop(self):
        self.modele.gestion()
        #self.client.envoyerInfo(dic)
        self.vue.root.after(24,self.gameLoop)

    def gererMouseClick(self,event):
        self.modele.gererMouseClic(event)

    def gererMouseDrag(self,event):
        self.modele.gererMouseDrag(event)

if __name__ == "__main__":
    c = Controleur()
