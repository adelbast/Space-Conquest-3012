import Pyro4
from Pyro4 import core
import socket
from random import randint
import pickle
import time
from threading import Thread
import traceback
import sys

VERSION = "1.0"

#Pyro4.config.SERIALIZER = 'pickle'
#Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

class ServerObject(object):
    def __init__(self,nomServeur,nomJoueurHost,ip, test):
        self.test = test
        self.nomServeur = nomServeur
        self.nomJoueurHost = nomJoueurHost
        self.ip = ip
        self.highestRead = 0        #le temps le plus recent lue
        self.client = []            #la liste des client
        self.actions = []           #[(temp,[package joueur 0][package joueur 1][][][])]la liste qui contient tous les evenements qui contiennent les actions
        self.maxTempsDecalage = 8
        self.gameStarted = False

    def ping(self):
        print("ping")
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
        except Exception as e:
            print(traceback.print_exc())    #code pour avoir le "FULL STACK TRACE" :D
            
    def sendAction(self,listePackage):
        try:
            for i in listePackage:
                num =       i[0]
                package =   i[1]
                if self.highestRead >= len(self.actions):           # si la dernière action dans le dictionnaire(leur cle est leur temps) est lue on en ajoute une nouvelle
                    uneListe = ["VOID"]*len(self.client)
                    self.actions.append( (self.highestRead, uneListe) )
                    print(self.actions[len(self.actions)-1][1])
                self.actions[len(self.actions)-1][1][num] = package    # on ajoute le package representant l'action  a la derniere place du dictionnaire
                self.actions[len(self.actions)-1][1][num]
        except:
            print(traceback.print_exc())

    def readAction(self,num):
        try:
            #Note : Faire une Fonction Avec  +
            delagger =True     #si le temps entre le plus lent et celui qui veux lire l'action est trop grand, on le fait attendre
            while delagger:
                delagger =False
                for i in self.client:
                    if i.temps+self.maxTempsDecalage < self.client[num].temps:
                        delagger =True
                if delagger:
                    time.sleep(0.01)

            if self.client[num].temps-1 == self.actions[0][0]:
                self.deleteLowest()
                
            self.client[num].temps+=1     #augmente le temps de la personne qui veux les actions
            
            if self.highestRead <= self.client[num].temps:     #sil est plus avancer dans le temps on enregistre son temps
                self.highestRead = self.client[num].temps

            print(self.highestRead-(self.client[num].temps-1), len(self.actions))

            return self.actions[self.highestRead-(self.client[num].temps)][1]  # le -1 est la ,parce quon a augmenter le temps avant d'envoyer le reponse
        except:
            print(traceback.print_exc())
    
    def deleteLowest(self): # cherche le client qui est le plus en retard dans la lecture des evenement
        try:
            #on trouve le temps le plus bas et on l'enregistre
            lowest = self.client[0].temps
            for i in self.client:
                if i.temps < lowest:
                    lowest = i.temps

            if lowest > self.actions[0][0]: #[element en orde chronologique][le temps de cette action]
                del self.actions[0]     # on enleve levenement avant le plus bas
        except:
            print(traceback.print_exc())

    #Getter qui retourne si la partie est commancé
    def isGameStarted(self):
        return self.gameStarted

    #Fonction qui set la partie à l'état Started = TRUE
    def startGame(self):
        self.gameStarted = True

    #Getter qui retourne la liste du nom des client connecté au serveur
    def getStartingInfo(self):
        return [client.nom for client in self.client]

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



class InternalClient(object):
    def __init__(self, num, nom):
        self.num = num
        self.nom = nom
        self.temps = 0



        
class Server(Thread):
    def __init__(self, nomServeur = "SpaceConquest3012", nomJoueurHost = "xavier", test = False):
        super(Server, self).__init__()
        self.nomServeur = nomServeur
        self.uri = None        #adresse utiliser par pyro pour se connecter au objets distants
        self.port = 9992
        self.ip = socket.gethostbyname(socket.gethostname())                        #retourne le IP
        self.serverObject = ServerObject(nomServeur, nomJoueurHost, self.ip, test)  #objet distant
        self.nameServerThread = None

        if(test):
            self.run()

    def run(self): #lance le serveur de jeu
        print("Création du serveur en cours...")
        daemon=Pyro4.Daemon(host=self.ip,port=self.port)
        self.uri=daemon.register(self.serverObject, self.nomServeur) #"PYRO:SpaceConquest3012@192.168.100.2:9992" Uri ressemble à quelque chose comme ça
        print(self.uri)
        self.startNameServer()
        print("Pret!")
        daemon.requestLoop()

    def startNameServer(self):      #lance le serveur qui broadcast les infos du serveur de jeu sur le réseau
        self.nameServerThread = Thread(target = Pyro4.naming.startNSloop,args=(self.ip, None, True)) #création de l'objet serveur
        self.nameServerThread.start()    #lance le nameServeur dans un thread
        ns = Pyro4.naming.locateNS(host=self.ip)
        ns.register(name=self.nomServeur, uri=self.uri)

    def close(self):
        sys.exit()
 


class Actions(object): 
    def __init__(self, nbClients):
        self.action = []
        
        for i in range(nbClients):
            self.action.append([])#chacune des actions prises chaque joueur
           
    def setAction(self,action,num):
        self.action[num].append(action)


if __name__ == '__main__':
    s=Server(test = True)
