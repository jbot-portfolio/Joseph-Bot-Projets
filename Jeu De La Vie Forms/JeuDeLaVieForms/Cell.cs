using System;

namespace Jeu_de_la_vie
{
    class Cell
    {
        private bool _isAlive; // État de la cellule
        public bool isAlive { get { return _isAlive; } set { _isAlive = value; } } //Accesseurs en lecture et en écriture pour _isAlive
        private bool _nextState; // Stockage temporaire de l’état de la cellule pour le prochain pas de la simulation
        public bool nextState { get { return _nextState; } set { _nextState = value; } } // Accesseurs en lecture et en écriture pour _nextState

        public Cell(bool state) // Constructeur de la classe Cell qui modifie l’attribut _isAlive via son accesseur en écriture pour lui attribuer la valeur state.
        {
            isAlive = state;
        }

        public void ComeAlive() // Méthode qui modifie à true l’attribut _nextState via son accesseur en écriture.
        {
            nextState = true;
        }

        public void PassAway() // Méthode qui modifie à false l’attribut _nextState via son accesseur en écriture.
        {
            nextState = false;
        }

        public void Update() // Méthode qui met à jour l’attribut _isAlive via son accesseur en écriture en lui associant la valeur contenue dans la variable _nextState via son accesseur en lecture
        {
            isAlive = nextState;
        }
    }
}
