"""
Projet Théorie des graphes L3 EFREI
    -
    -
    - Nathan RICARDO
    - Thomas SONG
    -

Classe principale de la gestion des Automates du projet
"""

import os

import beautifultable

import config

from config import Configuration
from graphe_files import Lecture

class Graphes:
    def __init__(self):
        """
        Initialisation de la classe et de ses paramètres

        :param fichier: Le nom du fichier à ouvrir dans le path par défaut trouvé dans les configurations.
        """
        self.config = Configuration()
        self.grapheDict = []
        self.tache = []
        self.duree = []
        self.contraintes = []
        self.rang = []

    def setAll(self, tache, duree, contraintes):
        """
        Set les paramètres de la classe avec les valeurs stockés dans "self.lignes"
        """
        self.tache = tache
        self.duree = duree
        self.contraintes = contraintes

    def setGrapheDict(self):
        """
        Set le dictionnaire du graphe
        """
        for i in range(len(self.tache)):
            self.grapheDict.append({"tache": self.tache[i],
                                    "duree": self.duree[i],
                                    "contraintes": self.contraintes[i]})





if __name__ == '__main__':
    # Tests de la classe locale
    configuration = Configuration()
    test = Lecture(os.path.join(configuration.graphes_path, "test.txt"))
    graphe = Graphes()
    graphe.setAll(test.tache, test.duree, test.contraintes)
    graphe.setGrapheDict()
    print(graphe.grapheDict)
