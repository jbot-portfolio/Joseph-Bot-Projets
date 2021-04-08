# PROGRAMMÉ PAR JOSEPH BOT #
#--------------------------#

from tkinter import*
import time
import random as rd

#Paramètre de la fenêtre
window = Tk()
window.title("Casse Brique")
window.geometry("1368x766")
window.config(background="#363636")

#Fenêtre de jeu
canvas = Canvas(window, width=1200, height=700, bd=0, bg="#323232")
canvas.pack(padx=50, pady=50)

x = 0
y = 0

class Ball():
    """ Création de la balle """

    def __init__(self): #Initialisation

        #Choix aléatoire de la taille de la balle
        self.rngTaille = rd.randint(20,30)
        
        #Initialisation des coordonnées de la balle
        self.xb1, self.yb1  = 600, 500
        self.xb2, self.yb2 = self.xb1+self.rngTaille, self.yb1+self.rngTaille

        self.vitesse = rd.randint(7,9)

        #On génère aléatoirement les vitesses de déplacements : dx += 5, dy += 5
        if rd.randint(0,1) == 0:
            self.dx = -self.vitesse
        else:
            self.dx = self.vitesse
        if rd.randint(0,1) == 0:
            self.dy = self.vitesse
        else:
            self.dy = -self.vitesse

        #On définie une liste stockant toutes les couleurs possibles de la balle
        self.rngColor = ["red", "skyblue", "purple", "orange","green","cyan", "yellow"]

        #On place la balle, de couleur aléatoire
        self.ball = canvas.create_oval(self.xb1, self.yb1, self.xb2, self.yb2, fill=self.rngColor[rd.randint(0,len(self.rngColor)-1)])

    def animationBall(self):
        """ Permet le déplacement et les rebonds de la balle """

        #Liste des coordonnées de ma raquette
        cooR = canvas.coords(self.ball)

        #gestions des rebonds sur les bords gauche et droit et supérrieur
        if (cooR[1] < 0):
            self.dy = -self.dy
        if (cooR[0] < 0) or (cooR[2] > 1200):
            self.dx = -self.dx

        #gestion de la collision avec la raquette
        if len(canvas.find_overlapping(cooR[0], cooR[1], cooR[2], cooR[3])) > 1:
            self.dy = -self.dy

        #arrêt avec la méthode exit() si collision loupé acec la raquette
        if (cooR[3] > 680): #self.raquette.yr2+150
            time.sleep(0.2)
            exit()

        #Affichage de la balle
        canvas.move(self.ball, self.dx, self.dy)
        window.after(20, self.animationBall)

    def animeRGB(self): #Change la couleur de la balle
        canvas.itemconfigure(self.ball, fill=self.rngColor[rd.randint(0,len(self.rngColor)-1)])
        window.after(250, self.animeRGB)

class Raq():
    """ Création de la raquette """

    def __init__(self):
        #Initialisation des coordonnées de la raquette
        self.xr1, self.yr1, self.xr2, self.yr2 = 800, 680, rd.randint(150, 450), 630
        #On place la raquette de couleur verte
        self.raquette = canvas.create_rectangle(self.xr1, self.yr1, self.xr2, self.yr2, fill="green")

    def droiteRaq(self, event):
        #Deplacement horizontal de la raquette de +15
        canvas.move(self.raquette, 25, 0)

    def gaucheRaq(self, event):
        #Deplacement horizontal de la raquette de -15
        canvas.move(self.raquette, -25, 0)

class Brique():
    """ Création des briques """
    
    def __init__(self): #Initialisation
        global x, y
        x+=125
        self.PV = 2
        
        #Positionnement des briques
        self.posX, self.posY = -75, 75
        self.xbr1, self.ybr1, self.xbr2, self.ybr2 = self.posX+x, self.posY+y, self.posX+100+x, self.posY+30+y
        self.brique = canvas.create_rectangle(self.xbr1, self.ybr1, self.xbr2, self.ybr2, fill="white")

        #Retour a la ligne du placement des briques
        if self.posX+x >= 1050:
            x = 0
            y += 50

        self.cooBrique = canvas.coords(self.brique)

    def delBrique(self):
        """ Supprime une brique """

        #Lors de la première collision avec une balle
        if len(canvas.find_overlapping(self.cooBrique[0], self.cooBrique[1], self.cooBrique[2], self.cooBrique[3])) > 1 and self.PV >= 2:
            canvas.itemconfigure(self.brique, fill="red")
            self.PV -= 1
        #Lors de la deuxième collision avec une balle
        elif len(canvas.find_overlapping(self.cooBrique[0], self.cooBrique[1], self.cooBrique[2], self.cooBrique[3])) > 1 and self.PV == 1:
            canvas.delete(self.brique) #Destruction de la balle

        window.after(20, self.delBrique)


#Instanciation des items
r=Raq()
br=Brique()
br.delBrique()

#Instanciation des briques
for i in range(2,46):
            globals()['br%s' % i]=Brique()
            globals()['br%s' % i].delBrique()

b=Ball()
b.animationBall() #Deplacement de la balle

#Jouer avec plusieurs balles
"""
b2=Ball()
b3=Ball()

b2.animationBall()
b3.animationBall()

b.animeRGB()
b2.animeRGB()
b3.animeRGB()"""

#Gestionnaire d'evenements pour le déplacement de la raquette
window.bind("<Left>", r.gaucheRaq)
window.bind("<Right>", r.droiteRaq)

#Affichage de la fenetre
window.mainloop()