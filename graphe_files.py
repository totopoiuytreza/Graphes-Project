"""
Projet Théorie des graphes L3 EFREI
    -
    -
    - Nathan RICARDO
    - Thomas SONG
    -
Gestion des fichiers permettant de conserver les automates.
"""

import os

from config import Configuration


class Error(Exception):
    pass


class GraphesNotFound(Error):
    pass


class Lecture:
    def __init__(self, fichier):
        """
        Cette classe permet de lire un fichier automate pour les gérer dans les classes qui l'exploitent.

        :param fichier: Le nom du fichier à ouvrir, présent dans le répertoire par défaut du projet.
        """

        config = Configuration()
        self.separateur = config.separateur
        self.fichier = fichier
        self.tache = []
        self.duree = []
        self.contraintes = []
        self.lignes = []
        self.lecture_fichier()

    def lecture_fichier(self):
        """
        Lecture complète d'un fichier, sans traitement. Le résultat est stocké dans "self.lignes" et peut donc être
        réutilisé
        """

        try:
            # On lit tous le fichier
            with open(self.fichier, "r") as fichier_ouvert:
                self.lignes = fichier_ouvert.readlines()
            # On supprime les retours \n
            add_empty_line = False
            for index, ligne in enumerate(self.lignes):
                if index == len(self.lignes) - 1 and "\n" in ligne:
                    add_empty_line = True
                self.lignes[index] = ligne.strip()
            if add_empty_line:
                # Dans le cas où la dernière ligne de transitions est vide
                self.lignes.append("")
        except FileNotFoundError:
            print(f"Attention, le fichier {self.fichier} n'existe pas. La classe n'est pas initialisée")
            raise GraphesNotFound
        self.remplissage_graphe()

    def remplissage_graphe(self):
        """
        Stocke les informations du graphe dans "self.tache", "self.duree" et "self.contraintes"
        """
        for element in self.lignes:
            temp = []
            element = element.split(self.separateur)
            self.tache.append(element[0])
            self.duree.append(element[1])
            if len(element) > 1:
                for i in range(2, len(element)):
                    temp.append(element[i])
            self.contraintes.append(temp)


if __name__ == '__main__':
    # Tests de la classe locale
    configuration = Configuration()
    test = Lecture(os.path.join(configuration.graphes_path, "test.txt"))
    print(test.tache)
    print(test.duree)
    print(test.contraintes)
