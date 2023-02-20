"""
Projet Théorie des graphes L3 EFREI
    -
    -
    - Nathan RICARDO
    - Thomas SONG
    -

Cette classe permet de créer une table à la manière d'Excel pour afficher les automates
"""

import re
from struct import pack
import tkinter as tk
from tkinter import ttk
from turtle import color

from graphes import Graphes


class Sheet:
    """
    Classe pour créer un tableau d'affichage des états et transitions d'un automate, dans le style excel.
    """

    def __init__(self, frame: tk.Frame):
        self.master_frame = frame
        self.tableau_automate = ttk.Treeview(self.master_frame)

        # Création des scrollbars
        scroll_y = tk.Scrollbar(self.master_frame, orient="vertical", command=self.tableau_automate.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_y.update()
        self.scrollbar_width = scroll_y.winfo_reqwidth()
        self.width = 0

        scroll_x = tk.Scrollbar(self.master_frame, orient="horizontal", command=self.tableau_automate.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")
        # AutomateSheet scroll configuration
        self.tableau_automate.configure(yscrollcommand=scroll_y.set,
                                        xscrollcommand=scroll_x.set)
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

        self.tableau_automate.configure(height=nbr_lignes)

    def init_colonne(self):
        """
        Création des colonnes de la table
        """

        self.tableau_automate.configure(columns=self.table[0], show="headings")

    def init_en_tete(self):
        """
        Créer la première ligne de la table (E/S Etats a b etc.)
        """

        # En-têtes des colonnes centrés
        self.tableau_automate.heading("#0", text="", anchor=tk.CENTER)
        for i in range(0, len(self.tableau_automate['columns'])):
            self.tableau_automate.heading("#" + str(i + 1), text=self.tableau_automate['columns'][i])

    def colonne_initiale(self):
        """
        Création du tableau initial
        """

        self.tableau_automate['columns'] = ("E / S", "Etats", "stretch")
        self.tableau_automate.column("#0", width=0, stretch=tk.NO)
        self.tableau_automate.column("E / S", anchor=tk.CENTER, width=60, stretch=False)
        self.tableau_automate.column("Etats", anchor=tk.CENTER, width=60, stretch=False)
        self.tableau_automate.column("stretch", anchor=tk.CENTER, width=60, stretch=False)
        self.tableau_automate.heading("E / S", text="E / S", anchor=tk.CENTER)
        self.tableau_automate.heading("Etats", text="Etats", anchor=tk.CENTER)

    def efface_tableau(self):
        """
        Cette fonction permet d'effacer le tableau de l'automate
        """

        self.tableau_automate['columns'] = ()
        self.tableau_automate.delete(*self.tableau_automate.get_children())

    def update_tableau(self, graphe: Graphes):
        """
        Cette fonction redessine totalement la grille d'affichage de l'automate

        :param automate: L'automate à afficher
        """

        # On commence par supprimer toutes les lignes et colonnes
        self.efface_tableau()

        # On recrée totalement la grille en se basant sur la table de l'automate
        self.table = graphe.to_table()

        # # Mise à jour de la nouvelle table
        self.init_colonne()
        self.init_en_tete()

        # Insertion des lignes dans la table
        for index_ligne in range(1, len(self.table)):
            self.tableau_automate.insert(parent='', index='end', text='', values=(self.table[index_ligne]))

        # Et on essaye de mettre les colonnes à une taille "adaptée"
        sizes = self.retourne_taille_colonne(largeur_fonte=8, marge=25)
        for index_colonne in range(0, len(self.tableau_automate['columns'])):
            self.tableau_automate.column(f"#{index_colonne + 1}", width=sizes[index_colonne], stretch=False,
                                         anchor=tk.CENTER)

    def retourne_taille_colonne(self, largeur_fonte: int, marge: int) -> dict:
        """
        Cette fonction essaye de déterminer la taille max, en pixels, de chaque colonne de la table à afficher

        :param largeur_fonte: Largeur en pixel de la fonte utilisée pour l'affichage
        :param marge: Marge en pixel à ajouter à chaque colonne
        :return: Dictionnaire des tailles en pixel, les clés sont les numéros de colonne
        """

        taille_colonne_min = marge
        tailles = {}
        # Pour chaque ligne à afficher
        for index_ligne, row in enumerate(self.table):
            # Et pour chaque colonne
            for index_colonne, value in enumerate(self.table[index_ligne]):
                # On calcule la largeur d'une colonne
                taille = taille_colonne_min + (len(value) * largeur_fonte)
                # Et on ajoute au dictionnaire {numero_colonne: taille}
                if not tailles.get(index_colonne):
                    tailles[index_colonne] = taille
                if taille > tailles[index_colonne]:
                    tailles[index_colonne] = taille
        return tailles
