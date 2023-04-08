"""
Projet Théorie des graphes L3 EFREI
    - Yann SCARDIGLI
    - Pierre THAITE
    - Nathan RICARDO
    - Thomas SONG
    -

Programme principal pour lancer l'interface.
"""

import mainGUI as Gui
from graphe_files import Lecture

if __name__ == '__main__':
    appGraphes = Gui.AppGraphe()
    appGraphes.title("Gestion des Graphes. EFREI L3")

    appGraphes.mainloop()
