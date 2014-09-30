import Vue
import Modele

class Controleur:
    def __init__(self):
        self.modele = Modele.Modele(self)
        self.vue = Vue.Vue(self)
        self.vue.root.mainloop()

if __name__ == "__main__":
    c = Controleur()
