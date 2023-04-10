"""
Projet Théorie des graphes L3 EFREI
    - Yann SCARDIGLI
    - Pierre THAITE
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
        self.fichier = Lecture(os.path.join(self.config.graphes_path, fichier))
        self.grapheDict = []
        self.tache = []
        self.duree = []
        self.contraintes = []
        self.graphe_to_table = []
        self.onlyOneEntreeAndSortie = False
        self.dontHaveCircuit = True
        self.dontHaveNegativeDuration = True

        self.setTaskDureeContraintes()
        self.setGrapheDict()
        self.setType()
        self.setAlphaOmega()

        self.getValueMatrix()

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
        self.grapheDict = [{"tache": "0",  # ou "0"
                            "duree": 0,
                            "contraintes": [],
                            "isEntree": "",
                            "isSortie": "",
                            "rang": 0,
                            "dateASAP": 0,
                            "dateALAP": 0,
                            "margeTotale": None,
                            "margeLibre": None
                            }] + self.grapheDict

        self.grapheDict.append(
            {"tache": str(int(self.grapheDict[-1]["tache"]) + 1),  # ou str(int(element["tache"]) + 1)
             "duree": 0,
             "contraintes": [],
             "isEntree": "",
             "isSortie": "",
             "rang": 0,
             "dateASAP": 0,
             "dateALAP": 0,
             "margeTotale": None,
             "margeLibre": None
             })

        for element in self.grapheDict:
            if element["isEntree"] == "Entree":
                element["contraintes"].append("0")  # ou "0"
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

            # Check combien il y a de 0 dans les arcs
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

    def setdateASAP(self):
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

    def setdateALAP(self):
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

    def setMargeTotale(self):
        """
        Set la marge de chaque tâche
        """
        for element in self.grapheDict:
            element["margeTotale"] = element["dateALAP"] - element["dateASAP"]

    def setMargeLibre(self):
        """
        Set la marge libre de chaque tâche
        """
        for element in self.grapheDict:
            if element["rang"] == 0:
                element["margeLibre"] = 0
            else:
                temp = []
                for element2 in self.grapheDict:
                    if element["tache"] in element2["contraintes"]:
                        temp.append(element2["dateASAP"])
                if not temp:
                    element["margeLibre"] = 0
                else:
                    element["margeLibre"] = min(temp) - element["dateASAP"] - int(element["duree"])


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
                                    "dateALAP": 0,
                                    "margeTotale": None,
                                    "margeLibre": None})

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

    def getMatrixBeautifulTable(self):
        """
        Renvoie la matrice du graphe sous forme de tableau
        """
        matrix = beautifultable.BeautifulTable()
        matrix.maxwidth = 100
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
            headers.append(element["tache"])
        matrix.columns.header = headers
        matrix.rows.header = headers

        return matrix

    def getMatrix_withAllData(self):
        """
        Renvoie la matrice du graphe sous forme de tableau
        """
        matrix = beautifultable.BeautifulTable()
        matrix.maxwidth = 1000
        for element in self.grapheDict:
            temp = []
            for element2 in self.grapheDict:
                if element["tache"] in element2["contraintes"]:
                    temp.append(element["tache"])
                else:
                    temp.append(" * ")
            temp.append(element["rang"])
            temp.append(element["dateASAP"])
            temp.append(element["dateALAP"])
            temp.append(element["margeTotale"])
            temp.append(element["margeLibre"])
            matrix.rows.append(temp)

        headers = []
        row_headers = []
        for element in self.grapheDict:
            headers.append(element["tache"])
        row_headers = headers.copy()
        headers.append("rang")
        headers.append("dateASAP")
        headers.append("dateALAP")
        headers.append("margeTotale")
        headers.append("margeLibre")
        matrix.columns.header = headers
        matrix.rows.header = row_headers

        return matrix

    def getValueMatrix(self):
        """
        Renvoie la matrice des valeurs
        """
        matrix = self.getMatrixBeautifulTable()

        self.graphe_to_table = str(matrix).split("\n")
        self.graphe_to_table = [row.strip().split('|') for row in self.graphe_to_table if not row.startswith('+')]
        self.graphe_to_table[0] = self.graphe_to_table[0][1:]
        for i in range(1, len(self.graphe_to_table)):
            self.graphe_to_table[i] = [col.strip() for col in self.graphe_to_table[i] if col.strip()]
        self.graphe_to_table = [row for row in self.graphe_to_table if row]



        return matrix

    def removeNotZeroMarge(self, graphe):
        """
        Supprime les tâches qui n'ont pas de marge de 0
        """
        zeroMarge = False
        while not zeroMarge:
            for element in graphe.grapheDict:
                if element["margeTotale"] != 0:
                    graphe.grapheDict.remove(element)
            for element in graphe.grapheDict:
                if element["margeTotale"] == 0:
                    zeroMarge = True
                else:
                    zeroMarge = False
                    break
        return graphe


    def inDepthSearch(self, graphe):
        """
        Renvoie une liste du parcours en profondeur du graphe
        """
        temp = []
        traversalList = []
        visited = []
        for element in graphe.grapheDict:
            visited.append([element["tache"], False])
        visitedAll = False

        k = 0 #rang
        while not visitedAll:
            while k <= self.getHighestRank(visited)[0]:
                for element in graphe.grapheDict:
                    i = None
                    if element["rang"] == k:
                        for element2 in visited:
                            if element["tache"] in element2[0]:
                                i = visited.index(element2)
                                break
                        if not visited[i][1]:
                            if not temp:
                                temp.append(element["tache"])
                                visited[i][1]  = True
                                graphe.grapheDict.remove(element)
                            else:
                                if element["tache"] not in temp:
                                    if temp[-1] in element["contraintes"]:
                                        temp.append(element["tache"])
                                        visited[i][1]  = True
                                        graphe.grapheDict.remove(element)
                k += 1
            visited = []
            traversalList.append(temp)
            temp = []
            k = 0
            for element in graphe.grapheDict:
                visited.append([element["tache"], False])
            if not visited:
                visitedAll = True

        return traversalList


    def getCriticalPath(self):
        """
        Renvoie le(s) chemin(s) critique(s)
        """
        newGraphe = self.__copy__()
        newGraphe.setRang()
        newGraphe.setdateASAP()
        newGraphe.setdateALAP()
        newGraphe.setMargeTotale()

        newGraphe = self.removeNotZeroMarge(newGraphe)
        criticalPath = self.inDepthSearch(newGraphe)


        return criticalPath

    def getHighestRank(self, temp):
        """
        Renvoie le rang le plus haut
        """
        task = 0
        stop_condition = 0
        for i in range(len(temp)):
            for element in self.grapheDict:
                if element["tache"] == temp[i][0] and stop_condition < element["rang"]:
                    stop_condition = element["rang"]
                    task = element["tache"]
        return stop_condition, task


    def __copy__(self):
        """
        Permet de copier un objet de la classe
        """
        newGraphe = Graphes(self.fichier.fichier)
        newGraphe.setTaskDureeContraintes()
        newGraphe.setType()
        newGraphe.checkEntreeSortie()
        return newGraphe


if __name__ == '__main__':
    # Tests de la classe locale
    graphe = Graphes("table 1.txt")

    print(graphe.getValueMatrix())
    graphe.checkCircuit()
    graphe.checkNegativeDuration()


    """graphe.setRang()
    graphe.setdateASAP()
    graphe.setdateALAP()
    graphe.setMargeTotale()
    graphe.setMargeLibre()
    graphes = graphe.getValueMatrix()

    criticalPath = graphe.getCriticalPath()"""
    """for element in graphe.grapheDict:
        print(element)"""

    #print(criticalPath)

    # print(graphe.onlyOneEntreeAndSortie)
    # print(graphe.dontHaveCircuit)
    # print(graphe)
