from Vue    import Vue
from Modele import Modele
from Class.AI import AI
from Class.Server import Server
from Class.Client import Client
from threading import Thread
import time,os

class Controleur:
    def __init__(self):
        self.modele = Modele()
        self.vue = Vue(self)
        self.client = None
        self.serveur = None
        
        #Section Temporaire
        self.listeTemporaireDeClient = ["Xavier","Antoine","AI","Laurence","Arnaud","Francis","Alexandre","AI"]
        self.leclient = 0    #changer le numero pour créé plusieur client
        self.autoCreateAndEnterLobby()#lorsque le menu sera fait, utiliser la fontion du bas plutôt que celle-ci
        self.lobbyLoop()
        #self.vue.afficherMenu()

        self.vue.root.mainloop()
        
        if(self.serveur):
            self.serveur.close()

    #Fonction qui crée le client local
    def creeClient(self,nom): 
        self.client = Client(nom)

    #Fonction qui crée le serveur. Un seul est nécéssaire par partie
    def creeServeur(self,nomPartie,nomJoueur):      
        self.serveur = Server(nomPartie,nomJoueur) #Inicialisation
        self.serveur.daemon = True
        self.serveur.start()    #Démarrage du serveur

    #TEMPORAIRE : Fonction qui crée le client local et un serveur s'il n'y en a pas déjà un sur le réseau
    def autoCreateAndEnterLobby(self):
        print(self.listeTemporaireDeClient[self.leclient])
        self.creeClient(self.listeTemporaireDeClient[self.leclient])
        if(not self.client.nameServer):
            self.creeServeur("DestructionGalactique","Xavier")
        self.client.connect([clee for clee, valeur in self.client.getServers().items() if clee != "Pyro.NameServer"][0])#Tente de se connecter sur la premiere clee retourner par getServers() qui n'est pas égale à Pyro.NameServer

    #Contenu TEMPORAIRE : Fonction qui permet d'attendre que le host décide de démarrer la partie. (Pour attendre que les joueurs soient connectés)
    def lobbyLoop(self):
        if(self.serveur):
            thread = Thread(target = self.inputThread)
            thread.start()
        while(not self.client.proxy.isGameStarted()):
            time.sleep(0.5)
            #os.system('cls')
            print(self.client.getStartingInfo(), "Si le serveur est sur cette machine, pesez sur Enter pour débuter la partie ou attendre les autres joueurs")
        self.lancerPartie()

    #Petite fonction qui attend que le host pèse sur ENTER (lancé comme thread dans lobbyLoop() )
    def inputThread(self):
        input()
        self.client.proxy.startGame()

    #Retourne si le client est aussi le host
    def isHost(self):
        if(self.serveur): return True
        return False

    #Fonction qui démarre la partie
    def lancerPartie(self):
        os.system('cls')
        print(self.client.noJoueur)
        self.modele.initPartie(self.client.noJoueur,self.client.getStartingInfo(),self.isHost())
        self.vue.displayMap(self.modele.map)
        self.vue.generateSpriteSet(self.modele.noJoueurLocal)
        self.vue.displayObject(self.modele.listeJoueur,[],self.modele.noJoueurLocal,self.modele.selection)
        self.vue.displayHUD()
        
        self.gameLoop()
    
    def packAction2Server(self):
    	retour = []
        retour.append((self.modele.noJoueurLocal,self.modele.dicAction2Server))
    	if(self.serveur):
    		for joueur in self.modele.listeJoueur:
    			if isinstance(joueur,AI):
    				retour.append((joueur.noJoueur, joueur.dictionaireAction))
    	return retour

    def gameLoop(self):
        self.modele.gestion(self.client.pullAction()) #enlever pour test bouton dans la vue
        self.client.pushAction( self.packAction2Server() ) #enlever pour test bouton dans la vue

        self.modele.bougerUnits()
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
        try:
            self.vue.displayInfoUnit(self.modele.selection[0])
        except Exception:
            print("Pas de selection!")

    

if __name__ == "__main__":
    c = Controleur()
