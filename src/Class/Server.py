import Pyro4
from Pyro4 import core
import socket
from random import randint
import pickle
#from MyData import act
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
        self.nbPlayerReq =1     #nombre de joueur necessaire pour partir la partie
        self.highestRead =0     #le temps le plus recent lue
        self.highestDel = 0     #le temps le plus recent effacer
        self.client =[]         # la liste des client
        self.actions ={0:Actions(self.nbPlayerReq)} #la liste qui contient tous les evenements qui contiennent les actions
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
                self.client.append(InternalClient(num,0,nom))   #ajoute un client avec comme numero sa position dans le tableau
                print(self.client[num].nom+" est connecté!")
                """while (self.client.__len__() != self.nbPlayerReq):
                    time.sleep(1)    #tant que tout le monde n'est pas connecter on attend"""#Pourquoi faire attendre le client?
                return num           #retourne le numero donne
        except Exception as e:
            print(traceback.print_exc())    #code pour avoir le "FULL STACK TRACE" :D

    def sendAction(self,package):
        if self.highestRead >= len(self.actions):# si la dernierre action dans le dictionnaire(leur cle est leur temps) est lue on en ajoute une nouvelle
            self.actions[self.highestRead] = Actions(self.client.__len__())
        self.actions[self.highestRead].setAction(package,self.client.__len__()-1)# on ajoute le package representant l'action  a la derniere place du dictionnaire


    def readAction(self,num):
        #Note : Faire une Fonction Avec  +
        delagger =True     #si le temps entre le plus lent et celui qui veux lire l'action est trop grand, on le fait attendre
        while delagger:
            delagger =False
            for i in self.client:
                if i.temps+self.maxTempsDecalage < self.client[num].temps:
                    delagger =True
            if delagger:
                time.sleep(0.01)

        if self.client[num].temps-1 == self.highestDel:
            self.seekLowest()
            
        self.client[num].temps+=1     #augmente le temps du la personne qui veux les actions
        
        if self.highestRead < self.client[num].temps:     #sil est plus avancer dans le temps on enregistre son temps
            self.highestRead +=1
        return self.actions[self.client[num].temps-1]     # le -1 est la ,parce quon a augmenter le temps avant d'envoyer le reponse
    
    def seekLowest(self): # cherche le client qui est le plus en retard dans la lecture des evenement
        #on trouve le temps le plus bas et on l'enregistre
        Lowest = self.client[0].temps
        for i in self.client:
            if i.temps < Lowest:
                Lowest = i.temps

        if Lowest-1 > self.highestDel:
            if Lowest-1 in self.actions:         #on verifie s'il existe (jai tester on en a pas de besoin mais jeprefaire eviter de prendre des risque)
                del self.actions[(Lowest-1)]     # on enleve levenement avant du plus bas
                self.highestDel = Lowest

    def isGameStarted(self):
        return self.gameStarted

    def startGame(self):
        self.gameStarted = True

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
    def __init__(self, num, renommerCetteVariableSiQqUnSaitDeOuElleSort, nom):
        self.num = num
        self.renommerCetteVariableSiQqUnSaitDeOuElleSort = renommerCetteVariableSiQqUnSaitDeOuElleSort
        self.nom = nom



        
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
        ns.register(name=self.nomServeur, uri=self.uri, safe=True)

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
