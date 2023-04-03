"""
Projet Théorie des graphes L3 EFREI
    - Yann SCARDIGLI
    - Pierre THAITE
    - Nathan RICARDO
    - Thomas SONG
    -

Cette classe permet de créer une table à la manière d'Excel pour afficher les graphes
"""

import re
from struct import pack
import tkinter as tk
from tkinter import ttk
from turtle import color

from graphes import Graphes


class Sheet:
    """
    Classe pour créer le tableau des variables du graphe
    """

    def __init__(self, frame: tk.Frame):
        self.master_frame = frame
        self.style = ttk.Style(self.master_frame)
        self.style.configure("Custom.Treeview", rowheight=20, font=('Helvetica', 10), bordercolor="black", borderwidth=1)
        self.tableau_graphes = ttk.Treeview(self.master_frame, style="Custom.Treeview")
        self.tableau_graphes.grid_propagate(False)

        # Création des scrollbars
        scroll_y = tk.Scrollbar(self.master_frame, orient="vertical", command=self.tableau_graphes.yview)
        scroll_y.grid(row=1, column=1, sticky="ns")
        scroll_y.update()
        self.scrollbar_width = scroll_y.winfo_reqwidth()
        self.width = 0

        # GrapheSheet scroll configuration
        self.tableau_graphes.configure(yscrollcommand=scroll_y.set)
        self.table = None


    def set_width(self, master_framesize: int):
        """
        Calcul de la taille de la frame, on se base sur une taille de la frame externe fournie en paramètre

        :param master_framesize: Taille de la frame principale
        """

        self.width = master_framesize - self.scrollbar_width


    def set_lines(self, nbr_lignes: int):
        """
        Fonction qui fixe le nombre de lignes à afficher dans la liste.

        :param nbr_lignes: Le nombre de lignes
        """

        self.tableau_graphes.configure(height=nbr_lignes)

    def init_colonne(self):
        """
        Création des colonnes de la table
        """
        self.tableau_graphes.configure(columns=self.table[0], show="headings")
        self.init_en_tete()

    def init_en_tete(self):
        """
        Création des en-têtes de la table
        """
        self.tableau_graphes.heading("#0", text="", anchor=tk.CENTER)
        for i in range(len(self.tableau_graphes["columns"])):
            self.tableau_graphes.heading("#" + str(i + 1), text=self.tableau_graphes["columns"][i], anchor=tk.CENTER)

    def remove_data(self):
        """
        Supprime les données de la table
        """
        self.tableau_graphes["columns"] = ()
        self.tableau_graphes.delete(*self.tableau_graphes.get_children())

    def set_data(self, graphes: Graphes):
        """
        Fonction qui permet de mettre à jour les données de la table
        """

        self.remove_data()

        self.table = graphes.graphe_to_table

        self.init_colonne()

        for i in range(1, len(self.table)):
            self.tableau_graphes.insert(parent="", index="end", values=self.table[i])

        for i in range(len(self.tableau_graphes["columns"])):
            self.tableau_graphes.column("#" + str(i + 1), minwidth=25, stretch=True, anchor=tk.CENTER)

    def set_Rank(self, graphes: Graphes):
        """
        Fonction qui permet de mettre à jour les données de la table
        """
        temp = []
        temp.append("Rang")



        i = 1
        for element in graphes.grapheDict:
            if int(element["tache"]) == int(self.table[0][i]):
                temp.append(element["rang"])
            i += 1
        self.table.append(temp)
        self.remove_data()

        self.init_colonne()

        for i in range(1, len(self.table)):
            self.tableau_graphes.insert(parent="", index="end", values=self.table[i])

        for i in range(len(self.tableau_graphes["columns"])):
            self.tableau_graphes.column("#" + str(i + 1), minwidth=25, stretch=True, anchor=tk.CENTER)

    def set_dateASAP(self, graphes: Graphes):
        """
        Fonction qui permet de mettre à jour les données de la table
        """

        temp = []
        temp.append("ASAP")

        i = 1
        for element in graphes.grapheDict:
            if int(element["tache"]) == int(self.table[0][i]):
                temp.append(element["dateASAP"])
            i += 1
        self.table.append(temp)
        self.remove_data()

        self.init_colonne()

        for i in range(1, len(self.table)):
            self.tableau_graphes.insert(parent="", index="end", values=self.table[i])

        for i in range(len(self.tableau_graphes["columns"])):
            self.tableau_graphes.column("#" + str(i + 1), minwidth=25, stretch=True, anchor=tk.CENTER)

    def set_dateALAP(self, graphes: Graphes):
        """
        Fonction qui permet de mettre à jour les données de la table
        """

        temp = []
        temp.append("ALAP")

        i = 1
        for element in graphes.grapheDict:
            if int(element["tache"]) == int(self.table[0][i]):
                temp.append(element["dateALAP"])
            i += 1

        self.table.append(temp)
        self.remove_data()

        self.init_colonne()

        for i in range(1, len(self.table)):
            self.tableau_graphes.insert(parent="", index="end", values=self.table[i])

        for i in range(len(self.tableau_graphes["columns"])):
            self.tableau_graphes.column("#" + str(i + 1), minwidth=25, stretch=True, anchor=tk.CENTER)

    def set_marge(self, graphes: Graphes):
        """
        Fonction qui permet de mettre à jour les données de la table
        """

        temp = []
        temp2 = []
        temp.append("MargeT")
        temp2.append("MargeL")

        i = 1
        for element in graphes.grapheDict:
            if int(element["tache"]) == int(self.table[0][i]):
                temp.append(element["margeTotale"])
                temp2.append(element["margeLibre"])
            i += 1

        self.table.append(temp)
        self.table.append(temp2)
        self.remove_data()

        self.init_colonne()

        for i in range(1, len(self.table)):
            self.tableau_graphes.insert(parent="", index="end", values=self.table[i])

        for i in range(len(self.tableau_graphes["columns"])):
            self.tableau_graphes.column("#" + str(i + 1), minwidth=25, stretch=True, anchor=tk.CENTER)






