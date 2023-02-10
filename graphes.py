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
        self.onlyOneEntreeAndSortie = False

    def setTaskDureeContraintes(self, tache, duree, contraintes):
        """
        Set les paramètres de la classe avec les valeurs stockés dans "self.lignes"
        """
        self.tache = tache
        self.duree = duree
        self.contraintes = contraintes

    def setType(self):
        """
        Set le type de chaque tâche
        """
        for element in self.grapheDict:
            if not element["contraintes"]:
                element["type"] = "Entree"
            isSortie = True
            for element2 in self.grapheDict:
                if element["tache"] in element2["contraintes"]:
                    isSortie = False
            if isSortie:
                element["type"] = "Sortie"


    def checkEntreeSortie(self):
        """
        Vérifie si le graphe possède bien une entrée et une sortie
        """
        onlyOneEntree = 0
        onlyOneSortie = 0
        for element in self.grapheDict:
            if element["type"] == "Entree":
                onlyOneEntree += 1
            if element["type"] == "Sortie":
                onlyOneSortie += 1
        if onlyOneEntree == 1 and onlyOneSortie == 1:
            self.onlyOneEntreeAndSortie = True










    def setGrapheDict(self):
        """
        Set le dictionnaire du graphe
        """
        for i in range(len(self.tache)):
            self.grapheDict.append({"tache": self.tache[i],
                                    "duree": self.duree[i],
                                    "contraintes": self.contraintes[i],
                                    "type": "",
                                    "rang": 0})

    # todo: faire la fonction qui renvoie la matrice des valeurs
    def getValueMatrix(self):
        """
        Renvoie la matrice des valeurs
        """
        rows = []
        columns = []
        matrix = []

    # todo : faire la fonction qui le rang de chaque tâche
    def setRang(self):
        """
        Set le rang de chaque tâche
        """
        pass
    
    def __copy__(self):
        """
        Permet de copier un objet de la classe
        """
        newGraphe = Graphes()
        newGraphe.setTaskDureeContraintes(self.tache, self.duree, self.contraintes)
        newGraphe.setGrapheDict()
        newGraphe.setType()
        newGraphe.checkEntreeSortie()
        return newGraphe



if __name__ == '__main__':
    # Tests de la classe locale
    configuration = Configuration()
    test = Lecture(os.path.join(configuration.graphes_path, "test.txt"))
    graphe = Graphes()
    graphe.setTaskDureeContraintes(test.tache, test.duree, test.contraintes)
    graphe.setGrapheDict()
    graphe.setType()
    graphe.checkEntreeSortie()
    for element in graphe.grapheDict:
        print(element)
    print(graphe.onlyOneEntreeAndSortie)
