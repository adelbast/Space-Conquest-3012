from Class.Joueur import Joueur
#auteurs : Alexandre + Antoine
class AI(Joueur):
    def __init__(self, parent, noJoueur):
        super(AI, self).__init__(parent, "AI", noJoueur)
        self.parent = parent
        self.noJoueur = noJoueur
        self.dictionaireAction = {}
        self.compteur = 0
        self.listePriorite = []
        self.positionXY=(0,0)
        self.nbWorkers = 0
        self.nbWorkersReq = 3
        self.nbGen = [0,0,0]
        self.nbGenReq = [0,0,0]

    #   self.construireBatiment(0,"barrack")

    def faireQqch(self):#bouge automatiquement(arbitrairement) l'unité 0
        self.compteur += 1
       #self.construireBatiment(0,"barrack")
      # self.etatCroissance()
       #self.etatMilitaire()
    
        
        print("AI batiment")
#------------------------------Croissance------------------------------#

    def etatCroissance(self):
        print("EC")
        if (self.compteur % 10 == 0):
            self.calculateWorkers()
            
        if (self.nbWorkers < self.nbWorkersReq):
                self.construireWorkers()

        if (self.compteur %10 == 0):
            self.calculateGen()
        for i in range(len(self.nbGenreq)):
            if(self.nbGenReq[i] < self.nbGen[i]):
               self.construireGen(i)


    def construireGen(self,genType):
        print ("construire gen" + genType)
      #  if gentype != 1:

    def verificationCarre(self, position):
        pass
        
    def positionPossible(self,unit):
        j=0
        placed = False

        while not placed:
            j+=1
            d = (self.listeBatiment[1].size/2) + (unit.size/2) + j 
            g = self.listeBatiment[1].size + 2*d
           
            for i in range (g):
                placed = verificationCarre( (i+ (self.listeBatiment[1].position[0]) - ((self.listeBatiment[1].size/2) +d)),
                                        (self.listeBatiment[1].position[1] - d - (self.listeBatiment[1].size/2)),unit)

                placed = verificationCarre ((i + (self.listeBatiment[1].position[0]) - ((self.listeBatiment[1].size/2) +d),
                                            (self.listeBatiment[1].position[1] + d + (self.listeBatiment[1].size/2)),unit)) 

                placed = verificationCarre (( (self.listeBatiment[1].position[0]) - (self.listeBatiment[1].position[0]) - d),
                                              (i+ (self.listeBatiment[1].position[1] -(self.listeBatiment[1].position[0]) -d)) ,unit)

                placed = verificationCarre ((self.listeBatiment[1].position[0] + self.listeBatiment[1].size/2 + d),
                                              (i+ (self.listeBatiment[1].position[1] -(self.listeBatiment[1].position[0]) -d)) ,unit)

    def construireWorkers(self):
        for i in self.listeBatiment:
            if (i.name == "HQ"):
                
                self.creerUnite("worker", (200,50),(i.position[0]+50,i.position+75))
          
    def calculateGen():
        self.nbGen = [0,0,0]
        for i in self.listeBatiment:
               if (i.name == "ferme"):
                   self.nbGen[0]+=1
               if (i.name == "mine"):
                   self.nbGen[1]+=1
               if (i.name == "solarPanel"):
                   self.nbGen[2]+=1

        for i in self.nbGenReq :
            i = 1 + int(self.compteur /20000)
            if i > 5:
               i = 5

    def calculateWorkers(self):
        self.nbWorkers = 0 
        for i in self.listeUnite:
            if (i.name == "worker"):
                 self.nbWorkers+=1
                 
        self.nbWorkersReq =  3 + int(self.compteur / 1000)
        if self.nbWorkersReq > 20:
            self.nbWorkerReq = 20
                 
#   def construireBatiment(self,worker,nom):   #tentative de faire créer un batiments à l'AI - à arranger 
   #    print(self.parent.dictBatiment)
   #    self.positionTest[1]+=10
   #    Joueur.creerBatiment([50,50],True,"barrack",0,self.parent.dictBatiment["barrack"])
    
        
    ''' for i in self.listebatiment:
            if (i.name == "HQ"):
                positionXY = i.position
            
        self.creerUnite(worker, attributs, positionXY)
        self.creerUnite(worker, attributs, positionXY)
        self.creerUnite(worker, attributs, positionXY)
        self.nbWorkers = 3
    '''
#------------------------------Aggresive------------------------------#
    def etatMilitaire(self):
        pass
