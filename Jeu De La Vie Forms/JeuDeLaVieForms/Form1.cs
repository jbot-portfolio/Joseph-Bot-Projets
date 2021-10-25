using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Jeu_de_la_vie
{
    public partial class Form1 : Form
    {
        Game game;
        int n = 40;

        public Form1()
        {
            InitializeComponent(n);
            game = new Game(n);
            Timer MyTimer = new Timer();
            MyTimer.Interval = (60);
            MyTimer.Tick += new EventHandler(MyTimer_Tick);
            pictureBox1.Paint += new PaintEventHandler(pictureBox1_Paint);
            MyTimer.Start();
        }

        private void MyTimer_Tick(object sender, EventArgs e)
        {
            game.grid.UpdateGrid();
            Refresh();

        }

        private void pictureBox1_Paint(object sender, PaintEventArgs e)
        {
            game.Paint(e.Graphics);
        }

    }
}
