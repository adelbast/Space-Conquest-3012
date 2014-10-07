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
        self.lancerPartie()#lorsque le menu sera fait, utiliser la fontion du bas plutôt que celle-ci
        #self.vue.afficherMenu()
        self.vue.root.mainloop()

    def creeClient(self,noJoueur):
        self.client = Client(noJoueur)

    def creeServeur(self):
        self.serveur = Serveur.Serveur(nomPartie,nomJoueur)

    def chercherServeur(self):
        pass

    def lancerPartie(self):
        self.modele.initPartie(0,["Xavier","Antoine","AI","Laurence","Arnaud","Francis","Alexandre","AI"],True)
        self.vue.displayMap(self.modele.map)
        self.vue.displayObject(self.modele.listeJoueur,[])
        self.vue.displayHUD()
        

    def gameLoop(self):
        self.modele.gestion(self.client.pullAction())
        self.client.pushAction(self.modele.dicAction2Server)
        self.vue.root.after(24,self.gameLoop)

    def gererMouseClick(self,event):

        #Obtenir la position du canvas
        offset = self.vue.getSurfacePos()
        
        self.modele.ClickPosx = event.x+offset[0]
        self.modele.ClickPosy = event.y+offset[1]

    def gererMouseDrag(self, event):
        print("DRAG", "depart: " ,self.modele.ClickPosx , self.modele.ClickPosy, "Fin: ", event.x,  event.y)
        self.vue.displaySelection((self.modele.ClickPosx,self.modele.ClickPosy), event)

    def gererMouseRelease(self,event):
        self.vue.eraseSelection()
        self.modele.drag = False
        self.modele.gererMouseRelease(event, self.vue.getSurfacePos())

if __name__ == "__main__":
    c = Controleur()
