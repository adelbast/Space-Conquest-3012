from Vue    import Vue
from Modele import Modele
from Class.AI import AI
from Class.Server import Server
from Class.Client import Client
from threading import Thread
import time,os

class Controleur:
    def __init__(self):
        
        self.modele = Modele(self)
        self.vue = Vue(self)

        self.modele.init_grid_Pathfinding(self)
        
        self.client = None
        self.serveur = None
        self.nomBatiment = None
        self.compteur = 0
        #Section Temporaire
        self.listeTemporaireDeClient = ["Xavier","Antoine","AI","Laurence","Arnaud","Francis","Alexandre","AI"]     
        self.leclient = 0    #changer le numero pour créé plusieur client
        self.choixServeur = False

        self.creeClient(self.listeTemporaireDeClient[self.leclient])#TODO
        self.serverLobby()#lorsque le menu sera fait, utiliser la fontion du bas plutôt que celle-ci
        #self.vue.afficherMenu()
        self.vue.root.mainloop()

        if(self.serveur):
            self.serveur.close()

    #Fonction qui crée le client local
    def creeClient(self,nom): 
        self.client = Client(nom)

    #Fonction qui crée le serveur. Un seul est nécéssaire par partie
    def creeServeur(self,nameServer, nomPartie, nomJoueur):
        self.serveur = Server(nameServer, nomPartie, nomJoueur) #Initialisation
        self.serveur.daemon = True
        self.serveur.start()    #Démarrage du serveur

    #Fait afficher le lobby de choix de serveur
    def serverLobby(self):
        if(not self.choixServeur):
            self.vue.removeAllDisplay()
            if(self.client.nameServer):
                self.vue.displayServers(self.client.getServers())#Affichage du lobby
            else:
                self.vue.displayServers({})
                t = Thread(target = self.client.findNameServer)
                t.daemon = True
                t.start()

            self.vue.root.after(5000,self.serverLobby)


    #Fonction qui permet d'entrer dans un Lobby et affiche le lobby de partie
    def joinLobby(self):
        selectedServer = self.vue.serverList.get(self.vue.serverList.curselection()[0])#Pour obtenir le serveur selectionne dans la listbox
        if(selectedServer):
            print("Connecting "+self.client.nom+" to "+selectedServer)
            self.client.connect(selectedServer)#Se connecter au serveur
            self.choixServeur = True
            self.playerLobby()

    #Creation d'un nouveau serveur et affiche le lobby de partie
    def createLobby(self):
        unNomDePartie   = "Boom"#TODO
        self.creeServeur(self.client.nameServer, unNomDePartie, self.client.nom)
        self.client.findNameServer()
        self.client.connect(unNomDePartie)
        self.choixServeur = True
        self.playerLobby()
        

    def playerLobby(self):
        self.vue.removeAllDisplay()
        self.vue.displayLobby(self.client.proxy.getClients())
        if(not self.modele.listeJoueur):
            if(self.client.proxy.isGameStarted()):
                self.vue.removeAllDisplay()
                self.lancerPartie()
            else:
                self.vue.root.after(300,self.playerLobby)
        else:self.vue.removeAllDisplay()


    #Retourne si le client est aussi le host
    def isHost(self):
        if(self.serveur): return True
        return False

    #Fonction qui démarre la partie
    def lancerPartie(self):
        self.client.proxy.startGame()
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
        reception = None
        #print("\n----------------------------\n",self.compteur, "ENVOIE : ", self.packAction2Server())
        self.client.pushAction( self.packAction2Server() )
        self.modele.dicAction2Server.clear()
        while not reception:
            reception = self.client.pullAction()
            #print("RECOIT : ", reception)
        self.modele.gestion( reception )
        """if(self.vue.etatCreation==True):
            self.vue.dessinerShadowBatiment()"""
        self.modele.actualiser()
        self.vue.displayRessources(self.modele.listeJoueur[self.modele.noJoueurLocal].listeRessource)
        self.vue.displayObject(self.modele.listeJoueur,[],self.modele.noJoueurLocal,self.modele.selection)
        self.compteur+=1
        self.vue.root.after(20,self.gameLoop)

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
        self.modele.gererMouseRelease(event,self.vue.etatCreation) # A AJOUTER!!!!!!
        try:
            self.vue.displayInfoUnit(self.modele.selection[0])
        except Exception:
            print("Pas de selection!")
        self.vue.etatCreation = False

    def creationBatiment(self,nom):  # A AJOUTER!!!!!!
        self.nomBatiment = nom
        self.vue.etatCreation = True


if __name__ == "__main__":
    c = Controleur()
