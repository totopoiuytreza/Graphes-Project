"""
Projet Théorie des graphes L3 EFREI
    -
    -
    - Nathan RICARDO
    - Thomas SONG
    -

Classe principale de la gestion des Graphes du projet
"""

import os

import beautifultable

from config import Configuration
from graphe_files import Lecture


class Graphes:
    def __init__(self, fichier):
        """
        Initialisation de la classe et de ses paramètres

        :param fichier: Le nom du fichier à ouvrir dans le path par défaut trouvé dans les configurations.
        """
        self.config = Configuration()
        self.fichier = Lecture(os.path.join(configuration.graphes_path, fichier))
        self.grapheDict = []
        self.tache = []
        self.duree = []
        self.contraintes = []
        self.onlyOneEntreeAndSortie = False
        self.dontHaveCircuit = True
        self.dontHaveNegativeDuration = True

        self.setTaskDureeContraintes()
        self.setGrapheDict()
        self.setType()
        self.setAlphaOmega()
        self.checkNegativeDuration()



    def setTaskDureeContraintes(self):
        """
        Set les paramètres de la classe avec les valeurs stockés dans "self.lignes" dans "self.fichier"
        """
        self.tache = self.fichier.tache
        self.duree = self.fichier.duree
        self.contraintes = self.fichier.contraintes

    def setType(self):
        """
        Set le type de chaque tâche
        """
        for element in self.grapheDict:
            if not element["contraintes"]:
                element["isEntree"] = "Entree"
            isSortie = True
            for element2 in self.grapheDict:
                if element["tache"] in element2["contraintes"]:
                    isSortie = False
            if isSortie:
                element["isSortie"] = "Sortie"

    def setAlphaOmega(self):
        """
        Set l'entrée et la sortie du graphe
        """
        self.grapheDict = [{"tache": "α",  # ou "0"
                            "duree": 0,
                            "contraintes": [],
                            "isEntree": "",
                            "isSortie": "",
                            "rang": 0,
                            "dateASAP": 0,
                            "dateALAP": 0}] + self.grapheDict
        self.grapheDict.append({"tache": "ω",  # ou str(int(element["tache"]) + 1)
                                "duree": 0,
                                "contraintes": [],
                                "isEntree": "",
                                "isSortie": "",
                                "rang": 0,
                                "dateASAP": 0,
                                "dateALAP": 0
                                })

        for element in self.grapheDict:
            if element["isEntree"] == "Entree":
                element["contraintes"].append("α") #ou "0"
            if element["isSortie"] == "Sortie":
                self.grapheDict[-1]["contraintes"].append(element["tache"])


    def setRang(self):
        """
        Set le rang de chaque tâche
        """
        newGraphe = self.__copy__()
        k = 0
        while newGraphe.grapheDict:
            howManyZeroInArc = 0
            temp = []

            #Check combien il y a de 0 dans les arcs
            for element in newGraphe.grapheDict:
                if len(element["contraintes"]) == 0:
                    howManyZeroInArc += 1

            # Tant qu'il y a des 0 dans les arcs, on met les rangs à k et on supprime les tâches
            while howManyZeroInArc != 0:
                for element in newGraphe.grapheDict:
                    # Si le rang est 0
                    if len(element["contraintes"]) == 0:
                        # On set le rang à k
                        for element2 in self.grapheDict:
                            if element2["tache"] == element["tache"]:
                                element2["rang"] = k

                        # On ajoute la tâche à la liste temporaire
                        temp.append(element["tache"])
                        # On supprime la tâche du graphe
                        newGraphe.grapheDict.remove(element)
                howManyZeroInArc -= 1

            # On supprime les tâches de la liste des contraintes
            for i in range(len(temp)):
                for element in newGraphe.grapheDict:
                    if temp[i] in element["contraintes"]:
                        element["contraintes"].remove(temp[i])
            k += 1





    def setGrapheDict(self):
        """
        Set le dictionnaire du graphe
        """
        for i in range(len(self.tache)):
            self.grapheDict.append({"tache": self.tache[i],
                                    "duree": self.duree[i],
                                    "contraintes": self.contraintes[i],
                                    "isEntree": "",
                                    "isSortie": "",
                                    "rang": 0,
                                    "dateASAP": 0,
                                    "dateALAP": 0})

    def checkEntreeSortie(self):
        """
        Vérifie si le graphe possède bien une entrée et une sortie et retourne vrai s'il y a au moins une entrée
        """
        onlyOneEntree = 0
        onlyOneSortie = 0
        for element in self.grapheDict:
            if element["isEntree"] == "Entree":
                onlyOneEntree += 1
            if element["isEntree"] == "Sortie":
                onlyOneSortie += 1
        if onlyOneEntree == 1 and onlyOneSortie == 1:
            self.onlyOneEntreeAndSortie = True
        elif onlyOneEntree >= 1:
            return True
        else:
            return False

    def checkCircuit(self):
        """
        Vérifie si le graphe possède un circuit
        """
        newGraphe = self.__copy__()
        while newGraphe.checkEntreeSortie():
            temp = []
            for element in newGraphe.grapheDict:
                if element["isEntree"] == "Entree":
                    temp.append(element["tache"])
                    newGraphe.grapheDict.remove(element)
            for element in newGraphe.grapheDict:
                for i in range(len(temp)):
                    if temp[i] in element["contraintes"]:
                        element["contraintes"].remove(temp[i])
            newGraphe.setType()
        if newGraphe.grapheDict:
            self.dontHaveCircuit = False

    def checkNegativeDuration(self):
        """
        Vérifie si le graphe possède une tâche avec une durée négative
        """
        for element in self.grapheDict:
            if int(element["duree"]) < 0:
                self.dontHaveNegativeDuration = False


    def getValueMatrix(self):
        """
        Renvoie la matrice des valeurs
        """

        matrix = beautifultable.BeautifulTable()
        for element in self.grapheDict:
            temp = []
            for element2 in self.grapheDict:
                if element["tache"] in element2["contraintes"]:
                    temp.append(element["tache"])
                else:
                    temp.append(" * ")
            matrix.rows.append(temp)

        headers = []
        for element in self.grapheDict:
            headers.append(" " + element["tache"] + " ")
        matrix.columns.header = headers
        matrix.rows.header = headers
        return matrix

    def dateASAP(self):
        """
        Renvoie la date ASAP de chaque tâche
        """
        k = 0
        while k <= self.grapheDict[-1]["rang"]:
            for element in self.grapheDict:
                if element["rang"] == k:
                    if element["rang"] == 0:
                        element["dateASAP"] = 0
                    else:
                        for element2 in self.grapheDict:
                            if element2["tache"] in element["contraintes"]:
                                temp = element["dateASAP"]
                                if temp < element2["dateASAP"] + int(element2["duree"]):
                                    element["dateASAP"] = element2["dateASAP"] + int(element2["duree"])
            k += 1

    def dateALAP(self):
        """
        Renvoie la date ALAP de chaque tâche
        """
        k = self.grapheDict[-1]["rang"]

        for element in self.grapheDict:
            element["dateALAP"] = self.grapheDict[-1]["dateASAP"]

        while k >= 0:
            for element in self.grapheDict:
                if element["rang"] == k:
                    if element["rang"] == self.grapheDict[-1]["rang"]:
                        element["dateALAP"] = element["dateASAP"]
                    else:
                        for element2 in self.grapheDict:
                            if element["tache"] in element2["contraintes"]:
                                temp = element["dateALAP"]
                                if temp > element2["dateALAP"] - int(element["duree"]):
                                    element["dateALAP"] = element2["dateALAP"] - int(element["duree"])
            k -= 1


    def __copy__(self):
        """
        Permet de copier un objet de la classe
        """
        newGraphe = Graphes(self.fichier.fichier)
        newGraphe.setTaskDureeContraintes()
        newGraphe.setGrapheDict()
        newGraphe.setType()
        newGraphe.checkEntreeSortie()
        return newGraphe


if __name__ == '__main__':
    # Tests de la classe locale
    configuration = Configuration()
    graphe = Graphes("test6.txt")

    graphe.checkCircuit()

    graphe.setRang()
    graphe.dateASAP()
    graphe.dateALAP()
    graphes = graphe.getValueMatrix()

    for element in graphe.grapheDict:
        print(element)

    #print(graphe.onlyOneEntreeAndSortie)
    #print(graphe.dontHaveCircuit)
    #print(graphe)
