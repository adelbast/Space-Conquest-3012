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

    def faireQqch(self):#bouge automatiquement(arbitrairement) l'unité 0
        self.compteur += 1
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

    def verificationCarre(self,x,y,unit):
        for i in range(unit.size):
            for j in range(unit.size):
                for k in parent.listeJoueur:
                    for l in k.listeUnite:
                        if k.listeUnite[l].position[0] == x+i :
                            if k.listeUnite[l].position[1] == y+j:
                                return False
                    for l in k.listeBatiment:
                        if k.listeBatiment[l].position[0] == x+i :
                            if k.listeBatiment[l].position[1] == y+j:
                                return False
            
        
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
                if placed:
                    pass
                    
                if not placed:
                    placed = verificationCarre ((i + (self.listeBatiment[1].position[0]) - ((self.listeBatiment[1].size/2) +d),
                                            (self.listeBatiment[1].position[1] + d + (self.listeBatiment[1].size/2)),unit))
                    if placed:
                        pass
                if not placed:
                    placed = verificationCarre (( (self.listeBatiment[1].position[0]) - (self.listeBatiment[1].position[0]) - d),
                                              (i+ (self.listeBatiment[1].position[1] -(self.listeBatiment[1].position[0]) -d)) ,unit)
                if not placed:
                    placed = verificationCarre ((self.listeBatiment[1].position[0] + self.listeBatiment[1].size/2 + d),
                                              (i+ (self.listeBatiment[1].position[1] -(self.listeBatiment[1].position[0]) -d)) ,unit)
            if placed:
                return
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
                 
    def construireBatiment(self,worker,batiment):   #tentative de faire créer un batiments à l'AI - à arranger 
        x,y =self.positionPossible( )
        self.dictionaireAction["NewBatiment"]=("HQ",128,2000)
        
        
    
#------------------------------Aggresive------------------------------#
    def etatMilitaire(self):
        pass
