from Tile.Map import Map
from Class.Joueur import Joueur
from Class.AI import AI


class Modele(object):
    def __init__(self):
        self.host = False
        self.listeJoueur = []
        self.noJoueurLocal = None
        self.maxUnite = 20  #???
        self.selection = []
        self.listeArtefact = []
        
        self.map = Map("Tile/map1.csv")

        self.dicAction2Server = {}
        self.dicActionFromServer = [{#joueur1
                                    "Deplacement":     (0, 500,500),#(noUnit, cibleX, cibleY)
                                    "DeplacementCible":(1, 2, 1, 0),#(noUnit, noProprio, 0:unité/1:structure , noUnitCible)
                                    "RechercheAge": 1,          #si changement d'âge
                                    "NewUnit":      (0,0),      #(type d'unité, noDuBatimentSpawner)
                                    "NewStruct":    (2,200,200),#(typeBatiment, posX, posY)
                                    "SuppressionBatiment":1,    #noBatiment
                                    "SuppressionUnit":2,        #noUnit
                                    "CaptureArtefact":0,        #noArtefact
                                    "PerteArtefact":1},
                                    
                                    {#joueur2

                                    },
                                    {},#joueur3
                                    {}]#joueur4...
        # facilite la gestion de la souris
        self.ClickPosx = 0
        self.ClickPosy = 0
        self.ReleasePosx = 0
        self.ReleasePosy = 0
        self.drag = False
    
    def initPartie(self,noJoueur,listeNomJoueur,host=False):
        self.noJoueurLocal = noJoueur
        for nomJoueur in listeNomJoueur:
            if(nomJoueur == "AI"):
                self.listeJoueur.append(AI(len(self.listeJoueur)))
            else:
                self.listeJoueur.append(Joueur(nomJoueur,len(self.listeJoueur)))
        self.host = host



    def gestion(self,dicActionFromServer):
        self.listeJoueur[self.noJoueurLocal].compterRessource()
        ii = 0
        for dic in dicActionFromServer:
            if(dic):
                if(ii != noJoueurLocal):
                    if(self.joueurPasMort(self.listeJoueur[ii])):
                        for clee, valeur in d.items():
                            if(clee == "Deplacement"):
                                noUnit, x, y = valeur
                            elif(clee == "DeplacementCible"):
                                noUnit, noProprio, UvS, noUnitCible = valeur
                            elif(clee == "RechercheAge"):
                                age = valeur
                            elif(clee == "NewUnit"):
                                typeUnit, noDuBatimentSpawner = valeur
                            elif(clee == "NewStruct"):
                                typeBatiment, x, y = valeur
                            elif(clee == "SuppressionBatiment"):
                                noBatiment = valeur
                            elif(clee == "SuppressionUnit"):
                                noUnit = valeur
                            elif(clee == "CaptureArtefact"):
                                noArtefact = valeur
                            elif(clee == "PerteArtefact"):
                                noArtefact = valeur

    def gererMouseClick(self,event): #ne faudrait-il pas mettre tout cela dans mouse release,ainsi on peu mettre une condition pour savoir si il y a drag ou non
        if(event.num == 0): #assomption de bouton droit
            cible = self.clickCibleOuTile(event.x,event.y)
            self.modifierSelection(cible)

        if(event.num == 1):     #assomption de bouton gauche
            #print("dans le modeleClick", event.x, event.y)
            self.ClickPosx = event.x
            self.ClickPosy = event.y
            print("okay click fait")
            if(self.selection): #Si le joueur a quelque chose de sélectionné, sinon inutile
                if(self.selection[0].owner.noJoueur == self.noJoueurLocal):

                    try:            #Duck typing
                        self.selection[0].move(None)
                    except Exception as e:#c'est donc un batiment
                        pass
                    else:#si pas d'exception
                        cible = self.clickCibleOuTile(event.x,event.y)
                        if(not cible):
                            cible = (event.x,event.y)

                        for unite in self.selection:
                            unite.move(cible)

    def gererDrag(self):
        if(self.drag == True):
            print("drag dans modele")
        #faire gestion de la selection multiple

    def gererMouseRelease(self,event):
       # print("dans le mouseReleaseModele", event.x, event.y)
       # a ajouter : le rajout des unite entre clickXY et releaseXY
        self.ReleasePosx = event.x
        self.ReleasePosy = event.y
        print("mouseRelease")

    def clickCibleOuTile(self,x,y): #retourne None pour un tile et la cible pour une cible
    #fonction qui regarde si le clic est sur un batiment ou une unité
        for joueur in listeJoueur:
            liste = joueur.listeUnite+joueur.listeBatiment
            for chose in liste:
                if(x < chose.position[0]):#+grosseur/2
                    if(x > chose.position[0]):#-grosseur/2
                        if(y < chose.position[1]):#+grosseur/2
                            if(y > chose.position[1]):#-grosseur/2
                                return chose
        else: return None

    def modifierSelection(self,cible):
        self.selection = cible


    def joueurPasMort(self,joueur):
        joueur.compterBatiment()
        if(not joueur.nbBatiment):
            print(joueur.nom+" est mort")
            return False
