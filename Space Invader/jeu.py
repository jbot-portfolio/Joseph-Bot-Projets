# PROGRAMMÉ PAR JOSEPH BOT #
#--------------------------#

import pygame, sys
from pygame.locals import*
from random import*
import time

pygame.init()
pygame.font.init()
mainclock = pygame.time.Clock()				
window = pygame.display.set_mode((1280,740 ,),0,32) #Taille fenêtre du jeu
pygame.display.set_caption('SpaceInvader') #Titre de la fenêtre

#Coordonnées de départ du vaiseau
xs = 40
ys = 625

missile = []
cible = []
Gauche = False
Droite = False

#Création d'un texte
Texty = pygame.font.Font('Font/Roboto-Black.TTF', 35)
TextEnd = pygame.font.Font('Font/Roboto-Black.TTF', 45)
Obj_texte = Texty.render('SPACE INVADER', 0, (255,255,255))

#Importation des images
ship = pygame.image.load('Images/ship.png')
hearts = pygame.image.load('Images/hearts3.png')

clock = pygame.time.Clock()

listeInvaders = [] #Stock des enemis
listeInstances = [] #Stock des instances de la classe Invader
listeSpawn = [125]
points = 0
vies = 3
partieFinie = False

class Invader():    
    """ Classe permettant la création d'enemis """

    def __init__(self, enemies, listeEnemies, enemy): #Initialisation
        self.enemies = enemies
        self.listeEnemies = listeEnemies
        self.enemy = enemy
        self.posX = 0
        self.posY = -100

    def spawn(self):
        """ Spawn de l'ennemi """

        global listeSpawn
        self.listeEnemies.append(f"enemy{+self.enemy}")

        if len(listeSpawn) <= 4: #Premier Spawn
            self.posX = 75 + listeSpawn[-1]
            listeSpawn.append(listeSpawn[-1] + 75)
        else:
            self.posX = randint(250, 950)

        self.posY = -100
        self.enemies.append(pygame.Rect(self.posX,self.posY,50,40))
        globals()[listeInstances[self.enemy]] = pygame.image.load("Images/enemy%s"% randint(1,20)+".png") 

    def move(self):
        """ Déplacement de l'ennemi """
        global vies, hearts, points, partieFinie
 
        if self.posY < 750:
            self.posY += 2
            self.enemies[self.enemy] = pygame.Rect(self.posX,self.posY,50,40)

        else: #Si l'ennemi quand il arrive en bas de la fenêtre
            del self.enemies[self.enemy]
            del self.listeEnemies[self.enemy]

            if vies > 1:
                vies -= 1 #On décrémente les vies de 1 et on actualise le sprite affichant celles-ci
                hearts = pygame.image.load(f'Images/hearts{vies}.png')
            else:
                hearts = pygame.image.load(f'Images/hearts0.png')
                partieFinie = True

            self.spawn()

for e in range(1,5):
    globals()["invader%s"%e] = Invader(cible, listeInvaders, e-1)
    listeInstances.append(globals()["invader%s"%e])
    globals()["invader%s"%e].spawn() #Instanciation des invaders


while True:
    window.fill(0x1D1D1D) #Remplissage de la couleur d'arrière plan
    window.blit(pygame.transform.scale(ship, (64, 64)), (xs, ys)) #Redimensionner et placer l'image du vaisseau
    window.blit(hearts,(1145, 690)) #Placement des vies
    
    #Placement du texte "Space Invader"
    window.blit(Obj_texte,(30,25)) 

    #Si la partie est finie on affiche le texte
    if partieFinie:
        texteScoreFinal = Texty.render(f"SCORE : {str(points)}", 0, (255,255,255))
        window.blit(texteScoreFinal,(500, 300))
        texteScoreFinal = TextEnd.render(f"PRESS ENTER TO PLAY AGAIN", 0, (255,255,255))
        window.blit(texteScoreFinal,(300, 410))

    if not partieFinie: #Tant que la partie n'est pas terminée
        #Affichage du score
        textePoints = Texty.render(str(points), 0, (255,255,255))
        window.blit(textePoints,(25, 690))

        #Affichage des ennemis
        for e in range(1,5):
            window.blit(globals()[listeInstances[e-1]], cible[e-1])
            globals()["invader%s"%e].move()

    #Traitement des évenements du clavier
    for event in pygame.event.get():
        if event.type == KEYDOWN: #Quand on appuis sur une touche
            if event.key == K_ESCAPE: #ECHAP
                pygame.quit()
                sys.exit()
            if event.key == K_RIGHT: #Flêche de gauche
                Droite = True
            if event.key == K_LEFT: #Flêche de droite
                Gauche = True
            if event.key == K_SPACE and not partieFinie: #Espace
                missile.append(pygame.Rect(xs+29,ys-3,6,16))
            if event.key == K_RETURN and partieFinie: #Entrer, uniquement si la partie est finie
                partieFinie = False
                hearts = pygame.image.load(f'Images/hearts3.png')
                vies = 3
                points = 0

        if event.type == KEYUP: #Quand on arrête d'appuyer sur une touche
            if event.key == K_RIGHT: 
                Droite = False
            if event.key == K_LEFT:
                Gauche = False

        if event.type == QUIT: #Quitter
            pygame.quit()
            sys.exit()

    #Déplacement du vaisseau
    if Gauche and xs > 40:
        xs -= 7
    if Droite and xs < 1170:
        xs += 7

    if not partieFinie:
        #Tirs
        for tir in missile:
            tir.top = tir.top-10
            pygame.draw.rect(window,0xFF0000,tir)

            if tir.top <= -150: #Suppression du missile lorsqu'il atteint le haut de la fenêtre
                missile.remove(tir)

            #Quand un enemi est touché
            for enemy in range(len(cible)):
                if tir.colliderect(cible[enemy]):
                    missile.remove(tir)
                    del cible[enemy]
                    del listeInvaders[enemy]
                    listeInstances[enemy].spawn()
                    points += 1000

    #Acutalisation de la fenêtre
    pygame.display.update()
    clock.tick(60) #Taux de rafraichissement