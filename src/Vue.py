from tkinter import *
from PIL import ImageTk

class Vue:
    def __init__(self, parent):    
        self.parent = parent #Pour l'heritage provenant du Controleur
        self.root = Tk()
        self.root.resizable(0,0)
        self.root.title("RTS")
        self.width = 1200
        self.height = 800
        self.root.geometry(str(self.width)+"x"+str(self.height))

        #Pour transferer les images en PhotoImage
        for tile in self.parent.modele.tileset.tileset:
            tile.img = ImageTk.PhotoImage(tile.img)
            
        #Initialisation de la surface de jeu
        self.surfaceJeu = Canvas(self.root, width=1200, height=600, bg='white', highlightthickness=0)
        self.surfaceJeu.configure(scrollregion=(0,0,len(self.parent.modele.map.map[0])*64,len(self.parent.modele.map.map)*64))
        self.surfaceJeu.place(x=0, y=0)

        self.displayMap()

    #Pour que le canvas scroll lorsquon click
        self.surfaceJeu.bind("<ButtonPress-1>", self.scroll_start)
        self.surfaceJeu.bind("<B1-Motion>", self.scroll_move)

    def scroll_start(self, event):
        self.surfaceJeu.scan_mark(event.x, event.y)
        
    
    def scroll_move(self, event):
        self.surfaceJeu.scan_dragto(event.x, event.y, gain=1)
        print(self.surfaceJeu.canvasx(0), self.surfaceJeu.canvasy(0))
       
        

    def displayMap(self):
        
        #Pour chaque ligne
        for y in range(0, len(self.parent.modele.map.map)):

            #Pour chaque colone
            for x in range(0, len(self.parent.modele.map.map[0])):

             
                self.surfaceJeu.create_image(x*64,y*64,anchor=NW, image=self.parent.modele.tileset.tileset[int(self.parent.modele.map.map[y][x])].img, tags="tile")

                

    
        
        
        
