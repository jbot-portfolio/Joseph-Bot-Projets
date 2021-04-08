# PROGRAMMÉ PAR JOSEPH BOT #
#--------------------------#

            #------------------------------------------------#
            #           PARTIE INTERFACE GRAPHIQUE           #
            #------------------------------------------------#

#Importation des modules
from tkinter import*
from tkinter import messagebox
from tkinter import colorchooser
import os

#Création de la fenêtre
window = Tk()

#Personnalistion de la fenêtre
window.title("NSI - Joseph Bot  (WORK IN PROGRESS)") #Titre de la fenêtre
window.geometry("1220x720")   # |
window.minsize(1220,720)      #  > Dimensionnement de la fênetre (avec une taille min/max) 
window.maxsize(1920,1080)     # |
window.config(background="#363636") #Couleur de fond de la fenêtre

#Creation d'une frame (=Cadre invisible) pour la grille dans laquelle sera placé les 9 boutons
frameGrille = Frame(window, bg="#363636")

#On créer un texte et un sous texte qui affichera les informations de la partie
TexteTour = Label(frameGrille,text="MORPION", font=("Arial", 42), bg="#363636", fg="white")
TexteTour.grid(row=1, column=4, sticky=S, padx=135, pady=42) #Affichage du texte
sousTexteTour = Label(frameGrille,text="Le joueur 1 commence !", font=("Arial", 20), bg="#363636", fg="white")
sousTexteTour.grid(row=1, column=4, sticky=S, padx=135, pady=5) #Affichage du sous texte

#On une autre frame pour y mettre les zones d'entrées / boutons de personnalisation des joueurs.
frameInfoJoueur = Frame(window, bg="#363636")

#Noms des joueurs
P1Text = Label(frameInfoJoueur,text="Joueur  1 :", font=("Arial", 16), bg="#363636", fg="white")
P1Text.grid(row=0, column=0, pady=20) #Affichage du texte
entryNomJoueur1 = Entry(frameInfoJoueur,width=14, font=("Arial", 16), bg="#363636", fg="white") #Zone d'entrée de texte
entryNomJoueur1.grid(row=0, column=1, pady=21, padx=8) #Affichage de la zone d'entré du nom

P2Text = Label(frameInfoJoueur,text="Joueur  2 :", font=("Arial", 16), bg="#363636", fg="white")
P2Text.grid(row=0, column=4, pady=20) 
entryNomJoueur2 = Entry(frameInfoJoueur, width=14, font=("Arial", 16), bg="#363636", fg="white")
entryNomJoueur2.grid(row=0, column=5, pady=21, padx=8)

#On définis des dictionnaires stockant les informations des joueurs
joueur1 = {'nom':"", 'couleur':"#FFF", 'score':0}
joueur2 = {'nom':"", 'couleur':"#FFF", 'score':0}

def boutonValider():
      """ Fonction pour affecter les noms entrés par les utilisateur et leur couleur dans leur dictionnaires """
      assert entryNomJoueur1.get() != ""   #\
      assert entryNomJoueur2.get() != ""   #  On vérifie si l'utlisateur a bien entré
      assert joueur1['couleur'] != "#FFF"  #  son nom et a séléctionné sa couleur.
      assert joueur2['couleur'] != "#FFF"  #/

      joueur1['nom'] = entryNomJoueur1.get()
      joueur2['nom'] = entryNomJoueur2.get()
      for i in range(1,10): #Boucle for pour prendre chaque boutons (b1, b2, b3, b4...) et les réactiver.
            globals()['b%s' % i].configure(state=NORMAL)
      boutonValiderInfo.configure(state=DISABLED)
      boutonCouleurJ1.configure(state=DISABLED)
      boutonCouleurJ2.configure(state=DISABLED)

