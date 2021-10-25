using System;
using System.Collections.Generic;
using System.Drawing;
using System.Threading;
using System.Windows.Forms;


namespace Jeu_de_la_vie
{
    class Game
    {
        private int n; // Taille de la grille
        int iter = -1;
        public Grid grid; // Grille des emplacements possibles
        List<Coords> AliveCellsCoords; // Liste des coordonnées des cellules vivantes en début de simulation.
        public Random random;

        public Game(int nbCells) // Constructeur de la class Game
        {
            n = nbCells;
            AliveCellsCoords = new List<Coords>();
            random = new Random();
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if (random.Next(0, 2) == 1)
                    {
                        Coords coords = new Coords(i, j);
                        AliveCellsCoords.Add(coords);
                    }
                }
            }
            grid = new Grid(n, AliveCellsCoords);
        }

        public Game(int nbCells, int iteration) // Constructeur de la class Game
        {
            n = nbCells;
            iter = iteration;
            AliveCellsCoords = new List<Coords>();
            random = new Random();
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if (random.Next(0, 2) == 1)
                    {
                        Coords coords = new Coords(i, j);
                        AliveCellsCoords.Add(coords);
                    }
                }
            }
            grid = new Grid(n, AliveCellsCoords);
        }

        public void Paint(Graphics g)
        {
            SolidBrush whiteBrush = new SolidBrush(Color.White);
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if (grid.TabCells[i, j].isAlive)
                    {
                        g.FillRectangle(whiteBrush, j * 5, i * 5, 5, 5);
                    }
                }
            }
        }

        public void RunGameConsole() // Méthode de supervisation qui implémente
        {
            grid.DisplayGrid();
            while (iter>0) {
                grid.UpdateGrid();
                grid.DisplayGrid();
                Thread.Sleep(1000);
                iter--;
            }
        }





    }
}
