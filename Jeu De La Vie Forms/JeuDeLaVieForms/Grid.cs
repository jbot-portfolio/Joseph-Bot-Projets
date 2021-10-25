using System;
using System.Collections.Generic;


namespace Jeu_de_la_vie
{
    class Grid
    {
        private int _n; // Taille de la grille
        public int n { get { return _n; } set { _n = value; } } // Accesseurs en lecture eten écriture
        public Cell[,] TabCells; // Tableau à deux dimensions contenant des objets de type Cell

        public Grid(int nbCells, List<Coords> AliveCellsCoords) // Constructeur de la class Grid
        {
            this.n = nbCells; // Initialisation de l’attribut _n au travers de l’accesseur en écriture

            TabCells = new Cell[n, n]; // Création d’un tableau à deux dimensions de taillen,n
            /* Remplissage du tableau avec à chaque emplacement une instance d’une cellule
            Cell créée vivante (true) si les coordonnées sont dans la liste AliveCellsCoords
            ou absente (false) sinon.*/

            for (int i = 0; i < n; i++){
                for (int j = 0; j < n; j++){
                    if (AliveCellsCoords.Contains(new Coords(i,j)))
                        TabCells[i, j] = new Cell(true);
                    else
                        TabCells[i, j] = new Cell(false);
                }
            }
        }

        public int getNbAliveNeighboor(int i, int j) // Méthode qui permet de déterminer le nombre de cellules vivantes autour d’un emplacement de coordonnées (i,j)
        {
            int nbCells = 0;
            if (i - 1 >= 0 && TabCells[i - 1, j].isAlive == true){
                nbCells += 1;
            }
            if (i + 1 < n && TabCells[i + 1, j].isAlive == true){
                nbCells += 1;  
            }
            if (j - 1 >= 0 && TabCells[i, j - 1].isAlive == true){
                nbCells += 1;
            }
            if (j + 1 < n && TabCells[i, j + 1].isAlive == true){
                nbCells += 1;
            }
            if (j + 1 < n && i + 1 < n && TabCells[i + 1, j + 1].isAlive == true){
                nbCells += 1;
            }
            if (i - 1 >= 0 && j - 1 >= 0 && TabCells[i - 1, j - 1].isAlive == true){
                nbCells += 1;
            }
            if (i + 1 < n && j - 1 >= 0 && TabCells[i + 1, j - 1].isAlive == true){
                nbCells += 1;
            }
            if (i - 1 >= 0 && j + 1 < n && TabCells[i - 1, j + 1].isAlive == true){
                nbCells += 1;
            }
            return nbCells;
        }    

        public List<Coords> getCoordsNeighboors(int i, int j) // Méthode qui permet de déterminer toutes les coordonnées valides autour d’un emplacement de coordonnées(i, j)(attention à la gestion des cas particulier en bordure de grille)
        {
            List<Coords> tempCoords = new List<Coords>();
            if (i - 1 >= 0 && TabCells[i - 1, j].isAlive == true){
                tempCoords.Add(new Coords(i - 1, j));
            }
            if (i + 1 < n && TabCells[i + 1, j].isAlive == true){
                tempCoords.Add(new Coords(i + 1, j));
            }
            if (j - 1 >= 0 && TabCells[i, j - 1].isAlive == true){
                tempCoords.Add(new Coords(i , j - 1));
            }
            if (j + 1 < n && TabCells[i, j + 1].isAlive == true){
                tempCoords.Add(new Coords(i , j + 1));
            }
            if (j + 1 < n && i + 1 < n && TabCells[i + 1, j + 1].isAlive == true){
                tempCoords.Add(new Coords(i + 1, j + 1));
            }
            if (i - 1 >= 0 && j - 1 >= 0 && TabCells[i - 1, j - 1].isAlive == true){
                tempCoords.Add(new Coords(i - 1, j - 1));
            }
            if (i - 1 >= 0 && j - 1 >= 0 && TabCells[i + 1, j - 1].isAlive == true){
                tempCoords.Add(new Coords(i + 1, j - 1));
            }
            if (i - 1 >= 0 && j + 1 < n && TabCells[i - 1, j + 1].isAlive == true){
                tempCoords.Add(new Coords(i - 1, j + 1));
            }
            return tempCoords;
        }    
        
        public List<Coords> getCoordsCellsAlive() // Méthode qui permet de déterminer la liste des coordonnées de toutes les cellules vivantes de la grille.
        {
            List<Coords> tempCoords = new List<Coords>();
            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j < n; j++)
                {
                    if (TabCells[i , j].isAlive == true)
                    {
                        tempCoords.Add(new Coords(i, j));
                    }
                }
            }
            return tempCoords;
        }

        public void DisplayGrid() // Méthode qui permet d’afficher une représentation de grille en console avec un X à chaque emplacement où une cellule est vivante
        {
            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j < n; j++)
                {
                    Console.Write("+---");
                }
                Console.Write("+\n");
                for (int j = 0; j < n; j++)
                {
                    if (TabCells[i, j].isAlive)
                        Console.Write("| X ");
                    else
                        Console.Write("|   ");
                }
                Console.Write("|\n");
            }
            for (int j = 0; j < n; j++)
            {
                Console.Write("+---");
            }
            Console.Write("+\n");
        }

        public void UpdateGrid() // Méthode qui parcourt chaque cellule et qui met à jour leur attribut _nextStep, via son accesseur en écriture, en fonction des règles de la simulation.L’attribut est mis à true si la cellule reste en vie ou apparaît et à false si la cellule à cet emplacement disparaît ou reste absente. Une fois toute la grille parcourue, une deuxième passe est effectué pour associer la valeur de nexStep à l’attribut isAlive de chaque cellule.
        {
            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j < n; j++)
                {
                    if(TabCells[i, j].isAlive == true && getNbAliveNeighboor(i, j)==2 || getNbAliveNeighboor(i,j)==3)
                    {
                        TabCells[i, j].ComeAlive();
                    }
                    else if (TabCells[i, j].isAlive == false && getNbAliveNeighboor(i, j) == 3)
                    {
                        TabCells[i, j].ComeAlive();
                    }
                    else
                    {
                        TabCells[i, j].PassAway();
                    }
                }
            }

            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j < n; j++)
                {
                    TabCells[i, j].Update();
                }
            }
        }
    }
}