def choixCouleurJoueur1():
      """ Fonction permettant a l'utilisateur de choisir sa couleur, et puis la place dans son dictionnaire """
      choix = colorchooser.askcolor(title="Choisissez une couleur")
      joueur1['couleur'] = choix[1] #On applique le code couleur hexadecimal choisi
      entryNomJoueur1['fg'] = joueur1['couleur'] #On applique la couleur choisie au nom du joueur

def choixCouleurJoueur2():
      choix = colorchooser.askcolor(title="Choisissez une couleur")
      joueur2['couleur'] = choix[1] #On applique le code couleur hexadecimal choisi
      entryNomJoueur2['fg'] = joueur2['couleur'] #On applique la couleur choisie au nom du joueur


#Création d'un bouton pour valider les noms que les joueurs ont entré.
boutonValiderInfo = Button(frameInfoJoueur, relief='ridge', text="Valider", font=("Arial", 16), bg="#363636", fg="white", width=8, command=boutonValider)
boutonValiderInfo.grid(row=0, column=3, pady=21, padx=25)

#On va chercher l'emplacement de l'image pour le bouton choix de couleur grace au module 'os'
fichier_image = os.path.dirname(__file__)
emplacement_image = os.path.join(fichier_image, 'imageCouleur.png')

#Image selection couleur
imageCouleur = PhotoImage(file=emplacement_image).subsample(9) #Déclaration et redimensionement de l'image

#Création des 2 boutons pour choisir la couleur de chaque joueur.
boutonCouleurJ1 = Button(frameInfoJoueur, image=imageCouleur, relief='ridge', bg="#363636", fg="white", width=25, height=25, command=choixCouleurJoueur1)
boutonCouleurJ1.grid(row=0, column=2, pady=30, padx=2)
boutonCouleurJ2 = Button(frameInfoJoueur, image=imageCouleur, relief='ridge', bg="#363636", fg="white", width=25, height=25, command=choixCouleurJoueur2)
boutonCouleurJ2.grid(row=0, column=6, pady=30, padx=2)

#Affichage score des joueurs
textScoreJ1 = Label(frameInfoJoueur,text="Score : 0", font=("Arial", 16), bg="#363636", fg="white")
textScoreJ2 = Label(frameInfoJoueur,text="Score : 0", font=("Arial", 16), bg="#363636", fg="white")


#Affichage des frames
frameInfoJoueur.pack()
frameGrille.pack(expand=YES)

            #------------------------------------------------#
            #             PARTIE PROGRAMME DU JEU            #
            #------------------------------------------------#

#Definition des variables
tourJoueur = True
partieFinie = False
nbTours = 0

def boutonClick(buttons):
      """
      Cette fonction permet de placer les points sur la grille, lors du clique X ou O apparaitra sur la case choisie
      """
      global tourJoueur, nbTours #On utilise les variables définies au début du programme

      #On fait jouer le premier joueur si c'est son tour et si il a cliqué sur une case valide
      if buttons["text"] == " " and tourJoueur == True:
            buttons['fg'] = joueur1['couleur']
            buttons["text"] = "X" #On change la valeur du bouton par X
            nbTours += 1 #On incrémente le nombre de tours de 1
            tourJoueur = False
            sousTexteTour['text'] = f"Tour : {joueur2['nom']}"
            sousTexteTour['fg'] = joueur2['couleur']
            checkGagnant("X") #On vérifie si le joueur 1 à gagné

      #Sinon on fait jouer le deuxième joueur si il a cliqué sur une case vide et si c'est son tour
      elif buttons["text"] == " " and tourJoueur == False:
            buttons['fg'] = joueur2['couleur']
            buttons["text"] = "O" #On change la valeur du bouton par O
            nbTours += 1 #On incrémente le nombre de tours de 1
            tourJoueur = True
            sousTexteTour['text'] = f"Tour : {joueur1['nom']}"
            sousTexteTour['fg'] = joueur1['couleur']
            checkGagnant("O") #On vérifie si le joueur 2 à gagné

