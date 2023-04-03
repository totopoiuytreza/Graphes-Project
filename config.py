"""
Projet Théorie des graphes L3 EFREI
    - Yann SCARDIGLI
    - Pierre THAITE
    - Nathan RICARDO
    - Thomas SONG
    -

Ce fichier conserve une classe de configuration qui permet de partager les configurations partout dans le projet
"""

import os


class Configuration:
    def __init__(self):
        """
        On vient mettre en place les constantes du projet.
        """

        # Path vers le répertoire des graphes par défaut.
        self.graphes_path = os.path.join(os.path.dirname(__file__), "graphes")
        # Path vers les ressources images
        self.ressources_path = os.path.join(os.path.dirname(__file__), "ressources")

        # Le groupe du projet, pour masquer dans l'interface
        #self.nom_groupe = "D04-"

        # Les séparateurs.
        self.separateur = " "

