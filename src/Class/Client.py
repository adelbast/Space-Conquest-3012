import Pyro4
import traceback


class Client(object):
	def __init__(self,noJoueur, num, temps, test = False):
		self.noJoueur = noJoueur
		self.proxy = None
		self.num = num
		self.temps = temps #represente ou il est rendu dans sa lecture des evenements
		
		if(test):
			self.search()

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

	def search(self):
		try:
			self.proxy = Pyro4.naming.locateNS()
			if(self.proxy.ping()):
				print("yes!")
		except Exception as e:
			print("Handling Error :")
			print(traceback.print_exc())
			print("Still rollin!")
			self.proxy = None


	def deepSearch(self):
		from ServerSniffer import Sniffer
		sniffer = Sniffer()
		sniffer.rechercheDeServeur()


if __name__ == '__main__':
	m=Client(0,0,0,True)