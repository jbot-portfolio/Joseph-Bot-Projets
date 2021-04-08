# PROGRAMMÉ PAR JOSEPH BOT #
#--------------------------#

import random as rd

class Pile:
    """ Création de la structure de données des Piles"""
    def __init__(self):
        """ Initialisation des 2 attributs : une liste L vide et la taille de la pile """
        self.L = []
        self.taille = 0

    def vide(self):
        """ Teste si la pile est vide en retournant Vrai si c’est le cas """
        return self.taille == 0

    def depiler(self):
        """ Retourne la pile au sommet """
        assert(self.taille != 0), "La pile est déjà vide"
        self.taille -= 1
        return self.L.pop()

    def empiler(self,x):
        """ Retourne la pile avec pour sommet x """
        self.taille += 1
        return self.L.append(x)

    def longeur(self):
        """ Retourne la longeur """
        return self.taille

    def sommet(self):
        """ Retourne le sommet """
        assert(self.taille != 0), "La pile est déjà vide"
        return self.L[-1]
    
    def melange(self):
        """ Mélange la Pile """
        return rd.shuffle(self.L)