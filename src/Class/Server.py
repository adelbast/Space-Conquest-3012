import Pyro4
from Pyro4 import core
import socket
from random import randint
import time
from threading import Thread, Lock
import traceback
import sys

VERSION = "1.0"

class ServerObject(object):
    def __init__(self,nomServeur,nomJoueurHost,ip, test):
        self.test = test
        self.nomServeur = nomServeur
        self.nomJoueurHost = nomJoueurHost
        self.ip = ip
        self.client = []            #la liste des client
        self.cpuClient = 0
        self.actions = {}           # {                                 la liste qui contient tous les evenements qui contiennent les actions
                                    #   temp 1,[ [package joueur 0]
                                    #            [package joueur 1]
                                    #            [package joueur 2] ]
                                    #   temp 2,[ [package joueur 0]
                                    #            [package joueur 1]
                                    #            [package joueur 2] ]
                                    #   temp 3,[ [package joueur 0]
                                    #            [package joueur 1]
                                    #            [package joueur 2] ]
                                    # }
        self.maxTempsDecalage = 8
        self.gameStarted = False
        self.pastTime = None#time.time()

    def ping(self):
        if(self.test):print("ping")
        return True
        
    def nbPlayer(self):
        return self.client.__len__()
        
    def seConnecter(self,nom):  #Signale au serveur quon est connecter
        try:
            if not self.gameStarted:   # on ne peut se connecter que si la limite des joueur n'est pas depasser et si la partie n'est pas commencé
                num = self.client.__len__()                 # le numero  que le client va recevoir est sa position dans le tableau des clients
                self.client.append(InternalClient(num,nom))   #ajoute un client avec comme numero sa position dans le tableau
                print(self.client[num].nom+" est connecté!")
                return num           #retourne le numero donne
            else:
                return -1
        except Exception as e:
            print(traceback.print_exc())    #code pour avoir le "FULL STACK TRACE" :D

    def seDeconnecter(self, noClient):
        self.client[noClient].estConnecte = False
        print(self.client[noClient].nom + " c'est déconnecté !!!!")
            
    def sendAction(self,listePackage):
        try:
            for i in listePackage:
                num =       i[0]
                package =   i[1]
                highestRead = self.getHighestRead()
                
                if not self.actions or highestRead >= self.getHighestActionTime():
                    if(self.test):print("Ajout d'un temps d'action")
                    uneListe = [None]*(len(self.client)+self.cpuClient)
                    self.actions[highestRead+1] = uneListe  #+1 pour mettre cette action dans le future
                
                #print(self.actions[len(self.actions)-1][1])
                self.actions[self.getHighestActionTime()][num] = package     # on ajoute le package representant l'action  a la derniere place du dictionnaire
                if(self.test):print("action Sauvegarder")

        except:
            print(traceback.print_exc())

    def readAction(self,num):
        try:
            for i in self.client:
                if i.estConnecte and i.temps+self.maxTempsDecalage < self.client[num].temps:
                    return None
            if(num == 0 and time.time() - self.pastTime  > 3 ):
                self.deleteLowest()
                self.pastTime = time.time()
            self.client[num].temps+=1     #augmente le temps de la personne qui veux les actions
            try:
                return self.actions[self.client[num].temps-1]
            except KeyError:
                return [None]*(len(self.client)+self.cpuClient)#utile pour le premier tour de boucle
        except:
            print(traceback.print_exc())
    

    def getHighestRead(self):
        return max([c.temps for c in self.client])

    def getLowestRead(self):
        return min([c.temps for c in self.client if c.estConnecte])

    def getActionDeleteList(self):
        lowRead = self.getLowestRead()
        return [clee for clee in self.actions if clee < lowRead]

    def getLowestActionTime(self):
        return min([clee for clee in self.actions])

    def getHighestActionTime(self):
        return max([clee for clee in self.actions])

    def deleteLowest(self): # cherche le client qui est le plus en retard dans la lecture des evenement
        for clee in self.getActionDeleteList():
            try:
                if(self.test):print("________________________________Suppression",self.actions[clee],clee)
                del self.actions[clee]     # on enleve levenement le plus bas
            except KeyError:
                print(traceback.print_exc())

    #Getter qui retourne si la partie est commancé
    def isGameStarted(self):
        return self.gameStarted

    #Fonction qui set la partie à l'état Started = TRUE
    def startGame(self):
        self.gameStarted = True
        self.pastTime = time.time()

    #Getter qui retourne la liste du nom des client connecté au serveur
    def getStartingInfo(self):
        return [client.nom for client in self.client]+["AI" for _ in range(self.cpuClient)]

    def setCpuClient(self,nombreDeAI):
        self.cpuClient = nombreDeAI

    def getInfo(self):
        global VERSION
        info = {#dictionaire d'info sur le serveur
            "NAME":self.nom,
            "IP":self.ip,
            "VERSION": VERSION,
            "DEBUG":test,
            "NB_CLIENT":len(self.client)
        }
        return info
        

    def getNomServeur(self):
        return self.nomServeur


class InternalClient(object):
    def __init__(self, num, nom):
        self.num = num
        self.nom = nom
        self.temps = 0
        self.estConnecte = True



        
class Server(Thread):
    def __init__(self, ns, nomServeur = "SpaceConquest3012", nomJoueurHost = "xavier", test = False, standAlone = False):
        super(Server, self).__init__()
        self.isReady = False
        self.nomServeur = nomServeur
        self.uri = None        #adresse utiliser par pyro pour se connecter au objets distants
        self.ip = socket.gethostbyname(socket.gethostname())                        #retourne le IP
        self.serverObject = ServerObject(nomServeur, nomJoueurHost, self.ip, test)  #objet distant
        self.nameServerThread = None
        self.nameServer = ns
        if(standAlone):
            self.run()


    def run(self): #lance le serveur de jeu
        print("Création du serveur en cours...")
        daemon=Pyro4.Daemon(host=self.ip)
        self.uri=daemon.register(self.serverObject, self.nomServeur) #"PYRO:SpaceConquest3012@192.168.100.2:9992" Uri ressemble à quelque chose comme ça
        print(self.uri)
        if(self.nameServer):
            self.nameServer.register(name=self.nomServeur, uri=self.uri)
        else:
            self.startNameServer()
        print("Pret!")
        daemon.requestLoop()

    def startNameServer(self):      #lance le serveur qui broadcast les infos du serveur de jeu sur le réseau
        try:
            self.nameServerThread = Thread(target = Pyro4.naming.startNSloop,args=(self.ip, None, True)) #création de l'objet serveur
            self.nameServerThread.start()    #lance le nameServeur dans un thread
            Pyro4.naming.locateNS(host=self.ip).register(name=self.nomServeur, uri=self.uri)
        except:
            print(traceback.print_exc())
        
    def removeServerBroadcast(self):
        if(self.nameServer):
            self.nameServer.remove(self.nomServeur)

    def close(self):
        if(self.nameServer):
            self.removeServerBroadcast()
        sys.exit()


if __name__ == '__main__':
    s=Server(ns = None, nomServeur = "test", nomJoueurHost = "bob", test = True, standAlone = True)
