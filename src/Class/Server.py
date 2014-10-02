import Pyro4
import socket
from Pyro4 import core

VERSION = "1.0"

class Serviteur(object):
	def __init__(self,nomServeur,nomJoueurHost,ip):
		self.nomServeur = nomServeur
		self.nomJoueurHost = nomJoueurHost
		self.listeClient = []
		self.ip = ip

	def ping(self):
		print("ping")

	def getBasicInfo(self):
		global VERSION
		info = {#dictionaire d'info sur le serveur
			"NAME":self.nom,
			"IP":self.ip,
			"VERSION": VERSION,
			"DEBUG":"No support",
			"NB_CLIENT":"No support"
		}
		return info

        
class Server(object):
	def __init__(self, nomServeur = "SpaceConquest3012",nomJoueurHost = "xavier", test = False):
		self.uri = None		#adresse utiliser par pyro pour se connecter au objets distants
		self.port = 9992
		self.ip = socket.gethostbyname(socket.gethostname())	#retourne le IP
		self.serviteur=Serviteur(nomServeur,nomJoueurHost,self.ip)	#objet distant
		if(test):
			self.start()

	def start(self):#lance le serveur de jeu
		daemon=Pyro4.Daemon(host=self.ip,port=self.port)
		self.uri=daemon.register(self.serviteur,nomServeur)#"PYRO:SpaceConquest3012@192.168.100.2:9992" Uri ressemble à quelque chose comme ça
		print(self.uri)
		self.startBroadcast()
		print("Pret!")
		daemon.requestLoop()

	def startBroadcast(self):	#lance le serveur qui broadcast les infos du serveur de jeu sur le réseau
		bS = Pyro4.naming.BroadcastServer(nsUri = core.URI(self.uri), bcport = self.port+1)#création de l'objet serveur (self.port+1 car ""socket"" ne peut pas binder deux fois le même socket)
		bS.runInThread()		#lance le serveur de broadcast dans un autre thread

	def stopBroadcast(self):
		bS.close()
        

if __name__ == '__main__':
	m=Server(test = True)