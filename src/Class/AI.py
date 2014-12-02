from Class.Joueur import Joueur
import traceback
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
        self.test = False
        self.test2 = False
        self.TrooperCree=False
        
    def faireQqch(self):#bouge automatiquement(arbitrairement) l'unité 0
        self.compteur += 1
        self.dictionaireAction.clear()
      
        
        if not self.test:
            self.test = True
            self.construireBatiment(0,"barrack")

        self.etatMilitaire()


        #self.etatCroissance()
        
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

    def verificationCarre(self,x,y,unit,a):
        print("=-==-=",int(x),int(y),a,"-=-=-=-")
        a= 0
        if x >= 0:
            if y >= 0:
                a = self.positionCreationValide((int(x),int(y)),self.parent.dictBatiment[unit][3])  
        return a
        
        
    def positionPossible(self,unit):
        j=-32
        placed = False
        while not placed:
            j+=32         
            d = int((self.parent.dictBatiment[unit][3]/2) + (self.listeBatiment[0].size/2) + j )
            g = (self.listeBatiment[0].size + 2*d)/32
            g2 = g*2

            for i in range(int(g2)):

                if not placed:
   
                    x = i+ ((self.listeBatiment[0].position[0] - self.listeBatiment[0].size/2) +d) -g

                    y = ((self.listeBatiment[0].position[1] - self.listeBatiment[0].size/2) + d) 
                    print(x,y)
                    placed = self.verificationCarre(x,y,unit,1)
                    if placed:
                        return (x,y)
                    
                if not placed:

                    x = ((i*32 + self.listeBatiment[0].position[0]) - ((self.listeBatiment[0].size/2) +d)) - g
                    y = (self.listeBatiment[0].position[1] +  ((self.listeBatiment[0].size/2)+d)) 

                    placed = self.verificationCarre (x,y,unit,2)
                    
                    if placed:
                        return (x,y)
                    
                if not placed:

                    x = ( self.listeBatiment[0].position[0] + (self.listeBatiment[0].size/2) + d) 
                    y = ((i*32+self.listeBatiment[0].position[1]) + ((self.listeBatiment[0].size/2) + d) )-g


                    placed = self.verificationCarre (x,y,unit,3)
                    
                    if placed:
                        return (x,y)

                    
                if not placed:
                    x = (self.listeBatiment[0].position[0] + ((self.listeBatiment[0].size/2) + d)) 
                    print(4)
                    y = ((i*32+ self.listeBatiment[0].position[1]) -((self.listeBatiment[0].size/2) +d) )-g
                    print(4)

                    placed = self.verificationCarre (x,y,unit,4)
                    
                    if placed:
                        return (x,y)
        
                  
                    
    def construireWorkers(self):#automatise le nombre requis de workers     #Antoine
        for i in self.listeBatiment:
            if (self.listeBatiment[i].name == "HQ"):
                for j in range(self.nbWorkersReq - self.nbWorkers):
                    print(j)
                    print(self.nbWorkersReq - self.nbWorkers)
                    if 'NewUnit' not in self.dictionaireAction:
                        self.dictionaireAction['NewUnit'] = []
                    print("dic existe")
                    print(j)
                    self.dictionaireAction['NewUnit'].append(("worker", (self.listeBatiment[i].position[0]+60,self.listeBatiment[i].position[1]+50*j)))
                    self.nbWorkers+=1
                    print("unit cree")
                    
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
            i = 1 + int(self.compttracebackeur /20000)
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
                 
    def construireBatiment(self,worker,batiment):  
        x,y =self.positionPossible(batiment)
        valeur = [(batiment,0,x,y)]
        if not self.test2:
            self.dictionaireAction["NewBatiment"]= valeur
            self.test2 = True
        
    
#------------------------------Aggresive------------------------------#
    def etatMilitaire(self):
        if (self.TrooperCree == False):
            for i in range(self.listeBatiment.__len__()):
                if (self.listeBatiment[i].name == "barrack"):
                    if self.listeBatiment[i].estConstruit:
                       if "NewUnit" not in self.dictionaireAction:
                           self.dictionaireAction["NewUnit"] = []
                       self.dictionaireAction["NewUnit"].append (  ("trooper",(self.listeBatiment[i].position[0], self.listeBatiment[i].position[1]-110) )) #self.parent.spawnUnit("trooper",self.listeBatiment[i])
                       self.TrooperCree=True
    def verifierNbTypeUnitAttaque(self):
        pass
    
    def attaque(self):
        #if self.verifierNbTypeAttaque():    
        pass

    def repliStrategique(self):
        pass

    

    
