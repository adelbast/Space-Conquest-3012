from Vue    import Vue
from Modele import Modele
from Class.AI import AI
from Class.Server import Server
from Class.Client import Client
import time,os
import traceback

class Controleur:
    def __init__(self):
        self.modele         = Modele(self)
        self.vue            = Vue(self)

        self.modele.init_grid_Pathfinding(self)
        self.client = None
        self.serveur = None
        self.nomBatiment = None
        self.infoCreation = None
        self.etatCreation = None
        self.compteur = 0
        self.afterID = None
        #Section Temporaire

        
        self.client = Client()
        self.initServerLobby()#lorsque le menu sera fait, utiliser la fontion du bas plutôt que celle-ci
        #self.vue.afficherMenu()
        self.vue.root.mainloop()
        self.closeGame()


    #Fonction qui crée le serveur. Un seul est nécéssaire par partie
    def creeServeur(self,nameServer, nomPartie, nomJoueur):
        self.serveur = Server(nameServer, nomPartie, nomJoueur) #Initialisation
        self.serveur.daemon = True
        self.serveur.start()    #Démarrage du serveur

    def initServerLobby(self):
        self.vue.removeGridDisplay()
        self.vue.displayServers([])
        self.serverLobby()

    #Fait afficher le lobby de choix de serveur
    def serverLobby(self):
        if(self.client.nameServer):
            try:
                self.vue.refreshServers(self.client.getServers())#Affichage du lobby
            except:
                print("oups le nameServer ne répond plus...")
                self.client.nameServer = None
        else:
            self.vue.refreshServers({})
            self.client.findNameServerThread()

        self.afterID = self.vue.root.after(5000,self.serverLobby)


    #Fonction qui permet d'entrer dans un Lobby et affiche le lobby de partie
    def joinLobby(self):
        selectedServer = self.vue.serverList.get(self.vue.serverList.curselection()[0])#Pour obtenir le serveur selectionne dans la listbox
        if(selectedServer):
            self.vue.root.after_cancel(self.afterID)
            self.client.nom = self.vue.entreClient.get()
            print("Connecting "+self.client.nom+" to "+selectedServer)
            self.client.connect(selectedServer)#Se connecter au serveur
            self.vue.removeGridDisplay()
            self.vue.displayLobby(self.serveur)
            self.playerLobby()

    #Creation d'un nouveau serveur et affiche le lobby de partie
    def createLobby(self):
        self.vue.root.after_cancel(self.afterID)
        self.client.nom = self.vue.entreClient.get()
        self.creeServeur(self.client.nameServer, self.vue.entreServeur.get(), self.client.nom)
        self.client.findNameServer()
        self.client.connect(self.vue.entreServeur.get())
        self.vue.removeGridDisplay()
        self.vue.displayLobby(self.serveur)
        self.playerLobby()
        

    def playerLobby(self):
        self.vue.refreshLobby(self.client.proxy.getStartingInfo())
        if(self.client.proxy.isGameStarted()):
            self.lancerPartie()
        else:
            if(self.serveur):
                self.client.setCpuClient( int(self.vue.spinBox.get()) )  #Afin que tous les joueurs puisse afficher les joueur IA dans leur lobby
                if(not self.client.isNameServerAlive()):
                    self.server.startNameServer()
            self.afterID = self.vue.root.after(300,self.playerLobby)


    #Retourne si le client est aussi le host
    def isHost(self):
        if(self.serveur): return True
        return False

    #Fonction qui démarre la partie
    def lancerPartie(self):
        self.vue.root.after_cancel(self.afterID)
        if(self.serveur):
            self.serveur.removeServerBroadcast()
            self.client.proxy.startGame()
        self.vue.removeGridDisplay()
        os.system('cls')
        print(self.client.noJoueur)
        self.modele.initPartie(self.client.noJoueur,self.client.getStartingInfo(),self.isHost())
        self.client.setCpuClient(self.modele.getAIcount())
        self.vue.displayMap(self.modele.map)
        self.vue.generateSpriteSet(self.modele.noJoueurLocal)
        self.vue.displayObject(self.modele.listeJoueur,[],self.modele.noJoueurLocal,self.modele.selection)
        self.vue.displayHUD()
        self.vue.displayRessources(self.modele.listeJoueur[self.modele.noJoueurLocal].listeRessource)
        
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
        if(self.compteur%5):
            reception = None
            #print("\n----------------------------\n",self.compteur, "ENVOIE : ", self.packAction2Server())
            self.client.pushAction( self.packAction2Server() )
            self.modele.dicAction2Server.clear()
            while not reception:
                reception = self.client.pullAction()
                if(not reception):
                    print("laaaaag!")
            self.modele.gestion( reception )
        """if(self.vue.etatCreation==True):
            self.vue.dessinerShadowBatiment()"""
        self.modele.actualiser()
        self.vue.displayRessources(self.modele.listeJoueur[self.modele.noJoueurLocal].listeRessource)
        self.vue.displayObject(self.modele.listeJoueur,[],self.modele.noJoueurLocal,self.modele.selection)
        self.compteur+=1
        self.vue.root.after(50,self.gameLoop) #monter a 50 pour tester le pathfinding plus facilement peux descendre si ca vs derange

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
        self.modele.gererMouseRelease(event,self.etatCreation, self.infoCreation) # A AJOUTER!!!!!!
        try:
            self.vue.displayInfoUnit(self.modele.selection[0],self.modele.noJoueurLocal)
        except Exception:
            self.vue.hud.delete("infos")
            self.vue.hud.delete("button")
            print("Pas de selection!")
        self.vue.etatCreation = False

    def creationBatiment(self,nom):  # A AJOUTER!!!!!!
        self.nomBatiment = nom
        self.vue.etatCreation = True

    def getSizeBatiment(self, batiment):
        return self.modele.dictBatiment[batiment]

    def closeGame(self):
        if(self.client and self.client.proxy):
            self.client.disconnect()

        if(self.serveur):
            self.serveur.close()


    

if __name__ == "__main__":
    c = Controleur()
