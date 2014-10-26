import Pyro4
import traceback
import socket


class Client(object):
	def __init__(self, nom,  test = False):
		self.nom =  nom
		self.noJoueur = None
		self.proxy = None
		self.nameServer = None
		self.getNameServer()
		if(test):
			s = self.getServers()
			try:
				liste = [clee for clee, valeur in s.items() if clee != "Pyro.NameServer"]

				print(liste)
				self.connect("SpaceConquest3012")
			except Exception as e:
				print(traceback.print_exc())	#code pour avoir le "FULL STACK TRACE" :D

	#Envoie le (possiblement "les" pour le host) dictionaires au serveur
	def pushAction(self,listeDic):
		try:
			self.proxy.sendAction(listeDic)
		except Exception as e:
			print(e)

	#Demande à recevoir les dictionaires des autres joueurs
	def pullAction(self):
		try:
			return self.proxy.readAction(self.noJoueur)
		except Exception as e:
			print(e)

	#Cherche le nameServer (Serveur secondaire sur lequel est enregister le(s) serveur(s) de jeux)
	def getNameServer(self):
		try:
			print("Recherche Du NameServer...")
			self.nameServer = Pyro4.naming.locateNS()	#Recherche le nameServer et l'assigne s'il le trouve
			print("Trouvé")
		except Exception as e:
			print("Le nameServer n'a pas été trouvé")

	def isNameServerAlive(self):
		try:
			self.nameServer.ping()	#Test que le nameserver est en ligne
			return True
		except:
			return False

	#Demande au nameServer la liste des serveurs enregister dans sa base de donné
	def getServers(self):
		if( not self.isNameServerAlive() ):
			self.getNameServer()
		try:
			return [clee for clee, valeur in self.nameServer.list().items() if clee != "Pyro.NameServer"]	#retourne un dict d'adresse de forme Uri
		except:
			print("Handling Error :")
			print(traceback.print_exc())	#code pour avoir le "FULL STACK TRACE" :D
			print("Still rollin!")
			return None

	#Crée l'objet serveur (dit Proxy) à partir du nom fournis et souscrit au serveur qui lui retourne un numero unique
	def connect(self,nomDuServeur):
		try:
			uri = self.nameServer.lookup(nomDuServeur)	#Cherche sur le nameServer si un serveur correspond au nom recu en param
			print("Connection en cours...")
			self.proxy = Pyro4.Proxy(uri)				#Assigne l'adresse uri à l'objet pyro
			self.noJoueur = self.proxy.seConnecter(self.nom)		#Signale au serveur qu'on est connecté et celui-ci nous assigne un numero unique
			print("Connection établie!")
		except:
			print("Handling Error :")
			print(traceback.print_exc())	#code pour avoir le "FULL STACK TRACE" :D
			print("Still rollin!")
			return 1

	#Getter des info que le serveur doit donner à chaque client pour démarrer la partie
	def getStartingInfo(self):
		return self.proxy.getStartingInfo()


if __name__ == '__main__':
	m=Client(nom = "Bob",test = True)