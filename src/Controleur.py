import Vue
import Modele
from Class import Server
from Class import Client

class Controleur:
    def __init__(self):
        self.modele = Modele.Modele()
        self.vue = Vue.Vue(self)
        self.client = None      #Client.Client()
        self.serveur = None
        self.vue.root.mainloop()

    def creeServer(self):
        self.serveur = Serveur.Serveur(nomPartie,nomJoueur)

    def lancerPartie(self):
        self.modele.initPartie

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
