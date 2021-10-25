using System;

namespace Jeu_de_la_vie
{
    public readonly struct Coords
    {
        public Coords(int X, int Y)
        {
            _x = X;
            _y = Y;
        }

        public int _x { get; }
        public int _y { get; }

        public override string ToString() => $"({_x}, {_y})";
    }
}

