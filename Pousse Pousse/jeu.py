# PROGRAMMÉ PAR JOSEPH BOT #
#--------------------------#

#Importation des librairies python
from tkinter import*
from tkinter import messagebox, simpledialog
from tkinter.simpledialog import*
from PIL import Image
from random import shuffle, choice
from urllib.request import urlretrieve
import pickle
from random import*

#Création de la fenêtre
window = Tk()

#Personnalistion de la fenêtre
window.title("JEU POUSSE POUSSE")   # Titre de la fenêtre
window.geometry("1200x720")         # |
window.minsize(1200,720)            #  > Dimensionnement de la fênetre (avec une taille min/max) 
window.maxsize(1200,720)            # |
window.config(background="#2e2e2e") # Couleur de fond de la fenêtre

#Importation des images
imageGold = PhotoImage(file="Design\GoldIconWHITE.png").subsample(20,20)
imageGoldWon = PhotoImage(file="Design\GoldIconWHITE.png").subsample(27,27)
imgAccelerer = PhotoImage(file="Design\Icon-Accelerer.png").subsample(7)
imgRalentir = PhotoImage(file="Design\Icon-Ralentir.png").subsample(7)

afficheImage = ['']
rangeShop = 23


def jeu():
      global images, cooClick, melangeEnCours, isTimerOn, temps, ff, cooCaseBlanche, nbrMelange, gameZone, win, ff, directionChoisie, nbrMoves, melangeEnCours, vitesseRes, xGold, yGold, tempsAnimGoldIncome, goldWon, largeur, hauteur, pic, URL, cases, pts, yBS, xF, xS, mins, sec, goldWon, gold, directions, vitesseRes, solutionEnCours, tpsChargement, URL, cases, utiliseImageURL, affichage, decoupage, saveMorceauImage, grille, afficheImage, nBFrames, nBFramesClap, clapSpeed, clapTime, mdp, rangeShop
      #On crée une frame dans laquelle on placera le bouton solution ainsi que le text info pour pouvoir les passer sous le canvas
      frameBottom = Frame(window, bg="#2e2e2e", width=600, height=300)
      frameBottom.place(x=100, y=400)

      #Création d'un canvas
      canvas = Canvas(window, width=498, height=498, cursor="X_cursor", highlightthickness=2, highlightbackground="black")
      canvas.pack(side=LEFT, pady=50, padx=100)

      #Chargement de l'image
      pic = Image.open('pont.png')
      largeur, hauteur = pic.size

      def decoupage():
            """ Fonction qui découpe l'image choisie en une liste de 16 cases contenant les morceaux de l'image. """
            grid=[]
            for x in range(4):
                  for y in range(4):
                        box=(x*(largeur/4), y*(hauteur/4), x*(largeur/4)+(largeur/4), y*(hauteur/4)+(hauteur/4))
                        area = pic.crop(box)
                        #Création de la case blanche en haut a droite de l'image
                        if x == 3 and y == 0:
                              area = Image.new('RGB',(hauteur//4,largeur//4), (255,255,255))
                        area.save(f'image{y}{x}.png')
                        grid.append(f'image{y}{x}.png')
            return grid

      grille=[ [0, 1, 2, 3 ],
            [4, 5, 6, 7 ],
            [8, 9, 10,11],
            [12,13,14,15] ]

      #On fait une copie de la grille pour la condition de victoire
      grilleDeBase = [ [0, 1, 2, 3 ],
                  [4, 5, 6, 7 ],
                  [8, 9, 10,11],
                  [12,13,14,15] ]

      cases = decoupage()

      images=[]
      def saveMorceauImage():
            """ Fonction stockant des 16 morceaux de l'image dans une liste de 16 variables """
            global images
            for morceau in cases:
                  img = PhotoImage(file=morceau)
                  images.append(img)
      saveMorceauImage()

      def affichage(grid):
            """ Fonction recevant une matrice nommée grid (4*4) """
            for y in range(4):
                  for x in range(4): 
                        canvas.create_image(x*(largeur/4), y*(hauteur/4), image=images[grid[x][y]], anchor=NW)

      affichage(grille)

      def afficheImageURL(urlImage):
            """ Fonction prenant en entrée l'URL d'une image, découpe cette image et l'affiche sur la grille """
            global cases, images
            utiliseImageURL(urlImage, "image")
            
            #Suppression des morceaux de l'ancienne image
            canvas.delete('all')
            del cases[:], images[:]

            #On découpe ensuite l'image et on stock les 16 morceaux dans cases
            cases = decoupage()
            #On enregistre ensuite ceux-ci
            saveMorceauImage()
            affichage(grille) #Et on affiche la grille

      #On charge l'image choisie par l'utilisateur dansl a boutique
      if afficheImage[0] != '':
            afficheImageURL(afficheImage[0])

      #Definition de la tuple qui stockera les coordonnées de la case cliquée sur la grille.
      cooClick = ()

      gameZone = False
      win = False
      ff = False
      melangeEnCours = False

      def posClick(event):
            """ Fonction servant à determiné les coordonnées du morceau d'image sur lequel a cliqué l'utilisateur """
            global cooClick, melangeEnCours, isTimerOn #On globalise la variable afin qu'elle puisse être enregistrée hors de cette fonction

            if gameZone == True and win == False and ff == False and melangeEnCours == False:
                  canvas['cursor'] = "dot"
                  #On converti ces coordonnées en indices dans la grille de 4x4
                  for x in range(4): #Colonnes
                        if event.y > x*125 and event.y < 125+(x*125): #event.y récupère les coordonnées (en pixel par rapport a la taille de l'image) Y de l'emplacement du clique
                              cooClick = (x,)
                  for y in range(4): #Lignes
                        if event.x > y*125 and event.x < 125+(y*125): #event.x récupère les coordonnées X de l'emplacement du clique
                              cooClick = cooClick + (y,)

                  melangeEnCours = False #On met melangeEnCours a False lorsque le joueur clique sur le canvas
                  isTimerOn = True

                  #Quand l'utilisateur commence à jouer on retire le message
                  textInfo['text'] = ''

                  move(grille, cooClick[1], cooClick[0])
                  checkSiGagne(grille)

            #Affichage des fênetres de messages d'interdiction lorsque l'utilisateur clique sur le canvas a certains moments
            elif melangeEnCours == True: #Lorsque le mélange est en cours
                  canvas['cursor'] = "X_cursor" #On modifie le curseur
                  messagebox.showinfo('POUSSE-POUSSE',"Le jeu est en cours de mélange veuillez patienter.")
            elif gameZone == False: #Lorsque le jeu n'est pas mélangé
                  canvas['cursor'] = "X_cursor"
                  messagebox.showwarning('ATTENTION',"Vous devez d'abord mélanger le jeu !")
            elif solutionEnCours == True: #Lordque la résolution automatique est en cours
                  canvas['cursor'] = "X_cursor"
                  messagebox.showinfo('RÉSOLUTION AUTOMATIQUE',"Le jeu est en cours de résolution automatique, veuillez patienter.")
            elif ff == True: #Lorsque l'utilisateur à abandonné
                  canvas['cursor'] = "X_cursor"
                  messagebox.showerror('ERREUR',"Vous avez abandonné ! Appuyer de sur le bouton RÉINITIALISER pour recommencer une partie !\nOu prenez le temps de voir la résolution automatique en appuaynt sur le bouton SOLUTION !")
            elif win == True: #Lordque l'utilisateur a gagné
                  canvas['cursor'] = "star"
                  messagebox.showinfo('POUSSE-POUSSE',"Vous avez gagné la partie ! Appuyez de nouveau sur le bouton mélanger pour rejouer !")      

      #On déclanche la fonction 'posClick' lorsque l'utilisateur presse le bouton 'Button-1' (clique gauche)
      canvas.bind('<Button-1>', posClick)

      def abandon():
            """ Fonction pour abandonner et réinitialiser le jeu """
            global ff, cooCaseBlanche, isTimerOn, nbrMelange

            cooCaseBlanche = ()
            ff = True
            isTimerOn = False
            nbrMelange = 0

            #Désactivation du bouton et changement du curseur
            ffButton.configure(state=DISABLED)
            ffButtonBorder['highlightbackground'] = "grey"
            ffButton["cursor"] = "X_cursor"

            shuffleButton.configure(state=NORMAL) #Réactivation du bouton "mélange"
            shuffleButtonBorder['highlightbackground'] = "white" #Changement de la couleur de la frame (du contour du bouton)
            shuffleButton["cursor"] = "hand2"
            canvas['cursor'] = "X_cursor" #On change le curseur sur le canvas
            
            #On renome le bouton mélange
            shuffleButton['text'] = "RÉINITIALISER"
            #On fait apparaitre le bouton solution
            animButton(soluceButton, slowerButton, fasterButton, sens=True)

            #On crée une fonction pour afficher le texte 0.4secondes après
            def afficheTimedText():
                  textInfo['text'] = "Vous pouvez voir la solution ou reinitialiser le jeu" #On informe l'utilisateur des choix qui sont a sa disposition
            canvas.after(400, afficheTimedText)
      
      nbrMelange = 0

      def melangerJeu(grid): 
            """ Fonction s'exécutant lorsque l'utilisateur clique sur le bouton mélanger ou rejouer pour lancer le jeu et réinitialisant les variables, les boutons, etc... """
            global gameZone, win, ff, directionChoisie, nbrMoves, nbrMelange, melangeEnCours, vitesseRes

            #On réinitialise la grille lorsque l'utilisateur appuis sur le bouton "Réinitialiser" après avoir abandonné
            if grille != grilleDeBase:
                  vitesseRes = 0 #On réinitialise la grille instantanément
                  solution()

                  #On renome le bouton réinitialiser en MÉLANGER
                  shuffleButton['text'] = "MÉLANGER"
                  textInfo['text'] = ""
                  #On fait disparaître le bouton solution
                  animButton(soluceButton, slowerButton, fasterButton, sens=False)

            #Si la grille est réinitialisé alors on mélange
            else:
                  melangeEnCours = True
                  #On fait disparaître le bouton solution
                  animButton(soluceButton, slowerButton, fasterButton, sens=False)

                  vitesseRes = 500 #On réinitialise la vitesse de résolution
                  if win == True:
                        textInfo.config(font=("Arial", 14, "italic")) #On remet le style du texte par défaut si l'utilisateur avait gagné

                  #On ajoute un peu d'estétique en animant un texte informant l'utilisateur que le jeu est en cours de mélange
                  textInfo['text'] = "Mélange en cours, veuillez patienter"
                  animText(textInfo['text'], 200)
                  canvas['cursor'] = "dot" #On change le curseur

                  #On désactive le bouton mélanger et on change le curseur
                  shuffleButton.configure(state=DISABLED)
                  shuffleButtonBorder['highlightbackground'] = "grey"
                  shuffleButton["cursor"] = "X_cursor"

                  #On supprime tous les mouvements de la partie précédente
                  del directionChoisie [1:]     

                  #On réinitialise toutes les variables
                  gameZone = True
                  win = False
                  ff = False
                  nbrMoves = 0
                  textTemps['text'] = 'Temps : 0:00'
                  textMvt['text'] = 'MOVES : 0'

                  def melangePlusieursFois(grid):
                        """ Fonction servant a effectuer plusieurs fois le mélange """
                        global nbrMelange, melangeEnCours
                        if nbrMelange < 40:
                              motionsEmpty(grid)
                              nbrMelange += 1
                              canvas.after(15, lambda:melangePlusieursFois(grid))
                        else:
                              melangeEnCours = False  
            
                  melangePlusieursFois(grille)

      def openShop():
            global cooCaseBlanche, ff, isTimerOn, nbrMelange
            #On rénitialise les variables et on arrête le jeu
            cooCaseBlanche = ()
            ff = True
            isTimerOn = False
            nbrMelange = 0

            #On supprime tous les élements présent dans la fenêtre
            destroyWindow()
            #Et on lance le shop dans cette même fenêtre
            loadingScreen("Chargement de la boutique")

      tpsChargement = False

      def loadingScreen(txtChargement):
            """ Tout simplement un temps de chargement """
            global loadinglabel, imageLoadingLabel, tpsChargement
            #Personnalistion de la fenêtre
            window.title("POUSSE-POUSSE - SHOP - CHARGEMENT..")   # Titre de la fenêtre
            window.configure(background="#151515")
            tpsChargement = True

            imageLoadingLabel = PhotoImage(file="LoadingFrames/loadingFrame (1).png").subsample(4,4)
            loadingLabel = Label(window, image=imageLoadingLabel, border=0, highlightthickness=0)
            loadingLabel.place(x=363, y=180)

            #On affiche le texte "Chargement de la boutique..."
            textLoading = Label(window, text=txtChargement, font=("Arial", 14, 'italic'), bg="#151515", fg="white")
            textLoading.place(x=605, y=380, anchor=CENTER)
            nbrFrames = 0
            tpsLoad = 0
            finChargement = randint(40,130)

            loadingPts = []
            def animText():
                  """ Fonction animant les ... du texte de chargement """
                  if tpsChargement == True:
                        textLoading['text'] = f"{txtChargement}{''.join(loadingPts)}"
                        loadingPts.append(".")
                        if len(loadingPts) == 4:
                              del loadingPts[:]
                        window.after(finChargement*2, animText)
            animText()
      
            def startLoadingScreen(nbrFrames, tps):
                  """ Fonction faisant tourner en boucle chaque image du gif et une fois fini elle recommence """
                  global tpsChargement
                  try:
                        #Porte de sortie de la boucle infinie pour aller a la boutique
                        if tps > finChargement:
                              tpsChargement = False
                              #Suppression des élements de la fenêtre de chargement et initialisation de la boutique
                              destroyWindow()
                              shop()
                        tps += 1

                        #Changement de frame a chaque passage dans la boucle afin de recomposer le gif
                        nbrFrames += 1
                        imageLoadingLabel = PhotoImage(file=f"LoadingFrames/loadingFrame ({nbrFrames}).png").subsample(4,4)
                        loadingLabel.configure(image=imageLoadingLabel)
                        loadingLabel.photo = imageLoadingLabel
                        loadingLabel.place(x=363, y=180)

                  #Une fois tout le gif recomposé on recommence
                  except Exception:
                        nbrFrames = 1

                  window.after(1, lambda:startLoadingScreen(nbrFrames, tps))
            startLoadingScreen(nbrFrames, tpsLoad)

      #Utilisation d'une image personnalisée via un URL
      def utiliseImageURL(url, nom):
            """ Fonction prenant en entrée une URL d'image, et enregistre cette image afin de l'utiliser pour le jeu """
            global largeur, hauteur, pic
            urlretrieve(url, f'{nom}.png') #On télécharge l'image
            pic = Image.open(f"{nom}.png") #On l'ouvre
            pic = pic.resize((500,500)) #On la resize
            pic.save(f"{nom}.png") #On la ré-enregistre pour appliquer les modification du resize
            pic = Image.open(f'{nom}.png') #On la ré-ouvre 
            largeur, hauteur = pic.size #On récupère sa taille

      def chooseImageURL(): #Fonction lancant la fênetre de demande de l'URL
            """ Fonction affichant une fenêtre demandant l'URL de l'image souhaitée """
            global gold
            if grille == grilleDeBase:
                  windowURL = Toplevel() #Exemple typique de la non intuitivité de tkinter... si on met Tk() cela met une erreur lors de l'affichage de l'image ci dessous, et on est donc obligé de mettre 'Toplevel()' au lieu de Tk()...

                  #Personnalistion de la fenêtre
                  windowURL.title("POUSSE POUSSE - Jouer une image via URL")
                  windowURL.geometry("450x165")
                  windowURL.minsize(450,165)
                  windowURL.maxsize(450,165)
                  windowURL.config(background="#222222")
                  windowURL.wm_attributes("-topmost", 1) # On garde toujours la fenêtre au premier plan
                  
                  #Creation d'un entry
                  entryLabel = Label(windowURL, text="Entrez votre URL juste ci-dessous", font=("Arial", 15, "bold", "underline"), bg="#222222", fg="white")
                  entryLabel.place(x=55, y=15)
                  entryURL = Entry(windowURL, width=32, text="", font=("Arial", 16), bg="white", fg="#222222", border=0, highlightthickness=0)
                  entryURL.focus()
                  entryURL.place(x=30, y=55)

                  def confirmURL(): #Fonction exécutant le changement d'image
                        global gold
                        try:
                              #Soustraction et Sauvegarde du gold
                              gold -= 5000
                              textGold['text'] = gold
                              serialization()

                              #On affiche l'image et on l'enregistre pour pas qu'elle soit perdue lorsque l'utilisateur va a la boutique et revient
                              afficheImageURL(entryURL.get())
                              afficheImage[0] = entryURL.get()

                              windowURL.destroy()
                        except Exception:
                              messagebox.showerror("ERREUR","URL Incorrecte !")
                        
                  #Bouton Confirmer
                  confirmButtonURLBorder = Frame(windowURL, highlightthickness=1, highlightbackground="white") #On crée également une frame autour du bouton pour changer la couleur du contour de celui-ci
                  confirmButtonURLBorder.place(x=239, y=104, width=134, height=39)
                  confirmButtonURL = Button(windowURL, relief='ridge', cursor="hand2", image=imageGoldWon, compound=LEFT, text="5000", font=("Arial", 24,"bold"), bg="#222222", fg="white", border=0, highlightthickness=0, command=confirmURL)
                  confirmButtonURL.photo = imageGoldWon
                  confirmButtonURL.place(x=240, y=105, width=132, height=37)
                  
                  if gold < 5000:
                        confirmButtonURL.configure(state=DISABLED)
                        confirmButtonURLBorder.config(highlightbackground="grey")

                  #Bouton Annuler
                  cancelButtonURLBorder = Frame(windowURL, highlightthickness=1, highlightbackground="white") #On crée également une frame autour du bouton pour changer la couleur du contour de celui-ci
                  cancelButtonURLBorder.place(x=79, y=104, width=134, height=39)
                  cancelButtonURL = Button(windowURL, relief='ridge', cursor="hand2", text="ANNULER", font=("Arial", 14,"bold"), bg="#222222", fg="white", border=0, highlightthickness=0, command=windowURL.destroy)
                  cancelButtonURL.place(x=80, y=105, width=132, height=37)
            else:
                  messagebox.showerror("ERREUR","Il semblerait que votre grille ne soit pas réinitialisée !\nFinissez votre partie ou abandonnez et réinitialisée là pour changer d'image !")

      #Texte animé affichant le gold gagné
      goldWon = 0
      xGold = 1285
      yGold = 75
      textGoldWon = Label(window, text="+"+str(goldWon), font=("Arial", 21, "italic"), bg="#2e2e2e", fg="white")
      textGoldWon.place(x=xGold, y=yGold, anchor=E)
      goldIconWon = Label(window, image=imageGoldWon, bg="#2e2e2e")
      goldIconWon.place(x=xGold, y=yGold, anchor=E)

      #Variable stockant le gold
      gold = 5000 #Gold de base offert :)

      #------------------- Enregistrement du gold -------------------#

      #On importe le gold
      try: 
            with open('Saves\gold.txt', 'rb') as f:
                  gold = pickle.load(f)
            #On importe également la valeur de shopRange
            with open('Saves\easterEgg.txt', 'rb') as f:
                  rangeShop = pickle.load(f)

      #Si il n'y en a aucun dans le fichier (donc si il y a erreur) on enregistre 250 gold dans le fichier comme c'est la première fois que l'utilisateur lance le jeu
      except EOFError: 
            with open('Saves\gold.txt', 'wb') as f:
                  pickle.dump(gold, f)
            #Même chose pour le shopRange
            with open('Saves\easterEgg.txt', 'wb') as f:
                  pickle.dump(23, f)

      def serialization():
            """ Fonction enregistrant le gold de l'utilisateur dans un fichier texte """
            with open('Saves\gold.txt', 'wb') as f:
                  pickle.dump(gold, f)

      #---------------------------------- Barre de Navigation ----------------------------------#

      #Création d'une frame qui servira de barre
      navBar = Frame(window, bg="#222222", width=1200, height=54)
      navBar.place(x=0, y=0)

      #Barre blanche sous la barre de navigation
      barreBlanche = Frame(window, bg="#222222", height=1, width=1200, highlightthickness=1, highlightbackground='white')
      barreBlanche.place(x=0, y=54)
      
      #Text affichant le nombre de gold du joueur
      textGold = Label(navBar, text=gold, font=("Arial", 30, "bold"), bg="#222222", fg="white")
      textGold.place(x=1145, y=28, anchor=E)

      #Icone piece a gauche du texte affichant le gold
      goldIcon = Label(navBar, image=imageGold, bg="#222222")
      goldIcon.place(x=1200, y=26, anchor=E)

      #Bouton jouer avec URL
      frameButtonURLImage = Frame(navBar, bg="#222222", height=67, width=279, highlightthickness=1, highlightbackground='white')
      frameButtonURLImage.place(x=329, y=-5)
      urlImageButton = Button(navBar, relief='ridge', cursor="hand2", text="IMAGE PERSONNALISÉ (URL)", font=("Arial", 16, "bold"), bg="#222222", fg="white", height=3, width=25, border=0, highlightthickness=0, command=chooseImageURL)
      urlImageButton.place(x=0, y=-14)

      #Bouton pour ouvrir le shop
      shopButton = Button(navBar, relief='ridge', cursor="hand2", text="ALLER A LA BOUTIQUE", font=("Arial", 16, "bold"), bg="#222222", fg="white", height=3, width=21, border=0, highlightthickness=0, command=openShop)
      shopButton.place(x=330, y=-14)
      
      nBFrames = 0
      nBFramesClap = 0
      clapSpeed = 51
      clapTime = 0

      def password():
            global mdp
            #Mise en place du mot de passe
            mdp = "30025032"
            mdp = mdp + str(temps) + str(nbrMoves)

      def EasterEgg(event):
            """ Fonction mettant en place l'Easter Egg """
            global nBFrames, nBFramesClap, clapSpeed, clapTime, rangeShop
            destroyWindow()
            window.title("YOU DIDN'T SAID THE MAGIC WORD!")
            window.configure(bg="#151515")

            dennis = PhotoImage(file="Design/Dennis-1.png")
            dennisLabel = Label(window, image=dennis, cursor="hand2", border=0, highlightthickness=0)
            dennisLabel.place(x=300, y=280)

            entryMDPLabel = Label(window, text="VOUS N'AVEZ PAS DIT LE MOT MAGIQUE !", font=("Arial", 13, "bold"), bg="#151515", fg="white")
            entryMDPLabel.place(x=485, y=360)
            entryMDP = Entry(window, width=32, text="", font=("Arial", 16), bg="white", fg="#151515", border=0, highlightthickness=0, validate='all')
            entryMDP.focus()
            entryMDP.place(x=465, y=390)

            def runningGif():
                  """ Fonction affichant le gif """
                  global nBFrames
                  if nBFrames <= 1:
                        nBFrames += 1
                        dennis = PhotoImage(file=f"Design/Dennis-{nBFrames}.png")
                        dennisLabel.config(image=dennis)
                        dennisLabel.photo = dennis
                        dennisLabel.place(x=300, y=280)
                  else:
                        nBFrames = 0
                  window.after(250, runningGif)
            runningGif()

            def verifMdp(event):
                  """ Fonction vérifiant si le mot de passe est correct """
                  global rangeShop
                  print("entry")
                  print(entryMDP.get())
                  print(f"{int(mdp):b}")
                  if entryMDP.get() == f"{int(mdp):b}":
                        print("ok")
                        destroyWindow()
                        clapGif()
                        rangeShop = 26
                        with open('Saves\easterEgg.txt', 'wb') as f:
                              pickle.dump(26, f)
                        print("ok1")
            dennisLabel.bind('<Button-1>', verifMdp)

            def retourAuJeu():
                  """ Fonction permettant de retourner au jeu pousse-pousse """
                  #On supprime tous les élements présent dans la fenêtre
                  destroyWindow()

                  #On reconstruit ensuite le programme pincipal
                  window.title("JEU POUSSE POUSSE")
                  window.config(background="#2e2e2e")
                  jeu()

            def afficheEasterEgg():
                  """ Fonction affichant l'Easter Egg """
                  #Image Easter Egg
                  imgWonEasterEgg = PhotoImage(file='Design/EasterEgg/ImageEasterEgg.png').subsample(2,2)
                  imgWonEasterEggLabel = Label(window, image=imgWonEasterEgg, border=0, highlightthickness=0)
                  imgWonEasterEggLabel.photo = imgWonEasterEgg
                  imgWonEasterEggLabel.place(x=350, y=65)

                  #Creation d'un bouton pour retourner au jeu
                  doneButtonBorder = Frame(window, highlightthickness=1, highlightbackground="white") #On crée également une frame autour du bouton pour changer la couleur du contour de celui-ci
                  doneButtonBorder.place(x=464, y=594, width=272, height=57)
                  doneButton = Button(window, relief='ridge', cursor="hand2", text="RETOUR", font=("Arial", 28,"bold"), bg="#151515", fg="white", border=0, highlightthickness=0, command=retourAuJeu)
                  doneButton.place(x=465, y=595, width=270, height=55)

            clap = PhotoImage(file="Design/Clap/Clap-1.png").zoom(2,2)
            clapLabel = Label(window, image=clap, border=0, highlightthickness=0)
            clapLabel.photo = clap
            clapLabel.place(x=-550+4*clapTime, y=50)

            def clapGif():
                  """ Fonction faisant bouger un gif de gauche a droite """
                  global nBFramesClap, clapSpeed, clapTime
                  if nBFramesClap < 7:
                        nBFramesClap += 1
                        clap = PhotoImage(file=f"Design/Clap/Clap-{nBFramesClap}.png").zoom(2,2)
                        clapLabel = Label(window, image=clap, border=0, highlightthickness=0)
                        clapLabel.photo = clap
                        clapLabel.place(x=-550+4*clapTime, y=50)
                        clapTime += 1
                  else:
                        nBFramesClap = 0
                        if clapSpeed > 25:
                              clapSpeed -= 5
                              clapTime += 5
                  #Une fois l'animation sortie de la fenêtre on l'arrête
                  if -550+4*clapTime >= 950:
                        afficheEasterEgg()
                        return None
                  window.after(clapSpeed, clapGif)
                  
      #Bouton Easter Egg
      easterEggImage = PhotoImage(file='Design/easterEgg.png').subsample(7,7)
      easterEggButton = Label(navBar, cursor="hand2", image=easterEggImage, compound=LEFT, bg="#222222", fg="white", height=43, width=43, border=0, highlightthickness=0)
      easterEggButton.photo = easterEggImage
      easterEggButton.bind('<Button-1>', EasterEgg)
      #Barre blanche bouton Easter Egg
      barreEasterEgg = Frame(navBar, bg="#222222", height=55, width=1, highlightthickness=1, highlightbackground='white')

      def afficheBoutonEasterEgg():
            """ Fonction affichant le bouton permettant d'accèder a l'Easter Egg lors d'une victoire """
            #Ajustement de l'affichage en fonction du nombre de gold
            if gold > 1000 and gold < 10000:
                  barreEasterEgg.place(x=1040, y=27, anchor=E)
                  easterEggButton.place(x=1033, y=27, anchor=E)
            elif gold > 10000 and gold < 100000:
                  barreEasterEgg.place(x=1020, y=27, anchor=E)
                  easterEggButton.place(x=1013, y=27, anchor=E)
            elif gold > 100000:
                  barreEasterEgg.place(x=1000, y=27, anchor=E)
                  easterEggButton.place(x=993, y=27, anchor=E)

      tempsAnimGoldIncome = 0 #Variable servant de timer pour savoir quand le texte du gold gagné pourra monter

      def animGoldIncome():
            """ Fonction animation qui fait apparaître le texte indiquant le nombre de gold gagné depuis la droite de l'écran vers la gauche puis disparaissant vers le haut """
            global xGold, yGold, tempsAnimGoldIncome, goldWon

            shopButton.configure(state=DISABLED) #Désactivation du bouton pour aller a la boutique pendant l'animation de gain du gold
            tempsAnimGoldIncome += 1 #incrémentation du timer
            textGoldWon['text'] = "+"+str(goldWon) #On actualise le texte affichant le gold gagné

            if xGold > 1145:
                  xGold -= 4 #décrémentation de la position X du texte
                  #On déplace le texte ainsi que l'icone vers la gauche
                  textGoldWon.place(x=xGold ,y=yGold, anchor=E) 
                  goldIconWon.place(x=xGold+40 ,y=yGold, anchor=E)     

            #On fait monter ensuite le texte et l'icone, si le timer 'tempsAnimGoldIncome' atteint 1825 (1.8s)
            elif xGold < 1146 and yGold > 0 and tempsAnimGoldIncome > 1125:
                  yGold -= 2 #Décrémentation de la position Y du texte
                  #On déplace le texte ainsi que l'icone vers le haut
                  textGoldWon.place(x=xGold ,y=yGold, anchor=E)  
                  goldIconWon.place(x=xGold+40 ,y=yGold, anchor=E)   

            #Une fois le texte disparu sous la barre de navigation, on le retire et on réinitialise toutes les variables  
            elif yGold <= 0:
                  xGold = 1285
                  yGold = 75

                  #Réinitialisation de la position du texte ainsi que de l'icone a droite en dehors de la fênetre
                  textGoldWon.place(x=xGold ,y=yGold, anchor=E)
                  goldIconWon.place(x=xGold ,y=yGold, anchor=E)   

                  textGold['text'] = gold #On actualise également le texte affichant le gold
                  goldWon = 0 #Réintialisation du gold gagné
                  serialization() #Enregistrement du gold
                  tempsAnimGoldIncome = 0 #Réintialisation du timer
                  shopButton.configure(state=NORMAL) #Réactivation du bouton pour aller a la boutique

                  if rangeShop == 23: #On affiche le bouton Easter Egg si celui ci n'a pas encore été fait.
                        afficheBoutonEasterEgg() 

                  return None #On retourne rien pour finir la fonction

            #On attent 1ms et on relance ainsi la fonction en boucle
            window.after(1, animGoldIncome)

      #------------------------------------------------------------------------------------------#

      #Création d'un label pour dire le nombre de mouvements exécuté lors du jeu
      nbrMoves = 0 #Variable stockant le nombres de mouvements faits
      textMvt = Label(window, text="MOVES : 0", font=("Arial", 39, 'bold'), bg="#2e2e2e", fg="white")
      textMvt.place(x=867, y=155, anchor=CENTER)

      #Label affichant le temps
      textTemps = Label(window, text="Temps : 0:00", font=("Arial", 26,'underline'), bg="#2e2e2e", fg="white")
      textTemps.place(x=865, y=220, anchor=CENTER)

      #Création d'un bouton servant à exécuter la fonction melange() afin de mélanger le jeu
      shuffleButtonBorder = Frame(window, highlightthickness=1) #On crée une frame autour du bouton pour changer la couleur du contour de celui-ci
      shuffleButtonBorder.place(x=729, y=319, width=282, height=62) 
      shuffleButton = Button(window, relief='ridge', text="MÉLANGER", font=("Arial", 22, 'bold'), cursor="hand2", bg="#222222", fg="#f1f1f1", border=0, highlightthickness=0, command=lambda:melangerJeu(grille))
      shuffleButton.place(x=730, y=320, width=280, height=60)

      #Création d'un bouton pour abandonner et réinitialiser le jeu
      ffButtonBorder = Frame(window, highlightthickness=1, highlightbackground="grey") #On crée également une frame autour du bouton pour changer la couleur du contour de celui-ci
      ffButtonBorder.place(x=729, y=389, width=282, height=62)
      ffButton = Button(window, relief='ridge', text="ABANDONNER", font=("Arial", 22, 'bold'), cursor="hand2", bg="#222222", fg="#f1f1f1", border=0, highlightthickness=0, state=DISABLED, command=abandon)
      ffButton.place(x=730, y=390, width=280, height=60)

      #Création d'un bouton pour à quitter le jeu
      leaveButtonBorder = Frame(window) #On crée également une frame autour du bouton pour changer la couleur du contour de celui-ci
      leaveButtonBorder.place(x=729, y=459, width=282, height=62) 
      leaveButton = Button(window, relief='ridge', text="QUITTER", font=("Arial", 22, 'bold'), cursor="X_cursor", bg="#222222", fg="white", border=0, highlightthickness=0, command=window.destroy)
      leaveButton.place(x=730, y=460, width=280, height=60)

      #Texte chargement/Info sous le canvas
      textInfo = Label(frameBottom, text="", font=("Arial", 14, 'italic'), bg="#2e2e2e", fg="white")
      textInfo.place(x=250, y=225, anchor=CENTER)

      pts = []
      def animText(text, vitAnim):
            """ Fonction animant les ... d'un texte """
            global pts
            #On joue l'animation en retirant et en ajoutant des points a la fin de la phrase
            if melangeEnCours == True or solutionEnCours == True or tpsChargement == True:
                  textInfo['text'] = f"{text}{''.join(pts)}"
                  pts.append(".")
                  if len(pts) == 4:
                        del pts[:]
                  window.after(vitAnim, lambda:animText(text, vitAnim))
            elif ff == False and tpsChargement == False: 
                  #Quand le mélange est fini on dis a l'utilisateur qu'il peut commencer a jouer
                  textInfo['text'] = "Appuyez sur un case pour commencer a jouer"
            else:
                  textInfo['text'] = "" #Sinon on enleve le texte

      yAnimBottomWidget = 0
      animationEnCours = False

      def animButton(button,bm,bp, sens):
            """ Fonction faisant passer en dessous du canvas un bouton en l'animant """
            global yBS, xF, xS
            #On fait sortir le boutton d'en dessous du canvas
            if yBS < 270 and sens == True:
                  yBS += 1
                  #On déplace le bouton solution ainsi que les boutons pour accelerer/ralentir en même temps vers le bas
                  button.place(x=250,y=yBS, anchor=CENTER) 
                  soluceButtonBorder.place(x=250,y=yBS, anchor=CENTER)
                  bp.place(x=xF,y=yBS, anchor=CENTER)       
                  bm.place(x=xS,y=yBS, anchor=CENTER) 
                  window.after(2, lambda:animButton(button, bm, bp, sens=True))
            #On fait rentrer le boutton en dessous du canvas
            elif yBS > 175 and sens == False:
                  #On ne remonte pas le bouton tant que les autres ne sont pas rentré dans celui-ci
                  yBS -= 0
                  if xF <= 360: #On utilise les coordonnées x d'un des 2 boutons pour dire a partir de quand celui-ci peut monter
                        yBS -= 1
                  # On déplace le bouton solution ainsi que les boutons pour accelerer/ralentir en même temps vers le haut
                  button.place(x=250,y=yBS, anchor=CENTER)  
                  soluceButtonBorder.place(x=250,y=yBS, anchor=CENTER)
                  bp.place(x=xF,y=yBS, anchor=CENTER)       
                  bm.place(x=xS,y=yBS, anchor=CENTER)       
                  window.after(2, lambda:animButton(button, bm, bp, sens=False)) #On attend 2secondes puis on ré-exécute la fonction

            def animButtonPlus(sens):
                  """ Fonction faisant sortir a droite du bouton solution, un bouton pour accelerer la résolution automatique """
                  global xF
                  #On fait glisser le bouton a droite
                  if xF < 425 and sens == True:
                        xF += 1 #incrémentation de 1 de la position x du bouton, le faisant se déplacé d'1 pixel vers la droite
                        bp.place(x=xF,y=yBS, anchor=CENTER)
                        window.after(2, lambda:animButtonPlus(sens=True))
                  #On le re glisse a gauche pour le cacher sous le bouton solution
                  elif xF > 280 and sens == False:
                        xF -= 1 #décrémentation de 1 de la position x du bouton, le faisant se déplacé d'1 pixel vers la gauche
                        bp.place(x=xF,y=yBS, anchor=CENTER)
                        window.after(1, lambda:animButtonPlus(sens=False))

            def animButtonMoins(sens):
                  """ Fonction faisant sortir a gauche du bouton solution, un bouton pour ralentir la résolution automatique """
                  global xS
                  #On fait glisser a gauche
                  if xS > 75 and sens == True:
                        xS -= 1 #décrémentation de 1 de la position x du bouton, le faisant se déplacé d'1 pixel vers la gauche
                        bm.place(x=xS,y=yBS, anchor=CENTER)
                        window.after(2, lambda:animButtonMoins(sens=True))
                  #On le re glisse a droite pour le cacher sous le bouton solution
                  elif xS < 220 and sens == False:
                        xS += 1 #incrémentation de 1 de la position x du bouton, le faisant se déplacé d'1 pixel vers la droite
                        bm.place(x=xS,y=yBS, anchor=CENTER)
                        window.after(1, lambda:animButtonMoins(sens=False))

            #On sort les boutons
            if yBS == 200 and sens == True:
                  animButtonPlus(sens=True)
                  animButtonMoins(sens=True)
            #On rentre les boutons
            elif sens == False:
                  animButtonPlus(sens=False)
                  animButtonMoins(sens=False)

      #Definition des variables utilisée pour la fonction timer()
      isTimerOn = True
      sec = 0
      mins = 0
      x = ""
      temps = 0

      def timer():
            global mins, sec, temps
            if isTimerOn == True:
                  sec += 1 #incrémantation des secondes de 1
                  if sec < 10: #On ajoute un 0 tant que les secondes sont en dessous de 10
                        x = "0"
                  else:
                        x = ""
                  textTemps['text'] = f"Temps : {mins}:{x}{sec}"
                  #Si les secondes atteigent 59 on incrémente les minutes de 1 et on redéfini les secondes a 0
                  if sec == 59:
                        mins += 1
                        sec = 0
                  #On re-exécute la fonction toutes les secondes
                  window.after(1000, timer)
            #On fait un else puisque le booléen est 'False' seulement quand on gagne/abandonne, on réinitialise les variales des minutes et secondes
            else:
                  temps = mins*60+sec #On converti tout en secondes puis on stocke le temps pour l'utiliser afin de comptabiliser les points gagnés
                  sec = -1
                  mins = 0

      def calculGold():
            """ Calcul des points obtenus en fonction du temps et des mouvements faits par l'utilisateur. """
            global goldWon, nbrMoves, gold
            #Points gagnés en fonction du temps passé 
            if temps < 150:
                  goldWon = randint(900,1800)
            elif temps < 300:
                  goldWon = randint(750,1500)
            elif temps < 420:
                  goldWon = randint(600,1200)
            elif temps < 600:
                  goldWon = randint(500,1000)
            elif temps < 900:
                  goldWon = randint(400,800)
            else: 
                  goldWon = randint(300,800)

            #Points gagnés en fonction du nombre de mouvements faits
            if nbrMoves < 55:
                  goldWon += randint(900,1800)
            elif nbrMoves < 80:
                  goldWon += randint(750,1500)
            elif nbrMoves < 100:
                  goldWon += randint(600,1200)
            elif nbrMoves < 115:
                  goldWon += randint(500,1000)
            elif nbrMoves < 135:
                  goldWon += randint(400,800)
            else: 
                  goldWon += randint(300,800)

            nbrMoves = 0
            gold += goldWon
            animGoldIncome()

      #--------------------------------------------------------------#

      #On défini un tuple qui servira a stocker les coordonnées ligne/colonne de la case blanche.
      cooCaseBlanche = ()

      directionChoisie = [""]

      def posEmpty(grid):
            """ Fonction retournant sous forme de tuple les coordonnées de la position de la case blanche """
            global cooCaseBlanche
            #On parcours la liste "grid" afin de trouver le numéro correspondant a la case blanche donc le 12 et une fois trouvé on utilise les indices x et y des boucles for pour former les coordonnées.
            for y in range(4):
                  for x in range(4):
                        if grid[x][y] == 12:
                              cooCaseBlanche = (x,y)

      def move(grid, ligne, colonne):
            """ Fonction qui dit si la case de la ligne et de la colonne données se trouve à coté de la case blanche """
            global directionChoisie
            posEmpty(grid)

            #On vérifie si la ligne et la colonne saisie est a coté de la case blanche en ajoutant/
            if colonne == cooCaseBlanche[1]+1 and ligne == cooCaseBlanche[0] and ligne <= 3: #NORD
                  echange(grid, ligne, colonne)
                  directionChoisie.append("SUD") #On ajoute la direction choisie par l'utilisateur afin de pouvoir refaire tous les mouvements pour la résolution automatique
                  #return print("NORD")
            elif colonne == cooCaseBlanche[1]-1 and ligne == cooCaseBlanche[0] and ligne >= 0: #SUD
                  echange(grid, ligne, colonne)
                  directionChoisie.append("NORD")
                  #return print("SUD")
            elif colonne == cooCaseBlanche[1] and ligne == cooCaseBlanche[0]-1 and colonne >= 0: #EST
                  echange(grid, ligne, colonne)
                  directionChoisie.append("OUEST")
                  #return print("EST")
            elif colonne == cooCaseBlanche[1] and ligne == cooCaseBlanche[0]+1 and colonne <= 3: #OUEST
                  directionChoisie.append("EST")
                  echange(grid, ligne, colonne)
                  #return print("OUEST")
            else:
                  return print("NON ADJACENTE")


      def echange(grid, ligne, colonne):
            """ Fonction servant a échanger la case blanche et la case cliquée si celles-ci sont adjacentes """
            global nbrMoves, isTimerOn
            #On l'échange avec la case blanche puis on remplace l'ancienne case blanche par la case selectionnée
            grid[ligne][colonne], grid[cooCaseBlanche[0]][cooCaseBlanche[1]] = grid[cooCaseBlanche[0]][cooCaseBlanche[1]], grid[ligne][colonne]

            #Une fois le mélange fini on lance le timer lorsque l'utilisateur aura cliqué sur une case et on incrémente de 1 a chaque fois
            if melangeEnCours == False and solutionEnCours == False:
                  if isTimerOn == True and nbrMoves == 0:
                        #On lance le timer
                        timer()
                  #On incrémente de 1 le nombre de mouvements a chaque échange
                  nbrMoves += 1
                  textMvt['text'] = f"MOVES : {nbrMoves}"
                  #On réactive également le bouton pour abandonner
                  ffButton.configure(state=NORMAL)
                  ffButtonBorder['highlightbackground'] = "white" #Changement de la couleur de la frame (donc du contour du bouton)
                  ffButton["cursor"] = "X_cursor"

            #On supprime l'ancien canvas avant d'afficher le nouveau
            canvas.delete('all')
            affichage(grid)

      #On crée une liste pour y stocker les directions possibles
      directions = []

      def motionsEmpty(grid):
            """ Fonction retournant la liste des directions des déplacements possibles de la case blanche """
            global directions
            posEmpty(grid)

            ligne = cooCaseBlanche[0]
            colonne = cooCaseBlanche[1] 

            #On ajoute 1 ou on soustrait 1 aux lignes et aux colonnes et on regarde si elles sont toujours entre 0 et 3 pour vérifier si l'échange est possible
            if ligne+1 > 0 and ligne+1 <= 3: #EST
                  directions.append("EST")
            if colonne+1 > 0 and colonne+1 <= 3: #SUD
                  directions.append("SUD")
            if ligne-1 >= 0 and ligne-1 <= 3: #OUEST
                  directions.append("OUEST")
            if colonne-1 >= 0 and colonne-1 <= 3:#NORD
                  directions.append("NORD")
            #print(directions)

            melange(grille)

      def melange(grid):
            """ Fonction permettant le mélange automatique, prenant en entré la liste des directions possibles et en prenant une au harsard parmi celles-ci puis faisant l'échange automatiquement """
            global directionChoisie, directions
            posEmpty(grid)

            if solutionEnCours == False:
                  choixDirection = choice(directions)
                  #On refait le choix tant que ça fait des allés retour
                  while choixDirection == "EST" and directionChoisie[-1] == "OUEST" or choixDirection == "OUEST" and directionChoisie[-1] == "EST" or choixDirection == "SUD" and directionChoisie[-1] == "NORD" or choixDirection == "NORD" and directionChoisie[-1] == "SUD":
                        choixDirection = choice(directions)
                  directionChoisie.append(choixDirection)

            #On regarde quelle est la direction choisie au hasard et on défini des coordonnées par rapport à celle-ci et par rapport a la case blanche en ajoutant/soutrayant 1
            if directionChoisie[-1] == "EST" and solutionEnCours == False or solutionEnCours == True and directions[0] == "OUEST": #Si solution en cours, on inverse la direction, le nord devient sud et ainsi de suite afin de reproduire tous les mouvements a l'envers
                  echange(grid, cooCaseBlanche[0]+1, cooCaseBlanche[1])
            elif directionChoisie[-1] == "SUD" and solutionEnCours == False or solutionEnCours == True and directions[0] == "NORD":
                  echange(grid, cooCaseBlanche[0], cooCaseBlanche[1]+1)
            elif directionChoisie[-1] == "OUEST" and solutionEnCours == False or solutionEnCours == True and directions[0] == "EST":
                  echange(grid, cooCaseBlanche[0]-1, cooCaseBlanche[1])
            elif directionChoisie[-1] == "NORD" and solutionEnCours == False or solutionEnCours == True and directions[0] == "SUD":
                  echange(grid, cooCaseBlanche[0], cooCaseBlanche[1]-1)   

            #On réinitialise la liste des directions
            del directions[:]

      def fasterSoluce():
            """ Fonction permettant d'augmenter la vitesse de la resolution automatique """
            global vitesseRes
            if vitesseRes > 100:
                  vitesseRes -= 100
            elif vitesseRes < 100 and vitesseRes > 25:
                  vitesseRes -= 25

      def slowerSoluce():
            """ Fonction permettant de baisser la vitesse de la resolution automatique """
            global vitesseRes
            if vitesseRes < 550:
                  vitesseRes += 100
            elif vitesseRes > 550 and vitesseRes < 2000:
                  vitesseRes += 250 

      #Definition du bouton permettant d'accelerer la résolution automatique
      yF = 175; xF = 280 #Position x et y
      fasterButton = Button(frameBottom, image=imgAccelerer, relief='ridge', text="", font=("Arial", 22), cursor="sb_right_arrow", bg="#2e2e2e", fg="black", border=0,command=fasterSoluce)
      fasterButton.place(x=425, y=yF, width=60, height=60, anchor=CENTER)

      #Definition du bouton permettant de ralentir la résolution automatique
      yS = 175; xS = 220 #Position x et y
      slowerButton = Button(frameBottom, image=imgRalentir, relief='ridge', text="", font=("Arial", 22), cursor="sb_left_arrow", bg="#2e2e2e", fg="black", border=0, command=slowerSoluce)
      slowerButton.place(x=75, y=yS, width=60, height=60, anchor=CENTER)

      solutionEnCours = False
      vitesseRes = 500 #Vitesse de Résolution

      def solution():
            """ Fonction qui montre a l'utilisateur la solution en faisant tous les déplacements du mélange et de l'utilisateur à l'envers pour revenir au point de départ """
            global directionChoisie, directions, solutionEnCours, nbrMoves
            solutionEnCours = True
            #Tout d'abord on désactive le bouton réinialiser pendant la résolution automatique
            shuffleButton.configure(state=DISABLED)
            shuffleButtonBorder['highlightbackground'] = "grey"
            soluceButton.configure(state=DISABLED) #On désactive également le bouton solution
      
            #On change les curseurs
            soluceButton['cursor'] = "X_cursor"
            canvas['cursor'] = "watch"

            #On ajoute un texte et on l'anime
            if nbrMoves != 0 and vitesseRes != 0: #Pour faire en sorte que ça lance l'animation du texte qu'une seule fois, on utilise en condition une variable quelconque qui va être réinitialiser et si la résolution auto n'est pas instantanée
                  textInfo['text'] = "Résolution Automatique en cours"
                  animText(textInfo['text'], 275)

            #On réinitialise
            nbrMoves = 0
            textTemps['text'] = 'Temps : 0:00'
            textMvt['text'] = 'MOVES : 0'
            #Tant que la lite n'est pas égale a 1 on prend chacune des directions choisies dans la liste a l'envers, puis on le supprime de la liste et on l'inverse pour aller en arrière
            if len(directionChoisie) != 1:
                  directions.append(directionChoisie[-1])
                  del directionChoisie[-1]
                  melange(grille)
                  canvas.after(vitesseRes, solution) #Après 'vitesseRes' choisie (en millisecondes) on ré-exécute la fonction solution jusqu'a ce qu'il ne reste plus qu'une direction dans la liste direction choisie
            else:
                  solutionEnCours = False

                  #On renome encore une fois le bouton réinitialiser en "REJOUER" et puis on le ré-active
                  shuffleButton['text'] = "REJOUER"
                  shuffleButton.configure(state=NORMAL)
                  shuffleButtonBorder['highlightbackground'] = "white" #Changement de la couleur de la frame (du contour du bouton)

                  #Reactivation du bouton solution
                  soluceButton.configure(state=NORMAL)
                  soluceButton['cursor'] = "hand2"

                  #On fait disparaitre le bouton solution
                  animButton(soluceButton, slowerButton, fasterButton, sens=False)
                  textInfo['text'] = ""
                  canvas['cursor'] = "X_cursor"

      #Bouton solution
      yBS = 175 #Variable yBoutonSoluce stockant l'emplacement vetical du bouton solution
      soluceButtonBorder = Frame(frameBottom, highlightthickness=1) #On crée également une frame autour du bouton pour changer la couleur du contour de celui-ci
      soluceButtonBorder.place(x=249, y=yBS-1, width=282, height=60, anchor=CENTER) 
      soluceButton = Button(frameBottom, relief='ridge', text="SOLUTION", font=("Arial", 22, 'bold'), cursor="hand2", bg="#222222", fg="#f1f1f1", border=0, highlightthickness=0, highlightbackground="white", command=solution)
      soluceButton.place(x=250, y=yBS, width=280, height=58, anchor=CENTER)

      def checkSiGagne(grid):
            """ Fonction vérifiant si la grille est complète """
            global win, isTimerOn, nbrMelange
            #Si la grille est égale a la grille de base et à condition que le jeu n'est pas en cours de mélange
            if grid == grilleDeBase and melangeEnCours == False:
                  isTimerOn = False #Arret du timer
                  timer()
                  password() #Calcul du mot de passe pour l'easter egg

                  win = True
                  calculGold() #Calcul des points gagnés
                  nbrMelange = 0
                  canvas['cursor'] = "star"

                  #Desactivation du bouton Abandonner, on réactive et on renome le bouton mélanger en 'Rejouer'
                  ffButton.configure(state=DISABLED)
                  ffButtonBorder['highlightbackground'] = "grey" #Changement de la couleur de la frame (du contour du bouton)
                  shuffleButton.configure(state=NORMAL)
                  shuffleButtonBorder['highlightbackground'] = "white"
                  shuffleButton['text'] = "REJOUER"   
                  
                  #On affiche le message de victoire
                  messagebox.showinfo("POUSSE POUSSE",f"Bravo vous avez réussi")
                  textInfo['text'] = f"BIEN JOUÉ ! VOUS AVEZ RÉUSSI !"
                  textInfo.config(font=("Arial", 14, "bold", "underline")) #On met le texte en GRAS et on le SOULIGNE


def destroyWindow():
      """ Fonction supprimant tous les élements présents dans la fenêtre """
      def all_children():
            listeWidgets = window.winfo_children()

            for element in listeWidgets:
                  if element.winfo_children():
                        listeWidgets.extend(element.winfo_children())

            return listeWidgets
      widget_list = all_children()
      for element in widget_list:
            element.destroy()
jeu()



def shop():
      """ Boutique du jeu """
      global gold, goldLost, xFrame, xGoldLost, yGoldLost, tempsAnimGoldLost, goldLost, timerNotEnoughtAnim, sens, afficheImage

      #Personnalistion de la fenêtre
      window.title("POUSSE-POUSSE - SHOP - Acheter des images")   # Titre de la fenêtre
      window.configure(background="#222222")

      #Texte affichant le titre de la fênetre
      titleText = Label(window, text="BIENVENUE DANS LA BOUTIQUE !", font=("Arial", 36,"bold"), bg="#222222", fg="white")
      titleText.place(x=175, y=85)

      #Texte animé affichant le gold gagné
      goldLost = 0
      xGoldLost = 1285
      yGoldLost = 75
      textGoldLost = Label(window, text="-"+str(goldLost), font=("Arial", 21, "italic"), bg="#222222", fg="red")
      textGoldLost.place(x=xGoldLost, y=yGoldLost, anchor=E)
      imageGoldLost = PhotoImage(file="Design\GoldIconWHITE.png").subsample(27,27)
      goldIconLost = Label(window, image=imageGoldLost, bg="#222222")
      goldIconLost.place(x=xGoldLost+40, y=yGoldLost, anchor=E)

      #Création d'une frame qui servira de barre
      navBar = Frame(window, bg="#222222", width=1200, height=54)
      navBar.place(x=0, y=0)

      #Bouton jouer avec URL
      frameButtonURLImage = Frame(navBar, bg="#222222", height=67, width=279, highlightthickness=1, highlightbackground='white')
      frameButtonURLImage.place(x=329, y=-5)
      urlImageButton = Button(navBar, relief='ridge', cursor="hand2", text="IMAGE PERSONNALISÉ (URL)", font=("Arial", 16, "bold"), bg="#222222", fg="white", height=3, width=25, border=0, highlightthickness=0, state=DISABLED)
      urlImageButton.place(x=0, y=-14)

      #Bouton pour ouvrir le shop
      shopButton = Button(navBar, relief='ridge', cursor="hand2", text="ALLER A LA BOUTIQUE", font=("Arial", 16, "bold"), bg="white", fg="#222222", height=3, width=21, border=0, highlightthickness=0)
      shopButton.place(x=330, y=-14)

      #Barre blanche
      barreBlanche = Frame(window, bg="#222222", height=2, width=1200, highlightthickness=2, highlightbackground='white')
      barreBlanche.place(x=0, y=54)

      def exitShop():
            #On supprime tous les élements présent dans la fenêtre
            destroyWindow()

            #On reconstruit ensuite le programme pincipal
            window.title("JEU POUSSE POUSSE")
            window.config(background="#2e2e2e")
            jeu()
            
      #Création d'un bouton permettant de valider et de quitter la fenêtre
      confirmButtonBorder = Frame(window, highlightthickness=1, highlightbackground="white") #On crée également une frame autour du bouton pour changer la couleur du contour de celui-ci
      confirmButtonBorder.place(x=464, y=609, width=272, height=77)
      confirmButton = Button(window, relief='ridge', cursor="hand2", text="CONFIRMER", font=("Arial", 28,"bold"), bg="#222222", fg="white", border=0, highlightthickness=0, command=exitShop)
      confirmButton.place(x=465, y=610, width=270, height=75)     

      #Creation d'une frame qui servira de cadre pour le textNotEnought
      xFrame = -380
      frameTextNE = Frame(window, bg="#222222", width=380, height=40, highlightthickness=2, highlightbackground="red")
      frameTextNE.place(x=xFrame, y=620)

      #Creation d'un Label indiquant a l'utilisateur qu'il n'a pas assez de gold
      textNotEnought = Label(frameTextNE, text="VOUS N'AVEZ PAS ASSEZ DE GOLD !", font=("Arial", 15, "bold"), bg="#222222", fg="white")
      textNotEnought.place(x=5, y=4)

      #Text affichant le nombre de gold du joueur
      textGold = Label(window, text=gold, font=("Arial", 30, "bold"), bg="#222222", fg="white")
      textGold.place(x=1145, y=28, anchor=E)

      #Icone piece a gauche du texte affichant le gold
      imageGold = PhotoImage(file="Design\GoldIconWHITE.png").subsample(19,19)
      goldIcon = Label(window, image=imageGold, bg="#222222")
      goldIcon.place(x=1200, y=25, anchor=E)
 
      sens = True
      timerNotEnoughtAnim = 0
      def notEnoughtAnim():
            """ Fonction faisant sortir a depuis le bord SW, un texte disant a l'utilisateur qu'il n'a pas assez de gold"""
            global xFrame, timerNotEnoughtAnim, sens
            timerNotEnoughtAnim += 1
            #On fait glisser a gauche
            if xFrame < -5 and sens == True:
                  xFrame += 4 #Incrémentation de 1 de la position x du bouton, le faisant se déplacé d'1 pixel sur la droite
                  frameTextNE.place(x=xFrame,y=620)
            #On le re glisse a droite pour le cacher sous le bouton solution
            elif xFrame >= -5 and timerNotEnoughtAnim > 800 or sens == False and xFrame >= -380 and timerNotEnoughtAnim > 800:
                  sens = False
                  xFrame -= 5 #Décrémentation de 1 de la position x du bouton, le faisant se déplacé d'1 pixel sur la gauche
                  frameTextNE.place(x=xFrame,y=620)
            #Une fois l'animation finie on arrête tout
            elif xFrame < -370:
                  sens = True
                  timerNotEnoughtAnim = 0
                  return None
            window.after(1, notEnoughtAnim)

      #------------------------- ScrollBar ------------------------#

      #On crée un canvas (seul moyen d'avoir une scrollbar avec des Labels) pour y mettre la frame avec les images 
      shopCan = Canvas(window, bg="#363636", width=1206, height=400)
      shopCan.place(x=-5, y=175)

      #On défini une frame dans le Canvas dans laquelle on y mettera les images
      shopFrame = Frame(shopCan, bg="#363636", width=1201, height=400, highlightthickness=0)
      shopCan.create_window(0, 0, window=shopFrame) #Affichage de la frame dans le canvas

      #On redimensionne la scrollbar en fonction de la largeur du canvas
      def config(event):
            shopCan.configure(scrollregion=shopCan.bbox('all'))
      shopFrame.bind('<Configure>', config)

      #On défini la scrollbar et on l'ajuste
      SBar = Scrollbar(window, command=shopCan.xview, orient=HORIZONTAL)
      SBar.place(relx=0, relwidth=1, anchor=SW, y=580)
      shopCan.configure(xscrollcommand=SBar.set)

      #----------------------- Fin ScrollBar ----------------------#

      #Liste des prix de chaques images disponnibles a l'achat
      couts = [500,1000,1500,2000,2500,3000,4000,4500,5500,7000,8000,9000,10000,11500,13000,15000,17500,25000,30000,35000,40000,50000,100000,gold,399]
      imagesURL = ["https://i.imgur.com/YU1zseP.gif","https://i.imgur.com/hrROXWA.png","https://i.imgur.com/ZUGwNsh.png","https://i.imgur.com/F37xK53.png","https://i.imgur.com/O2mkA01.png","https://i.imgur.com/MmLayXn.png","https://i.imgur.com/PsT0SQw.png","https://i.imgur.com/XLtaYV8.png","https://i.imgur.com/s5CWt2P.png","https://i.imgur.com/A1DpsYI.png","https://i.imgur.com/nALUfIo.png","https://i.imgur.com/ZIxNLKZ.png","https://i.imgur.com/HWeBMmX.png","https://i.imgur.com/7ZxqIds.png","https://i.imgur.com/mz9KKDX.png","https://i.imgur.com/iDrZthc.png","https://i.imgur.com/INfIqcp.png","https://i.imgur.com/oWoMNqg.png","https://i.imgur.com/hQXJK6r.png","https://i.imgur.com/ex6zKJK.png","https://i.imgur.com/fPntKtU.png","https://i.imgur.com/5WNvwGn.jpg","https://i.imgur.com/qTIAp8G.png","https://i.imgur.com/qlhigXI.png","https://i.imgur.com/lJ8bbuL.png"]

      #On crée une liste qui stockera tous les indices des images achetées
      imagesBought = []


      #------------------- Enregistrement Achats ------------------#

      #On importe les données enregistrée de la liste 'imagesBought'
      try: 
            with open('Saves\imagesBought.txt', 'rb') as f:
                  imagesBought = pickle.load(f)
      #Si il n'y en a aucune (donc si il y a erreur) on enregistre la liste vide
      except EOFError: 
            with open('Saves\imagesBought.txt', 'wb') as f:
                  pickle.dump(imagesBought, f)

      def serialization():
            """ Fonction enregistrant l'indice de l'image achetée se trouvant dans la liste 'imagesBought' """
            with open('Saves\imagesBought.txt', 'wb') as f:
                  pickle.dump(imagesBought, f)


      #-------------------- Enregistrement Gold -------------------#

      def goldSerialization():
            """ Fonction enregistrant le gold de l'utilisateur dans un fichier texte """
            with open('Saves\gold.txt', 'wb') as f:
                  pickle.dump(gold, f)

      tempsAnimGoldLost = 0

      def animAchat():
            """ Fonction animation qui fait apparaître le texte indiquant le nombre de gold perdu depuis la droite de l'écran vers la gauche puis disparaissant vers le haut """
            global xGoldLost, yGoldLost, tempsAnimGoldLost, goldLost

            #On désactive le bouton confirmer pendant la transaction
            confirmButton.configure(state=DISABLED)
            confirmButtonBorder.config(highlightbackground='grey')

            tempsAnimGoldLost += 1 #Incrémentation du timer
            textGoldLost['text'] = "-"+str(goldLost) #On actualise le texte affichant le gold
            if xGoldLost > 1145:
                  xGoldLost -= 4 #décrémentation de la position X du texte
                  #On déplace le texte ainsi que l'icone vers la gauche
                  textGoldLost.place(x=xGoldLost ,y=yGoldLost, anchor=E) 
                  goldIconLost.place(x=xGoldLost+40 ,y=yGoldLost, anchor=E)     

            #On fait monter ensuite le texte et l'icone, si le timer 'tempsAnimGoldIncome' atteint 1825 (1.8s)
            elif xGoldLost < 1146 and yGoldLost > 0 and tempsAnimGoldLost > 1325:
                  yGoldLost -= 2 #Décrémentation de la position Y du texte
                  #On déplace le texte ainsi que l'icone vers le haut
                  textGoldLost.place(x=xGoldLost ,y=yGoldLost, anchor=E)  
                  goldIconLost.place(x=xGoldLost+40 ,y=yGoldLost, anchor=E)   

            #Une fois le texte disparu sous la barre de navigation, on le retire et on réinitialise toutes les variables  
            elif yGoldLost <= 0:
                  xGold = 1285
                  yGold = 75

                  #Réinitialisation de la position du texte ainsi que de l'icone a droite en dehors de la fênetre
                  textGoldLost.place(x=xGoldLost ,y=yGoldLost, anchor=E)
                  goldIconLost.place(x=xGoldLost+40 ,y=yGoldLost, anchor=E)   

                  #Réactivation du bouton confirmer
                  confirmButton.configure(state=NORMAL)
                  confirmButtonBorder.config(highlightbackground='white')

                  textGold['text'] = gold #On actualise également le texte affichant le gold
                  goldLost = 0 #Réintialisation du gold gagné
                  goldSerialization() #Enregistrement du gold
                  tempsAnimGoldLost = 0 #Réintialisation du timer
                  return None #On retourne rien pour finir la fonction

            #On attent 1ms et on relance ainsi la fonction en boucle
            window.after(1, animAchat)

      def cliqueShop(event):
            """ Fonction exécutée lorsque l'utilisateur clique sur une des images disponnibles a l'achat, renvoyant l'indice de celle-ci afin d'identifier son prix 
            grace a la liste couts stockant tous les prix dans l'ordre """
            global gold, goldLost, grille, cases, images, afficheImage

            #Si il y a un 'L' dans les 2 dernieres lettres du nom de l'image (donc de la variable) cliquée, cela veut dire que que seul la dernière lettre est un chiffre donc on la prend
            if str(event.widget)[-2:].count("l") == 1:
                  indiceImageSelect = int(str(event.widget)[-1:])-2 #On applique un -2 a cause de l'écart crée par 'event.widget'
            #Sinon cela signifie que les 2 dernières lettres sont des chiffres donc on prend les 2
            else: 
                  indiceImageSelect = int(str(event.widget)[-2:])-2 #On applique un -2 a cause de l'écart crée par 'event.widget'

            #Si le joueur à assez de gold
            if gold - couts[indiceImageSelect] >= 0 and not indiceImageSelect+1 in imagesBought:
                  globals()['achatImage%s'%(indiceImageSelect+1)]['image'] = globals()['imageShopOWN%s'%(indiceImageSelect+1)]
                  goldLost = couts[indiceImageSelect]
                  imagesBought.append(indiceImageSelect+1)
                  serialization()
                  gold -= goldLost
                  animAchat()
                  couts[23] = gold #On actualise le cout de l'image easter Egg qui prend TOUT le gold
            #On affiche l'image JOUER si celle ci est déjà achetée
            elif indiceImageSelect+1 in imagesBought:
                  afficheImage[0] = imagesURL[indiceImageSelect]
                  exitShop()
            else:
                  notEnoughtAnim()

      #Création d'un label invisible afin de faire un peu d'espace supplémentaire au début du scrollbar, question d'esthétique
      espaceVideDebut = Label(shopFrame, bg='#363636', border=0, highlightthickness=0)
      espaceVideDebut.pack(side=LEFT, padx=20, pady=20)

      #On défini les variables stoclant : image puis Label contenant l'image puis affichage de celui-ci
      for i in range(1,rangeShop):
            #On défini les images (ACHETER/JOUER)
            if i > 22:
                  globals()['imageShopBUY%s'%i] = PhotoImage(file="ImagesShop/EasterEgg/ImageShopBUYEasterEgg%s"%(i-22)+".png").subsample(3,3)
                  globals()['imageShopOWN%s'%i] = PhotoImage(file="ImagesShop/EasterEgg/ImageShopOWNEasterEgg%s"%(i-22)+".png").subsample(3,3)
            else:
                  globals()['imageShopOWN%s'%i] = PhotoImage(file="ImagesShop/ImageShopOWN%s"%i+".png").subsample(3,3)
                  globals()['imageShopBUY%s'%i] = PhotoImage(file="ImagesShop/ImageShopBUY%s"%i+".png").subsample(3,3)

            #On regarde si l'utilisateur à déja acheté l'image et si oui on affiche l'image avec le texte JOUER
            if not i in imagesBought:
                  globals()['achatImage%s'%i] = Label(shopFrame, image=globals()['imageShopBUY%s'%i], cursor="hand2", bg='#363636')
            else:
                  globals()['achatImage%s'%i] = Label(shopFrame, image=globals()['imageShopOWN%s'%i], cursor="hand2", bg='#363636')
            globals()['achatImage%s'%i].pack(side=LEFT, padx=12, pady=20)

            #On déclanche la fonction 'clique' lorsque l'utilisateur presse le bouton 'Button-1' (clique gauche) sur un label
            globals()['achatImage%s'%i].bind('<Button-1>', cliqueShop)

      #Création d'un label invisible afin de faire un peu d'espace supplémentaire a la fin du scrollbar, question d'esthétique
      espaceVideFin = Label(shopFrame, bg='#363636', border=0, highlightthickness=0)
      espaceVideFin.pack(side=LEFT, padx=25, pady=20)

      #Affichage
      window.mainloop()

#Affichage de la fenêtre
window.mainloop()