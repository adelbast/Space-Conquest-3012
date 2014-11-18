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
        self.dictionaireAction.clear()
        
        #self.construireBatiment(0,"HQ")

        #self.etatCroissance()
        #self.etatMilitaire()
        self.construireWorkers()
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
        print(int(x),int(y),"-=+-=+_+=-==---=-==-")
        a = self.positionCreationValide((int(x),int(y)),self.parent.dictBatiment[unit][3])
        if a == 1:
            print("-=-==-=--=-==-==-=--=-==-==")
            print(a)
            print("=======-------===========")
        return a
        
        
    def positionPossible(self,unit):
        j=0
        placed = False
        while not placed:
          
            j+=1
            d = int((self.parent.dictBatiment[unit][3]/2) + (self.parent.dictBatiment[unit][3]/2) + j )
            g = self.parent.dictBatiment[unit][3] + 2*d
           
            for i in range (g):
                if not placed:
                    x = (i+ (self.listeBatiment[0].position[0]) - ((self.listeBatiment[0].size/2) +d)) /32
                    
                    y = (self.listeBatiment[0].position[1] - d - (self.listeBatiment[0].size/2)) /32
                    placed = self.verificationCarre(x,y,unit)
                    if placed:
                        return (x,y)

                
                    
                if not placed:
                    x = (i + (self.listeBatiment[0].position[0]) - ((self.listeBatiment[0].size/2) +d))/32
                    y = (self.listeBatiment[0].position[1] + d + (self.listeBatiment[0].size/2)) /32

                    placed = self.verificationCarre (x,y,unit)
                    
                    if placed:
                        return (x,y)

                    
                if not placed:
                    x = ( (self.listeBatiment[0].position[0]) - (self.listeBatiment[0].position[0]) - d) /32
                    y = i+ ((self.listeBatiment[0].position[1] -(self.listeBatiment[0].position[0]) -d)) /32

                    placed = self.verificationCarre (x,y,unit)
                    
                    if placed:
                        return (x,y)

                    
                if not placed:
                    x = (self.listeBatiment[0].position[0] + self.listeBatiment[0].size/2 + d) /32
                    y = (i+ (self.listeBatiment[0].position[1] -(self.listeBatiment[0].position[0]) -d)) /32

                    placed = self.verificationCarre (x,y,unit)
                    
                    if placed:
                        return (x,y)
                  
                    
    def construireWorkers(self):#automatise le nombre requis de workers     #Antoine
        for i in self.listeBatiment:
            if (self.listeBatiment[i].name == "HQ"):
                for j in range(self.nbWorkersReq - self.nbWorkers):
                    print(j)
                    print(self.nbWorkersReq - self.nbWorkers)
                    if 'NewUnit' in self.dictionaireAction:
                        print("dic existe")
                        print(j)
                        self.dictionaireAction['NewUnit'].append(("worker", (self.listeBatiment[i].position[0]+60,self.listeBatiment[i].position[1]+50*j)))
                        self.nbWorkers+=1
                        print("unit cree")
                    else:
                        print("dic existe pas")
                        self.dictionaireAction['NewUnit'] =[("worker", (self.listeBatiment[i].position[0]+60,self.listeBatiment[i].position[1]+(50*j*2)))]
                        self.nbWorkers+=1
                        print(j)
                        print("unit cree no dic")
            #else: créer un HQ
            
               


                  

     
          
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
        print ("1")
        x,y =self.positionPossible("HQ")
        self.dictionaireAction["NewBatiment"]=("HQ",x,y)
        
        
    
#------------------------------Aggresive------------------------------#
    def etatMilitaire(self):
        pass

    def verifierNbTypeUnitAttaque(self):
        pass
    
    def attaque(self):
        #if self.verifierNbTypeAttaque():    
        pass

    def repliStrategique(self):
        pass

    

    
