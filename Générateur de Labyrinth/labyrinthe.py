# PROGRAMMÉ PAR JOSEPH BOT #
#--------------------------#

import ClassPile as cp

class Labyrinthe():
    """ Modélisation d'un labyrinthe """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = []
        self.ouvert = 0 #Nombre de murs ouverts
        self.cases = 0 #Nombre de cases du labyrinthe

        #On génère toutes les cases du labyrinthe
        for h in range(height): # Colonnes
            self.cells.append([])
            for w in range(width): #Lignes
                self.cases += 1
                self.cells[h].append({"N":False, "E":False, "S":False, "O":False, "zone":self.cases})
    
    def print(self, print_zones=False):
        """ Affichage du labyrinthe en 'ASCII art' dans la console """
        from math import floor
        #alias :
        w=self.width;h=self.height;c=self.cells
        #si on imprime les zones, il faut élargir la taille des couloirs
        if(print_zones):
            len_zone=max([ max([ len(str(laby.cells[i][j]['zone'])) for i in range(laby.height) ]) for j in range(laby.width) ])+1
        inters=[' ','╴','╷', '┐','╶','─','┌','┬','╵','┘','│','┤','└','┴','├','┼']
        t=""
        #la grille des intersections de cases est de taille (N+1)(M+1)
        for i in range(h+1):
            interligne=""
            for j in range(w+1):
                #up, right, bottom, left : les 4 parties de la croix "┼" #False = mur, True = pas mur
                #Coins et bords:
                up=False if i==0 else None
                left=False if j==0 else None
                right=False if j==w else None
                bottom=False if i==h else None
                if j==w:
                    if up==None:up=not c[i-1][j-1]['E']
                    if bottom==None:bottom=not c[i][j-1]['E']
                if i==h:
                    bottom=False
                    if right==None:right=not c[i-1][j]['S']
                    if left==None:left=not c[i-1][j-1]['S']
                #intérieur :
                if up==None:up=not c[i-1][j]['O']
                if right==None:right=not c[i][j]['N']
                if bottom==None:bottom=not c[i][j]['O']
                if left==None:left=not c[i][j-1]['N']
                #-> mot binaire à 4 bits. 16 cas qu'on a mis dans l'ordre dans la liste inters
                #indice inters
                k=-up*8+right*4+bottom*2+left
                if not print_zones:
                    #espacement horizontal supplémentaire
                    sep= "─" if left else " "
                    t+=sep+inters[k]
                    if j==self.width:t+="\n"
                else:
                    sep= (len_zone+2)*"─" if right else (len_zone+2)*" "
                    #num_zone=self.zones[self.cells[i][j]["zone"]] if i<self.height and j<self.width else ""
                    num_zone=self.cells[i][j]["zone"] if i<self.height and j<self.width else ""

                    len_sp_left=floor((len_zone - len(str(num_zone)))/2)
                    len_sp_right=len_zone-len(str(num_zone))-len_sp_left
                    txt_num_zone=str(num_zone)# if num_zone > -1 and num_zone <10  else "*"
                    interligne+=("│" if bottom else " ")+" "*(len_sp_left+1)+txt_num_zone+" "*(len_sp_right+1)
                    t+=inters[k]+sep
                    if j==self.width:
                        t+="\n" + interligne + "\n"
        print(t)

    def peindre(self, i, j, origine, valeur):
        """ Peint les zones a fusionner avec le même chiffre """
        if i < 0 or i >= self.height or j < 0 or j >= self.width:
            return None
        else:
            if self.cells[i][j]["zone"] == valeur:
                self.cells[i][j]["zone"] = origine
                self.peindre(i, j-1, origine, valeur)
                self.peindre(i, j+1, origine, valeur)
                self.peindre(i-1, j, origine, valeur)
                self.peindre(i+1, j, origine, valeur)

    def fusionner(self, i, j, dir):
        """ Ouvre les murs et fusionne les zones """
        zone = self.cells[i][j]["zone"]
        if  dir == "E" and self.cells[i][j+1]["zone"] != zone:
            self.ouvert += 1
            self.cells[i][j]["E"] = True
            self.cells[i][j+1]["O"] = True
            self.peindre(i, j+1, zone, self.cells[i][j+1]["zone"])

        elif  dir == "O" and self.cells[i][j-1]["zone"] != zone:
            self.ouvert += 1
            self.cells[i][j]["O"] = True
            self.cells[i][j-1]["E"] = True
            self.peindre(i, j-1, zone, self.cells[i][j-1]["zone"])

        elif  dir == "N" and self.cells[i-1][j]["zone"] != zone:
            self.ouvert += 1
            self.cells[i][j]["N"] = True
            self.cells[i-1][j]["S"] = True
            self.peindre(i-1, j, zone, self.cells[i-1][j]["zone"])

        elif  dir == "S" and self.cells[i+1][j]["zone"] != zone:
            self.ouvert += 1
            self.cells[i][j]["S"] = True
            self.cells[i+1][j]["N"] = True
            self.peindre(i+1, j, zone, self.cells[i+1][j]["zone"])

        else:
            return False

    def generer(self):
        """ Génération du labyrinthe """
        murs = cp.Pile()
        for i in range(self.height):
            for j in range(self.width):
                if i != 0:
                    murs.empiler((i, j, "N"))
                if i != self.height-1:
                    murs.empiler((i, j, "S"))
                if j != 0:
                    murs.empiler((i, j, "O"))
                if j != self.width-1:
                    murs.empiler((i, j, "E"))
        murs.melange()
        while self.ouvert < (self.height * self.width-1):
            monMur = murs.depiler()
            self.fusionner(monMur[0], monMur[1], monMur[2])

laby = Labyrinthe(20,20)
laby.generer()
laby.print([0])