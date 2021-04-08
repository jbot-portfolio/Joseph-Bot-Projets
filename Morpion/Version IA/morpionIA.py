# PROGRAMMÉ PAR JOSEPH BOT #
#--------------------------#

import pygame,sys
import random as rd

pygame.init()
police = pygame.font.Font("Ressources/Roboto.ttf", 80)

class Morpion :

    def __init__(self,profondeur): #Initialisation
        self.J1 = "X"
        self.IA = "O"
        self.ecran = pygame.display.set_mode((600,600))
        self.grille = Grille(self.ecran)
        self.compteur = 0
        self.profondeur = profondeur
        
    
    def checkGagnant(self, joueur):
        """ Vérifie si un joueur a gagné """

        for i in range(3): #Lignes
            if self.grille.grille[i][0] == self.grille.grille[i][1] == self.grille.grille[i][2] == joueur:
                return joueur
        for j in range(3): #Colonnes
            if self.grille.grille[0][j] == self.grille.grille[1][j] == self.grille.grille[2][j] == joueur:
                return joueur
        if self.grille.grille[0][0] == self.grille.grille[1][1] == self.grille.grille[2][2] == joueur: #Diagonale descendante
            return joueur
        if self.grille.grille[2][0] == self.grille.grille[1][1] == self.grille.grille[0][2] == joueur: #Diagonale montante
            return joueur
        
        #On vérifie si il reste des mouvements possibles
        for i in range(3):
            for j in range(3):
                if self.grille.grille[i][j] == None:
                    return True
        return False #Sinon égalité
    
    
    def jeu(self):
        """ Permet l'IHM et le jeu """
        pygame.display.set_caption("Morpion")
        joueurs = [self.IA, self.J1]
        fin = False
        
        clock = pygame.time.Clock()
        
        while not fin: #Actualisation de la fenêtre
            time = clock.tick(30) #Refresh rate
            for event in pygame.event.get():                
                player = joueurs[self.compteur%2] #Tour
                
                if player == self.IA : #Tour de l'IA
                    self.intelligence_artificielle(self.profondeur)
                        
                else: #Tour du joueur
                    if player == self.J1 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        position = event.pos
                        if position[0] < 600: #Si l+'utilisateur clique sur le plateau de jeu
                            posX, posY = position[1]//200 ,position[0]//200
                            self.grille.changerValeur(posX, posY, self.J1)
                
                #On vérifie si le joueur à gagné ou si il y a égalité et on met fin au jeu
                if self.checkGagnant(player) == player or self.checkGagnant(player) == False:
                    fin = True
                #Sinon, fin du tour
                elif self.grille.tourJoueur:
                    self.compteur += 1 #Tour de l'autre joueur
                    self.grille.tourJoueur = False
                
                #Sortie du jeu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.ecran.fill((40,40,40))
            self.grille.afficher() #Actualisation du tableau de jeu
            pygame.display.flip() #Update
            
        #On vérifie si le joueur a gagné et on l'affiche
        if self.checkGagnant(player) == player:
                texte = police.render(f"GAGNANT : {player}", True, pygame.Color("#FFFFFF"))
                rectTexte = texte.get_rect()
                rectScreen = self.ecran.get_rect()
                rectTexte.center = rectScreen.center
                self.ecran.blit(texte, rectTexte)
                pygame.display.flip()
        else: #Sinon égalité
            texte = police.render("EGALITÉ",True, pygame.Color("#FFFFFF"))
            rectTexte = texte.get_rect()
            rectScreen = self.ecran.get_rect()
            rectTexte.center = rectScreen.center
            self.ecran.blit(texte, rectTexte)
            pygame.display.flip()
        
        #Sortie du jeu à la fin de la partie
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
        
    def intelligence_artificielle(self, depth):
        """ Fait jouer le coup par l'IA """
        maxI,maxJ = None,None
        maximum = -10000
        jeu = self.grille.grille # On copie le jeu dans une variable temporaire
        for i in range(3):
            for j in range(3):
                #Si la case est libre, on lance l'IA
                if jeu[i][j] == None:
                    jeu[i][j] = self.IA
                    tmp = self.valeurMin(jeu, depth-1)

                    if tmp > maximum or (tmp == maximum and rd.randint(0,2) == 1): #Premier coup aléatoire par l'IA
                        maximum = tmp
                        maxI = i
                        maxJ = j
                    jeu[i][j] = None

        #On fait jouer le meilleur coup par l'IA
        if self.checkGagnant(self.IA) == True:
            self.grille.changerValeur(maxI, maxJ, self.IA)
    
        
    def valeurMax(self, jeu, depth):
        """ Détermine le meilleur coup possible pour l'IA """
        maximum = -10000
        if depth == 0 or self.checkGagnant(self.J1) != True or self.checkGagnant(self.IA) != True:
            return self.evaluer(jeu)

        for i in range(3):
            for j in range(3):
                #Si la case est libre on lance l'IA
                if jeu[i][j] == None:
                    jeu[i][j] = self.IA
                    tmp = self.valeurMin(jeu, depth-1)
        
                    if tmp > maximum:
                        maximum = tmp
                    
                    jeu[i][j] = None
        return maximum
    
    
    def valeurMin(self, jeu, depth):
        """ Détermine le meilleur coup possible par le Joueur """
        minimum = 10000
        if depth == 0 or self.checkGagnant(self.J1) != True or self.checkGagnant(self.IA) != True:
            return self.evaluer(jeu)
     
        for i in range(3):
            for j in range(3):
                #Si la case est libre, on fait jouer le coup anticipé du joueur
                if jeu[i][j] == None:
                    jeu[i][j] = self.J1
                    tmp = self.valeurMax(jeu, depth-1)
                
                    if tmp < minimum:
                        minimum = tmp
                    jeu[i][j] = None
        return minimum
    
    def nbrSeries(self, jeu, seriesJ1, seriesJ2, n=0):
        """ Compte le nombre de séries de n pions alignés de chacun des joueurs, en ligne, colonne et en diagonale """

        seriesJ1, seriesJ2 = 0, 0
        compteur1, compteur2 = 0, 0
        largeur = len(jeu[0])
        
        #Diagonale descendante
        for i in range(largeur):
            if jeu[i][i] == 1:
        
                compteur1 += 1
                compteur2 = 0

                if compteur1 == n:
                    seriesJ1 += 1
        
            elif jeu[i][i] == 2:
                compteur2 += 1
                compteur1 = 0
     
                if compteur2 == n:
                     seriesJ2 += 1

        compteur1, compteur2 = 0,0

        #Diagonale montante
        for i in range(largeur):
            if jeu[i][largeur-i] == 1:
                compteur1 += 1
                compteur2 = 0

                if compteur1 == n:
                    seriesJ1 += 1
            elif jeu[i][largeur-i] == 2:
                compteur2 += 1
                compteur1 = 0
     
                if compteur2 == n:
                     seriesJ2 += 1

        #En ligne
        for i in range(largeur):
            compteur1, compteur2 = 0, 0
       
            #Horizontalement
            for j in range(largeur):
                if jeu[i][j] == 1:
                    compteur1 += 1
                    compteur2 = 0

                    if compteur1 == n:
                        seriesJ1 += 1
            
                elif jeu[i][j] == 2:
                    compteur2 += 1
                    compteur1 = 0

                    if compteur2 == n:
                        seriesJ2 += 1

            compteur1,compteur2 = 0, 0

            #Verticalement
            for j in range(largeur):
                if jeu[j][i] == 1:
                    compteur1 += 1
                    compteur2 = 0

                    if compteur1 == n:
                        seriesJ1 += 1
            
                elif jeu[j][i] == 2:
                    compteur2 += 1
                    compteur1 = 0

                    if compteur2 == n:
                        seriesJ2 += 1

    def evaluer(self,jeu):
        """ Évaluation du poid du tableau de jeu """
        gagnant = None
        nb_de_pions = 0
    
        #On compte le nombre de pions présents sur le plateau
        for i in range(3):
            for j in range(3):
                if jeu[i][j] != None:
                    nb_de_pions += 1

        if self.checkGagnant(self.J1) != True or self.checkGagnant(self.IA) != True:
            gagnant = self.checkGagnant(self.J1)
        
        if gagnant == self.IA:
            return 1000 - nb_de_pions;
        
        elif gagnant == self.J1:
            return -1000 + nb_de_pions
        else:
            return 0

        #On compte le nombre de séries de 2 pions alignés de chacun des joueurs
        seriesJ1 = 0
        seriesJ2 = 0
        nbrSeries(jeu, seriesJ1, seriesJ2, 2)

        return seriesJ1 - seriesJ2 
             
 

