import Pyro4
import traceback
import socket


class Client(object):
	def __init__(self, noJoueur, num, temps, test = False):
		self.noJoueur = noJoueur
		self.proxy = None
		self.num = num
		self.nameServer = None
		self.temps = temps #represente ou il est rendu dans sa lecture des evenements
		
		if(test):
			s = self.getServers()
			try:
				liste = [clee for clee, valeur in s.items() if clee != "Pyro.NameServer"]

				print(liste)
				self.connect("SpaceConquest3012")
			except Exception as e:
				print(traceback.print_exc())	#code pour avoir le "FULL STACK TRACE" :D

	def pushAction(self,dicAction2Server):
		try:
			self.proxy.sendAction(dicAction2Server)
		except Exception as e:
			print(e)

	def pullAction(self):
		try:
			return self.proxy.readAction()
		except Exception as e:
			print(e)

	def getNameServer(self):
		try:
			print("Recherche Du NameServer...")
			self.nameServer = Pyro4.naming.locateNS()	#Recherche le nameServer et l'assigne s'il le trouve
			print("Trouvé")
		except Exception as e:
			print(e)

	def getServers(self):
		if(not self.nameServer):
			self.getNameServer()
		try:
			return self.nameServer.list()	#retourne un dict d'adresse de forme Uri
		except Exception as e:
			print("Handling Error :")
			print(traceback.print_exc())	#code pour avoir le "FULL STACK TRACE" :D
			print("Still rollin!")
			return None

	def connect(self,nomDuServeur):
		try:
			self.nameServer.ping()						#Test que le nameserver est en ligne
			uri = self.nameServer.lookup(nomDuServeur)	#Cherche sur le nameServer si un serveur correspond au nom recu en param
			print("Connection en cours...")
			self.proxy = Pyro4.Proxy(uri)				#Assigne l'adresse uri à l'objet pyro
			self.proxy.ping()							#Test si l'objet est en ligne
			self.num = self.proxy.seConnecter()			#Signale au serveur qu'on est connecté et celui-ci nous assigne un numero unique
			print("Connection établie!")
		except Exception as e:
			print(e)

	def deepSearch(self): #Dangereux
		from ServerSniffer import Sniffer
		sniffer = Sniffer()
		sniffer.rechercheDeServeur()


if __name__ == '__main__':
	m=Client(0,0,0,True)