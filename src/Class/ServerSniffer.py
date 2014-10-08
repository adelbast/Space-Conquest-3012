import Pyro4, multiprocessing, socket
from multiprocessing import Queue

#VAS VOIR TON PROCESSEUR ET TA MEMOIRE DANS LE GESTIONAIRE DE TACHE!
#ATTENTION/WARNING/ACHTUNG/ADVERTENCIA : CE PROGRAMME BOUFFE 2gb de ram !!!!!!!!!!!!
#note à moi même, ne plus faire autant de process en  meme temps...

class Sniffer(object):
	def __init__(self,test = False):
		self.resultat = []
		self.port = str(9992)
		self.ur = ""			# Addresse complete du serveur que l'on tente de joindre
		self.monserveur = None	# Objet fournit par le serveur si la connection est réussi
		self.q = Queue()		# File d'attente d'objet, qui est une sous classe de multiprocessing, donc, elle se lock tout seul a chaque fois qu'un process ajoute ou enleve quelque chose
								# On ne peux acceder qu'au premier element de la liste, et on ne peux ajouter d'element qu'a la fin
		if(test):
			self.rechercheDeServeur()	# Fonction de recherche de serveur
			self.imprimer()			# Fonction d'impression du retour des process de la fonction test()

	def rechercheDeServeur(self):
		"""
		Fonction de recherche de serveur valide.
		Cette fonction boucle sur tous les addresses ---> de xxx.xxx.xxx.0 à xxx.xxx.xxx.255.
		Pour chaqune de ces addresses, la fonction test() est lance dans un process different.
		"""
		ip = socket.gethostbyname(socket.gethostname())	# Donne le ip du client
		ip = ip.split(".")					# Separe l'addresse dans un array
		ip = ip[0]+"."+ip[1]+"."+ip[2] 		# Je ne prend que les trois premiers chiffres de l'IP dans le array
		for i in range(0,256):				# Iteration sur les 256 chiffre du dernier chiffre de l'IP
			self.ur="PYRO:foo@"+ip+".%s:"%i+self.port # Creation de l'addresse complete. %i remplace la valeur de %s dans le string
			print("Testing : " + self.ur)
			try:
				proc = multiprocessing.Process(target=self.test, args=(i,)) # cree un process dont la cible est la fonction "self.test()" avec l'argument "i" !(la virgule est nécéssaire)
				proc.deamon = True	# Premet au processus mere de fermer même si il reste des processus enfants vivant
				proc.start()		# Demarre le processus !(lance la fonction test() dans un processus différent)
									# Meme si le processus ne répond pas tout de suite, le processus mere continue de boucler

			except Exception as e:
				print(e)

	def test(self,i):
		"""
		Fonction de test de serveur valide.
		Cette fonction cree un objet Pyro4.Proxy !(Lire : Serveur Pyro).
		On essaye ensuite d'acceder a un fonction de l'objet cree.
		Si ca marche, on sauvegarde le nom du serveur et son ip dans des Queues.
		"""
		try:
			self.monserveur=Pyro4.Proxy(self.ur)		# Assignation d'un objet serveur
			self.q.put(self.monserveur.getInfo())		# Tente d'utiliser une fonction du nouvel objet serveur
														# Ajoute les information du serveur dans des queues			
		except Exception as e:
			pass

	def imprimer(self):
		"""
		Fonction d'impression du contenue des Queues
		"""
		pasVide = True #Flag d'iteration
		print("Serveur Valide : ")
		while pasVide:
			try:
				info = self.q.get(True,10)	# Le premier parametre: LOCK, arrete le processus tant qu'il n'y a pas d'element dans la "Queue"
											# Le deuxieme parametre: TIMEOUT, enleve le LOCK passé le temps donné
											# Lance une exception si il n'y a plus d'element en queue: Queue.Empty
				self.resultat.append(info)
				print(info)
			except Exception as e:
				pasVide = False	# Pour sortir de la boucle
				print("FIN!!!")

	def getResultat(self):
		return self.resultat

if __name__ == '__main__':
	s=Sniffer(test = True)