def checkGagnant(joueur):
      """
      Cette fonction permet d'identifier le gagnant, si il y en à un et de l'afficher a l'écran
      """
      global partieFinie
      if (b1['text'] == joueur and b2['text'] == joueur and b3['text'] == joueur or    #
            b4['text'] == joueur and b5['text'] == joueur and b6['text'] == joueur or  #
            b7['text'] ==joueur and b8['text'] == joueur and b9['text'] == joueur or   #
            b1['text'] == joueur and b5['text'] == joueur and b9['text'] == joueur or  #  On vérifie toutes les 
            b3['text'] == joueur and b5['text'] == joueur and b7['text'] == joueur or  #   possibilitées pour 
            b1['text'] == joueur and b4['text'] == joueur and b7['text'] == joueur or  #  determiner le gagnant
            b2['text'] == joueur and b5['text'] == joueur and b8['text'] == joueur or  #
            b3['text'] == joueur and b6['text'] == joueur and b9['text'] == joueur):   #

            #On vérifie qui a gagné
            if joueur == "X":
                  messagebox.showinfo("Morpion",f"Bravo {joueur1['nom']} à gagné !") #On affiche le gagnant
                  desactiveBoutons()
                  TexteTour['fg'] = joueur1['couleur']  # On affiche les informations du joueur 1
                  TexteTour['text'] = joueur1['nom']    # (Nom du joueur qui gagne avec sa couleur)
                  sousTexteTour['fg'] = 'white' #On remet la couleur du sous texte pour afficher "Gagne !" en blanc
                  sousTexteTour['text'] = "Gagne !" 
                  joueur1['score'] += 1 #On incrémente le score sur joueur 2 de 1
                  textScoreJ1['text'] = "Score : " + str(joueur1['score']) #On met à jour l'affichage du score du joueur 2
                  partieFinie = True
            else:
                  messagebox.showinfo("Morpion",f"Bravo {joueur2['nom']} à gagné !") #On affiche le gagnant
                  desactiveBoutons()
                  TexteTour['fg'] = joueur2['couleur']  #On affiche les informations du joueur 2
                  TexteTour['text'] = joueur2['nom']    #(Nom du joueur qui gagne avec sa couleur)
                  sousTexteTour['fg'] = 'white' #On remet la couleur du sous texte pour afficher "Gagne !" en blanc
                  sousTexteTour['text'] = "Gagne !"
                  joueur2['score'] += 1 #On incrémente le score sur joueur 2 de 1
                  textScoreJ2['text'] = "Score : " + str(joueur2['score']) #On met à jour l'affichage du score du joueur 2
                  partieFinie = True
            
            #On active le bouton rejouer
            boutonRejouer.configure(state=NORMAL)
      
            #On fait apparaître le score dés qu'un des deux joueurs gagne
            textScoreJ1.grid(row=1, column=0)
            textScoreJ2.grid(row=1, column=4)
      
      #On regarde combiens il reste de tous pour vérifier si il y a égalité pour non
      elif(nbTours == 9):
            messagebox.showinfo("Morpion","Match NUL !")
            desactiveBoutons()
            TexteTour['text'] = "MATCH"
            sousTexteTour['fg'] = 'white'
            sousTexteTour['text'] = "NUL"
            sousTexteTour.grid(row=1, column=4, sticky=S, padx=135,pady=4)
            #On active le bouton rejouer
            boutonRejouer.configure(state=NORMAL)

def desactiveBoutons():
      """ Cette fonction permet de désactiver tous les boutons """
      for i in range(1,10): #Boucle for pour prendre chaque boutons (b1, b2, b3, b4...) et les désactiver.
            globals()['b%s' % i].configure(state=DISABLED)

