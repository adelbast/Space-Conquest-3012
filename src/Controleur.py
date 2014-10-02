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
        self.drag = False
        self.clickDroitPress = None
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
        self.vue.displayHUD()
        

    def gameLoop(self):
        self.modele.gestion(self.client.pullAction())
        self.client.pushAction(self.modele.dicAction2Server)
        self.vue.root.after(24,self.gameLoop)

    def gererMouseClick(self,event):
        self.clickDroitPress = event
        self.modele.gererMouseClick(event)

    def gererMouseDrag(self,click,event):
        if(self.drag or event.x>click.x+16  or  event.x<click.x-16  or  event.y>click.y+16  or  event.y<click.y-16): #si il y a eu un déplacement de la souris de plus de 16px de la source, c'est considerer un drag
            self.drag = True
            self.vue.dessinerSelection((click.x,click.y),(event.x,event.y))

    def gererMouseRelease(self,event):
        self.drag = False
        self.modele.gererMouseRelease(self.clickDroitPress,event)

if __name__ == "__main__":
    c = Controleur()