class Grille():

    def __init__(self, ecran): #Iniatialisation
        self.ecran = ecran
        self.lignes = [((200, 0),(200, 600)), ((400, 0),(400, 600)), ((0, 200),(600, 200)), ((0, 400),(600, 400))]
        self.grille = [[None,None,None],
                       [None,None,None],
                       [None,None,None]]
        self.tourJoueur = False
        #Importation des images pour les X et O
        self.imgX = pygame.image.load('Ressources/X.png')
        self.imgO = pygame.image.load('Ressources/O.png')
        
    def afficher(self):
        """ Affiche le plateau de jeu """
        for ligne in self.lignes:
            pygame.draw.line(self.ecran, (230, 230, 230), ligne[0], ligne[1], 5)
        for y in range(0,len(self.grille)):
            for x in range(0,len(self.grille)):
                if self.grille[y][x] == 'X':
                    self.ecran.blit(self.imgX, ((x * 200), (y * 200)))

                elif self.grille[y][x] == 'O':
                    self.ecran.blit(self.imgO, ((x * 200), (y * 200)))
    
    def changerValeur(self, x, y, valeur):
        """ Change la valeur d'une case du tableau de jeu """
        if self.grille[x][y] == None:
            self.grille[x][y] = valeur
            self.tourJoueur = True #Fin du tour
           

#On demande au joueur la difficulté de l'IA
choixDifficulte = int(input("Niveau : 1 (facile) à 9 (difficile)\nVotre choix : "))
while choixDifficulte < 1 or choixDifficulte > 9:
    print("\nSaisie invalide\n")
    choixDifficulte = int(input("Niveau : 1 (facile) à 9 (difficile)\nVotre choix : "))

#Instanciation du jeu
game = Morpion(choixDifficulte)
game.jeu()