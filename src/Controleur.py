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
        self.listeTemporaireDeClient = ["Xavier","Antoine","AI","Laurence","Arnaud","Francis","Alexandre","AI"]
        self.lancerPartie()#lorsque le menu sera fait, utiliser la fontion du bas plutôt que celle-ci
        #self.vue.afficherMenu()
        self.vue.root.mainloop()

    def creeClient(self,nom):
        self.client = Client(nom)

    def creeServeur(self,nomPartie,nomJoueur):
        self.serveur = Server(nomPartie,nomJoueur)
        self.serveur.daemon = True
        self.serveur.start()

    def lancerPartie(self):
        self.creeClient(self.listeTemporaireDeClient[1])#changer le numero pour créé plusieur client
        if(self.client.nameServer):
            self.client.connect([clee for clee, valeur in self.client.getServers().items() if clee != "Pyro.NameServer"][0])#Tente de se connecter sur la premiere clee retourner par getServers() qui n'est pas égale à Pyro.NameServer
        else:
            self.creeServeur("DestructionGalactique","Xavier")
            self.client.connect([clee for clee, valeur in self.client.getServers().items() if clee != "Pyro.NameServer"][0])
        self.modele.initPartie(0,self.client.getStartingInfo(),True)
        self.vue.displayMap(self.modele.map)
        self.vue.generateSpriteSet(self.modele.noJoueurLocal)
        self.vue.displayObject(self.modele.listeJoueur,[],self.modele.noJoueurLocal,self.modele.selection)
        self.vue.displayHUD()
        
        self.gameLoop()
        

    def gameLoop(self):
        #self.modele.gestion(self.client.pullAction()) #enlever pour test bouton dans la vue
        #self.client.pushAction(self.modele.dicAction2Server) #enlever pour test bouton dans la vue
        self.vue.displayObject(self.modele.listeJoueur,[],self.modele.noJoueurLocal,self.modele.selection)
        self.vue.root.after(24,self.gameLoop)

    def gererMouseClick(self,event):

        offset = self.vue.getSurfacePos()#Obtenir la position du canvas
        
        self.modele.clickPosx = event.x+offset[0]
        self.modele.clickPosy = event.y+offset[1]

    def gererMouseDrag(self, event):
        offset = self.vue.getSurfacePos()
        self.vue.displaySelection((self.modele.clickPosx,self.modele.clickPosy), event)

    def gererMouseRelease(self,event):
        self.vue.eraseSelection()
        offset = self.vue.getSurfacePos()#Obtenir la position du canvas
        self.modele.releasePosx = event.x+offset[0]
        self.modele.releasePosy = event.y+offset[1]
        self.modele.gererMouseRelease(event)

    def fermeture(self):
        if(self.serveur):
            self.serveur.close()
        self.vue.root.destroy()

if __name__ == "__main__":
    c = Controleur()
