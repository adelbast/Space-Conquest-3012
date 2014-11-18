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
        self.client       = None
        self.serveur      = None
        self.nomBatiment  = None
        self.infoCreation = None
        self.etatCreation = None
        self.tempsDebut   = None
        self.compteur     = 0
        self.afterID      = None
        #Section Temporaire
        self.verbose = False # //Mettre verbose a True pour plus de print venant du serveur
        
        self.client = Client()
        self.initServerLobby()#lorsque le menu sera fait, utiliser la fontion du bas plutôt que celle-ci
        #self.vue.afficherMenu()
        self.vue.root.mainloop()
        self.closeGame()


    #Fonction qui crée le serveur. Un seul est nécéssaire par partie
    def creeServeur(self,nameServer, nomPartie, nomJoueur):
        self.serveur = Server(nameServer, nomPartie, nomJoueur, test = self.verbose) #Initialisation 
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
        self.tempsDebut = time.time()
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
        if(self.verbose):print("\n----------------------------\n",self.compteur, "ENVOIE : ", self.packAction2Server())
        self.client.pushAction( self.packAction2Server() )
        self.modele.dicAction2Server.clear()
        while not reception:
            reception = self.client.pullAction()
            if(self.verbose):print("RECOIE : ", reception)
            if(not reception):
                time.sleep(0.01)
                #print("laaaaag!")
        self.modele.gestion( reception )
        """if(self.vue.etatCreation==True):
            self.vue.dessinerShadowBatiment()"""
        self.modele.actualiser()
        self.vue.displayRessources(self.modele.listeJoueur[self.modele.noJoueurLocal].listeRessource)
        self.vue.displayObject(self.modele.listeJoueur,[],self.modele.noJoueurLocal,self.modele.selection)
        #self.vue.displayNodes(self.modele.cutNodes)
        self.compteur+=1
        self.vue.root.after(24,self.gameLoop) #monter a 50 pour tester le pathfinding plus facilement peux descendre si ca vs derange

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
        

    #Validation de la spawning position
    def spawnUnit(self, unitName):

        validateSpawn = False
        
        pX = self.modele.selection[0].position[0] - (self.modele.dictUnit[unitName][7] + self.modele.selection[0].size/2)
        pY = self.modele.selection[0].position[1] - (self.modele.dictUnit[unitName][7] + self.modele.selection[0].size/2)

        #Nombre de fois qu'il faut passer dans la boucle Ex : 6 options = 0,1,2,3,4,5
        size = self.modele.dictUnit[unitName][7]
        
        numOption = (self.modele.selection[0].size/size)+1 #Le +1 est en fait -1 + 2, parce qu'il faut aller un cube en haut (-1) et il faut rajouter 2 pour aller 1 cube en bas

        #Compteurs
        compteurX = 0
        compteurY = 0

        #Regarde si la case choisit est valide
        if(self.modele.getNode(int(pX/32), int(pY/32)).voisins is not None):
                
            for _,unit in self.modele.listeJoueur[self.modele.noJoueurLocal].listeUnite.items():
                node1, node2 = self.modele.getNode(int(pX/32), int(pY/32)), self.modele.getNode(int(unit.position[0]/32), int(unit.position[1]/32))
                    
                if(node1.x == node2.x and node1.y == node2.y):
                    validateSpawn = False
                    break
                else:
                    validateSpawn = True
        

        while(not validateSpawn):

            #En partant du coin en haut a gauche du batiment
            if(compteurX == 0 and compteurY < numOption): 
                pY = pY + size
                compteurY += 1
                
            #En partant du coin en bas a gauche du batiment
            elif (compteurX < numOption and compteurY == numOption):
                pX = pX + size
                compteurX += 1
                
            #En partant du coin en bas a gauche du batiment
            elif(compteurX == numOption and compteurY > 0):
                pY = pY - size
                compteurY -= 1
                
            #En partant du coin en haut a droite
            elif(compteurY == 0 and compteurX > 1):
                pX = pX - size
                compteurX -= 1

            #Si on a fnit de regarder toutes les positions posibles
            elif(compteurX == 1 and compteurY == 0):
                numOption += 2
                pX = pX - size*2
                pY = pY - size
                compteurX = 0
                compteurY = 0
                
            #Regarde si la case choisit est valide
            if(self.modele.getNode(int(pX/32), int(pY/32)).voisins is not None):
                
                for _,unit in self.modele.listeJoueur[self.modele.noJoueurLocal].listeUnite.items():
                    node1, node2 = self.modele.getNode(int(pX/32), int(pY/32)), self.modele.getNode(int(unit.position[0]/32), int(unit.position[1]/32))
                    
                    if(node1.x == node2.x and node1.y == node2.y):
                        validateSpawn = False
                        break
                    else:
                        validateSpawn = True

              
        if('NewUnit' not in self.modele.dicAction2Server):  
            self.modele.dicAction2Server['NewUnit'] = []
            
        self.modele.dicAction2Server['NewUnit'].append((unitName, (pX,pY)))

    def moveUnitWithMinimap(self, event):
        #print("Avant : ",event.x, event.y)
        event.x = event.x * (len(self.modele.map.map[0])*64)/self.vue.miniMapW
        event.y = event.y * (len(self.modele.map.map)*64)/self.vue.miniMapH
        self.modele.releasePosx = event.x
        self.modele.releasePosy = event.y
        #print("Apres : ",event.x, event.y)
        self.modele.gererMouseRelease(event,self.etatCreation, self.infoCreation)
        
        

    def getSizeBatiment(self, batiment):
        return self.modele.dictBatiment[batiment]

    def closeGame(self):
        if(self.client and self.client.proxy):
            self.client.disconnect()

        if(self.serveur):
            self.serveur.close()


    

if __name__ == "__main__":
    c = Controleur()
