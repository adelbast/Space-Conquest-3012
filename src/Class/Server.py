# -*- coding: iso-8859-1 -*-
import Pyro4
import socket

VERSION = "1.0"

class Serviteur(object):
	def __init__(self,nomServeur,nomJoueurHost,ip):
		self.nomServeur = nomServeur
		self.nomJoueurHost = nomJoueurHost
		self.ip = ip

	def servir(self):
		pass

	def getBasicInfo(self):
		global VERSION
		info = {
			"NAME":self.nom,
			"IP":self.ip,
			"VERSION": VERSION,
			"DEBUG":"No support",
			"NB_CLIENT":"No support"
		}
		print("Trouver!")
		return info

        
class Server(object):
	def __init__(self, nomServeur,nomJoueurHost):
		self.port = 9988
		self.ip = socket.gethostbyname(socket.gethostname())
		self.serviteur=Serviteur(nomServeur,nomJoueurHost,self.ip)

		
		daemon=Pyro4.Daemon(host=self.ip,port=self.port)

		uri=daemon.register(self.serviteur,"SpaceConquest3012")
		print(uri)

		print("Pret!")
		daemon.requestLoop()

if __name__ == '__main__':
	m=Main()
