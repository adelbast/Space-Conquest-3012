import Pyro4
from Pyro4 import core
import socket
from random import randint
import pickle
#from MyData import act
import time

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

    def ping(self):
        print("ping")
        return True
        
    def nbPlayer(self):
        return self.client.__len__()
        
    def seConnecter(self):  #Signale au serveur quon est connecter
        if self.client.__len__() != self.nbPlayerReq: # on ne peut se connecter que si la limite des joueur n'est pas depasser
            num = self.client.__len__()      # le numero  que le client va recevoir est sa position dans le tableau des clients
            self.client.append(client(self.client.__len__(),0))    #ajoute un client avec comme numero sa position dans le tableau
            while (self.client.__len__() != self.nbPlayerReq):    #ajoute un client avec comme numero sa position dans le tableau
                time.sleep(1)    #tant que tout le monde n'est pas connecter on attend
            return (num)        #retourne le numero donne

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

        
class Server(object):
    def __init__(self, nomServeur = "SpaceConquest3012",nomJoueurHost = "xavier", test = False):
        self.nomServeur = nomServeur
        self.uri = None        #adresse utiliser par pyro pour se connecter au objets distants
        self.port = 9992
        self.ip = socket.gethostbyname(socket.gethostname())                        #retourne le IP
        self.serverObject = ServerObject(nomServeur, nomJoueurHost, self.ip, test)  #objet distant

        if(test):
            self.start(self.nomServeur)

    def start(self,nomServeur): #lance le serveur de jeu
        daemon=Pyro4.Daemon(host=self.ip,port=self.port)
        self.uri=daemon.register(self.serverObject,nomServeur) #"PYRO:SpaceConquest3012@192.168.100.2:9992" Uri ressemble à quelque chose comme ça
        print(self.uri)
        self.startBroadcast()
        print("Pret!")
        daemon.requestLoop()

    def startBroadcast(self):    #lance le serveur qui broadcast les infos du serveur de jeu sur le réseau
        bS = Pyro4.naming.BroadcastServer(nsUri = core.URI(self.uri), bcport = self.port+1)#création de l'objet serveur (self.port+1 car ""socket"" ne peut pas binder deux fois le même socket)
        bS.runInThread()        #lance le serveur de broadcast dans un autre thread

    def stopBroadcast(self):
        bS.close()
        
class Actions(object): 
    def __init__(self, nbClients):
        self.action = []
        
        for i in range(nbClients):
            self.action.append([])#chacune des actions prises chaque joueur
           
    def setAction(self,action,num):
        self.action[num].append(action)


if __name__ == '__main__':
    s=Server(test = True)
