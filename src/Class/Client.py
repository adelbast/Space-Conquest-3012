import Pyro4


class Client(object):
	def __init__(self,noJoueur,test=False):
		self.noJoueur=noJoueur
		self.server = None
		
		if(test):
			self.trouverServeur()

	def trouverServeur(self):
		self.server = Pyro4.naming.locateNS()
		if(self.server.ping()):
			print("yes!")


if __name__ == '__main__':
	m=Client(2,True)