#Definition des boutons qui serons donc les cases
b1 = Button(frameGrille, relief="ridge", text=" ", font=("Arial", 60), bg="#363636", fg="white", height=1, width=3, command=lambda: boutonClick(b1))
b2 = Button(frameGrille, relief="ridge", text=" ", font=("Arial", 60), bg="#363636", fg="white", height=1, width=3, command=lambda: boutonClick(b2))
b3 = Button(frameGrille, relief="ridge", text=" ", font=("Arial", 60), bg="#363636", fg="white", height=1, width=3, command=lambda: boutonClick(b3))
b4 = Button(frameGrille, relief="ridge", text=" ", font=("Arial", 60), bg="#363636", fg="white", height=1, width=3, command=lambda: boutonClick(b4))
b5 = Button(frameGrille, relief="ridge", text=" ", font=("Arial", 60), bg="#363636", fg="white", height=1, width=3, command=lambda: boutonClick(b5))
b6 = Button(frameGrille, relief="ridge", text=" ", font=("Arial", 60), bg="#363636", fg="white", height=1, width=3, command=lambda: boutonClick(b6))
b7 = Button(frameGrille, relief="ridge", text=" ", font=("Arial", 60), bg="#363636", fg="white", height=1, width=3, command=lambda: boutonClick(b7))
b8 = Button(frameGrille, relief="ridge", text=" ", font=("Arial", 60), bg="#363636", fg="white", height=1, width=3, command=lambda: boutonClick(b8))
b9 = Button(frameGrille, relief="ridge", text=" ", font=("Arial", 60), bg="#363636", fg="white", height=1, width=3, command=lambda: boutonClick(b9))

#Positionnement des boutons sur la grille avec une boucle for qui prend chaque bouton et le place sur la grille
for x in range(0,9): 
      if x <= 2: #Pour les boutons de la première ligne           ##
            globals()['b%s' % (x+1)].grid(row=1, column=0+x)      # |
      elif x <= 5: #Pour les boutons de la seconde ligne          #  \     "globals()['b%s' % (x+1)]" permet de prendre chaque 
            globals()['b%s' % (x+1)].grid(row=2, column=0+x-3)    #  /    boutons 'b' et d'y ajouter la variable x de la boucle for
      else: #Pour les boutons de la dernière ligne                # |         afin de prendre chaque bouton : b1, b2, b3... 
            globals()['b%s' % (x+1)].grid(row=3, column=0+x-6)    ##

def rejouer():
      global partieFinie
      """ Cette fonction permet de rejouer """
      for i in range(1,10): #Boucle for pour prendre chaque boutons (b1, b2, b3, b4...) et les réactiver.
            globals()['b%s' % i].configure(state=NORMAL)
            globals()['b%s' % i]['text'] = " "

      global tourJoueur, nbTours #Déclaration des variables en "global" afin de pouvoir les modifier depuis cette fonction
      #On remet toutes les variables/textes par défaut
      tourJoueur = True
      nbTours = 0
      TexteTour['fg'] = 'white'
      TexteTour['text'] = "MORPION"
      if joueur1['score'] >= joueur2['score']:
            sousTexteTour['fg'] = joueur1['couleur']
            sousTexteTour['text'] = f"{joueur1['nom']} commence !"
      elif joueur2['score'] > joueur1['score']:
            sousTexteTour['fg'] = joueur2['couleur']
            sousTexteTour['text'] = f"{joueur2['nom']} commence !" 
      boutonRejouer.configure(state=DISABLED) #On désactive le bouton rejouer
      partieFinie = False

#Creation d'un bouton rejouer
boutonRejouer = Button(frameGrille, relief="ridge", text="REJOUER", font=("Arial", 32), bg="#363636", fg="white", width=10, command=rejouer)
boutonRejouer.grid(row=2, column=4, sticky=NE, padx=185, pady=25)

desactiveBoutons() #On désactive les boutons dés le début tant que le joueur n'a pas entré le nom des joueurs
boutonRejouer.configure(state=DISABLED)

#Affichage de la fenêtre
window.mainloop()