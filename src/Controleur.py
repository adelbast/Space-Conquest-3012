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
        self.nomBatiment = None
        self.compteur = 0
        #Section Temporaire
        self.listeTemporaireDeClient = ["Xavier","Antoine","AI","Laurence","Arnaud","Francis","Alexandre","AI"]
        self.leclient = 1    #changer le numero pour créé plusieur client
        self.autoCreateAndEnterLobby()#lorsque le menu sera fait, utiliser la fontion du bas plutôt que celle-ci
        self.serverLobby()
        #self.vue.afficherMenu()

        self.vue.root.mainloop()
        
        if(self.serveur):
            self.serveur.close()

    #Fonction qui crée le client local
    def creeClient(self,nom): 
        self.client = Client(nom)

    #Fonction qui permet de stopper le after de la recherche de serveur
    def joinLobby(self):

        #Pour obtenir le serveur selectionne dans la listbox
        selectedServer = self.vue.serverList.get(self.vue.serverList.curselection()[0])

        print("Connecting "+self.client.nom+" to "+selectedServer)

        #Se connecter au serveur
        self.client.connect(selectedServer)

        #Remove le display du lobby
        for child in self.vue.root.winfo_children():
            child.place_forget()

        self.lancerPartie()

    #Fonction qui crée le serveur. Un seul est nécéssaire par partie
    def creeServeur(self,nomPartie,nomJoueur):      
        self.serveur = Server(nomPartie,nomJoueur) #Inicialisation
        self.serveur.daemon = True
        self.serveur.start()    #Démarrage du serveur

    #TEMPORAIRE : Fonction qui crée le client local et un serveur s'il n'y en a pas déjà un sur le réseau
    def autoCreateAndEnterLobby(self):
        self.creeClient(self.listeTemporaireDeClient[self.leclient])
        if(not self.client.nameServer):
            self.creeServeur("DestructionGalactique","Xavier")

    #Contenu TEMPORAIRE : Fonction qui permet d'attendre que le host décide de démarrer la partie. (Pour attendre que les joueurs soient connectés)
    def serverLobby(self):

        print("Refreshed")
        
        #Affichage du lobby
        self.vue.displayServerLobby(self.client.getServers())
        
        """if(self.serveur):
            thread = Thread(target = self.inputThread)
            thread.start()
        while(not self.client.proxy.isGameStarted()):
            time.sleep(0.5)
            #os.system('cls') 
            print(self.client.getStartingInfo(), "Si le serveur est sur cette machine, pesez sur Enter pour débuter la partie ou attendre les autres joueurs")
        self.lancerPartie()"""

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
        #self.modele.initPartie(self.client.noJoueur,self.client.getStartingInfo(),self.isHost())
        self.modele.initPartie(self.client.noJoueur,["Xavier","AI"],self.isHost())
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
        print(self.compteur, "ENVOIE : ", self.packAction2Server())
        self.client.pushAction( self.packAction2Server() )
        self.modele.dicAction2Server.clear()
        while not reception:
            reception = self.client.pullAction()
            print("RECOIT : ", reception, end="\n\n\n\n")
        self.modele.gestion( val )
        """if(self.vue.etatCreation==True):
            self.vue.dessinerShadowBatiment()"""
        self.modele.actualiser()
        self.vue.displayRessources(self.modele.listeJoueur[self.modele.noJoueurLocal].listeRessource)
        self.vue.displayObject(self.modele.listeJoueur,[],self.modele.noJoueurLocal,self.modele.selection)
        self.compteur+=1
        self.vue.root.after(1000,self.gameLoop)

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
