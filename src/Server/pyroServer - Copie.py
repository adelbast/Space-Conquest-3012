# -*- coding: iso-8859-1 -*-
import Pyro4
from random import randint
import pickle
import time

#Pyro4.config.SERIALIZER = 'pickle'
#Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

class client(object):
    def __init__(self,num,temps):
        self.num= num
        self.temps = temps#represente ou il est rendu dans sa lecture des evenements
        

class server(object):
    def __init__(self):
        self.nbPlayerReq = 2 #nombre de joueur necessaire pour partir la partie
        self.highestRead =0 #le temps le plus recent lue
        self.highestDel = 0 #le temps le plus recent effacer
        self.client =[] # la liste des client
        self.actions ={0:act.actions(self.nbPlayerReq)} #la liste qui comptien tout les evenements qui comptienne les actions
        self.maxTempsDecalage = 8

        
    def nbPlayer(self):
        return self.client.__len__()
        
    def seConnecter(self):  #Signale au serveur quon est connecter
        if self.client.__len__() != self.nbPlayerReq: # on ne peut se connecter que si la limite des joueur n'est pas depasser
            num = self.client.__len__()  # le numero  que le client va recevoir est sa position dans le tableau des clients
            self.client.append(client(self.client.__len__(),0))#ajoute un client avec comme numero sa position dans le tableau
            while (self.client.__len__() != self.nbPlayerReq):#ajoute un client avec comme numero sa position dans le tableau
                time.sleep(1)#tant que tout le monde n'est pas connecter on attend
            return (num)#retourne le numero donne

    def sendAction(self,package):
        if self.highestRead >= len(self.actions):# si la dernierre action dans le dictionnaire(leur cle est leur temps) est lue on en ajoute une nouvelle
            self.actions[self.highestRead] = act.actions(self.client.__len__())
        self.actions[self.highestRead].setAction(package,self.client.__len__()-1)# on ajoute le package representant l'action  a la derniere place du dictionnaire


    def readAction(self,num):
        #Note : Faire une Fonction Avec  +
        delagger =True#si le temps entre le plus lent et celui qui veux lire l'action est trop grand, on le fait attendre
        while delagger:
            delagger =False
            for i in self.client:
                if i.temps+self.maxTempsDecalage < self.client[num].temps:
                    delagger =True
            if delagger:
                time.sleep(0.01)

        if self.client[num].temps-1 == self.highestDel:
            self.seekLowest()
            
        self.client[num].temps+=1#augmente le temps du la personne qui veux les actions
        
        if self.highestRead < self.client[num].temps: #sil est plus avancer dans le temps on enregistre son temps
            self.highestRead +=1
        return self.actions[self.client[num].temps-1]# le -1 est la ,parce quon a augmenter le temps avant d'envoyer le reponse
    
    def seekLowest(self): # cherche le client qui est le plus en retard dans la lecture des evenement
        #on trouve le temps le plus bas et on l'enregistre
        Lowest = self.client[0].temps
        for i in self.client:
            if i.temps < Lowest:
                Lowest = i.temps

        if Lowest-1 > self.highestDel:
            if Lowest-1 in self.actions: #on verifie s'il existe (jai tester on en a pas de besoin mais jeprefaire eviter de prendre des risque)
                del self.actions[(Lowest-1)]# on enleve levenement avant du plus bas
                self.highestDel = Lowest
            
            
            
        
        
    
GameHost=server()

daemon=Pyro4.Daemon(host="127.0.0.1",port=9999)

uri=daemon.register(GameHost,"foo")
print(uri) 

print("Prêt!")
daemon.requestLoop()

