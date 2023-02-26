"""
Projet Théorie des graphes L3 EFREI
    -
    -
    - Nathan RICARDO
    - Thomas SONG
    -

Gestion de l'interface graphique utilisateur
"""

import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

from graphes import Graphes
from Sheet import Sheet
from visual_graphe import ToGraphviz
from config import Configuration


class AppGraphe(tk.Tk):
    def __init__(self):
        # Initialisation de la classe parente
        super().__init__()

        """
        Cette partie permet de créer la page vide avec les propriétés suivantes:
            - Titre de l'application : "GrapheReader"
            - Longueur : 900px
            - Largeur : 675px
            - Taille de l'écran en fonction de la taille d'écran de l'utilisateur
            - Taille non modifiable
        """
        # Taille de la fenêtre
        self.Largeur = 900
        self.Hauteur = 675

        # Configuration de l'application
        self.cfg = Configuration()

        # Déclaration des variables qui vont servir dans toute la classe.
        self.filepath: str | None = None
        self.fichiers: dict | None = None

        self.liste_graphes: list | None = None

        # Automate en cours de traitement et d'affichage.
        self.graphe_courant: Graphes | None = None

        #Image utilisée dans l'application
        self.imageLoad = tk.PhotoImage(file=os.path.join(self.cfg.ressources_path, "load.png"))
        self.imageLoad = self.imageLoad.subsample(x=8, y=8)
        self.imageCross = tk.PhotoImage(file=os.path.join(self.cfg.ressources_path, "crossmark.png"))
        self.imageMark = tk.PhotoImage(file=os.path.join(self.cfg.ressources_path, "checkmark.png"))

        # Création du menu et des 4 pages de l'application
        self.page_menu = tk.Frame(master=self, bg="black", width=self.Largeur, height=self.Hauteur)
        self.page_menu.grid_propagate(False)
        self.page_menu.grid()
        self.page_boutons = tk.Frame(master=self.page_menu, bg="white", width=(self.Largeur / 3) - 5,
                                     height=2*((self.Hauteur / 3) - 5))
        self.page_info = tk.Frame(master=self.page_menu, bg="white", width=2*((self.Largeur / 3) - 5),
                                  height=(self.Hauteur / 3) - 5)
        self.page_choix = tk.Frame(master=self.page_menu, bg="white", width=(self.Largeur / 3) - 5,
                                   height=(self.Hauteur / 3) - 5)
        self.page_tableau = tk.Frame(master=self.page_menu, bg="white", width=2*((self.Largeur / 3) - 5),
                                     height=2*((self.Hauteur / 3) - 5))
        self.page_tableau.grid_rowconfigure(0, weight=0)
        self.page_tableau.grid_rowconfigure(1, weight=1)
        self.page_tableau.grid_columnconfigure(0, weight=1)



        self.createWindow()
        self.createPage()


    def createWindow(self):
        """
        Cette fonction permet de créer la fenêtre de l'application.
        """
        # On centre la fenêtre dans l'écran, au lancement.
        largeur_ecran = self.winfo_screenwidth()
        hauteur_ecran = self.winfo_screenheight()
        self.geometry(
            f'{self.Largeur}x{self.Hauteur}+{int((largeur_ecran - self.Largeur) / 2)}+{int((hauteur_ecran - self.Hauteur) / 2)}')
        # Taille non modifiable.
        self.resizable(width=False, height=False)

    def createPage(self):
        """
        Cette fonction permet de la page de l'application.
        """

        #Creation de la page information
        self.page_info.grid_propagate(False)
        self.page_info_label = tk.Label(master=self.page_info, text="Information", bg="white", fg="black", font=("Arial", 12))
        self.page_info_graphe_name = tk.Label(master=self.page_info, text="Nom du graphe: ", bg="white", fg="black", font=("Arial", 10))
        self.page_info_graphe_name_value = tk.Label(master=self.page_info, text="Aucun", bg="white", fg="black", font=("Arial", 10))
        self.page_info_graphe_circuit_verif = tk.Label(master=self.page_info, text="Pas de Circuit: ", bg="white", fg="black", font=("Arial", 10))
        self.page_info_graphe_circuit_verif_value = tk.Label(master=self.page_info, text="Not Verified", bg="white", fg="black", font=("Arial", 10))
        self.page_info_graphe_arc_verif = tk.Label(master=self.page_info, text="Pas d'arcs négatifs: ", bg="white", fg="black", font=("Arial", 10))
        self.page_info_graphe_arc_verif_value = tk.Label(master=self.page_info, text="Not Verified", bg="white", fg="black", font=("Arial", 10))

        #Creation de la page choix des graphes
        self.page_choix.grid_propagate(False)
        self.page_choix_label = tk.Label(master=self.page_choix, text="Choix des graphes", bg="white", fg="black", font=("Arial", 12))
        self.page_choix_combobox = ttk.Combobox(master=self.page_choix, values=self.liste_graphes, state="readonly", width=30)
        self.page_choix_combobox.bind("<<ComboboxSelected>>", lambda event: self.verifGrapheChoice())
        self.page_choix_repertory = tk.Button(master=self.page_choix, borderwidth=0, relief=tk.FLAT, image=self.imageLoad, command=self.choose_path)

        #Creation de la page tableau de variables
        self.page_tableau.grid_propagate(False)
        self.page_tableau_label = tk.Label(master=self.page_tableau, text="Tableau de variables", bg="white", fg="black", font=("Arial", 12))
        self.page_tableau_treeview = Sheet(self.page_tableau)

        #Creation de la page choix des boutons
        self.page_boutons.grid_propagate(False)
        self.page_boutons_label = tk.Label(master=self.page_boutons, text="Boutons", bg="white", fg="black", font=("Arial", 12))
        self.page_boutons_ordonnancement_verif = tk.Button(master=self.page_boutons, text="Verification du graphe", bg="white", fg="black", font=("Arial", 10),
                                                           command=lambda: self.verifOrdonnancement())
        self.page_boutons_ordonnancement_verif.configure(state="disabled")
        self.page_boutons_affiche_graphe = tk.Button(master=self.page_boutons, text="Show the graphe", bg="white", fg="black", font=("Arial", 10),
                                                     command=lambda: self.showGraphe())
        self.page_boutons_affiche_graphe.configure(state="disabled")


        # Placement des pages
        self.page_info.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        self.page_choix.grid(row=0, column=1, sticky="ne", pady=5)
        self.page_tableau.grid(row=1, column=0, sticky="se", padx=5)
        self.page_boutons.grid(row=1, column=1, sticky="sw")

        # Placement des titres des pages
        self.page_info_label.grid(row=0, column=0, sticky="nw", pady=5)
        self.page_choix_label.grid(row=0, column=0, sticky="nw", pady=5)
        self.page_tableau_label.grid(row=0, column=0, sticky="nw", pady=5)
        self.page_boutons_label.grid(row=0, column=0, sticky="nw", pady=5)

        """self.page_info.grid(row=0, column=0, sticky="nw", padx=5, pady=5, columnspan=2)
        self.page_choix.grid(row=0, column=2, sticky="ne", pady=5)
        self.page_tableau.grid(row=1, column=0, sticky="se", padx=5, rowspan=2, columnspan=2)
        self.page_boutons.grid(row=1, column=2, sticky="sw", columnspan=2)"""

        # Placement dans la page information
        self.page_info_graphe_name.grid(row=1, column=0, sticky="nw")
        self.page_info_graphe_name_value.grid(row=1, column=1, sticky="nw")
        self.page_info_graphe_circuit_verif.grid(row=2, column=0, sticky="nw")
        self.page_info_graphe_circuit_verif_value.grid(row=2, column=1, sticky="nw")
        self.page_info_graphe_arc_verif.grid(row=3, column=0, sticky="nw")
        self.page_info_graphe_arc_verif_value.grid(row=3, column=1, sticky="nw")

        # Placement dans la page choix des graphes
        self.page_choix_combobox.grid(row=1, column=0, sticky="nw", padx=5)
        self.page_choix_repertory.grid(row=1, column=1, sticky="nw")

        # Placement dans la page tableau de variables
        self.page_tableau_treeview.tableau_graphes.grid(row=1, column=0, sticky="nwes", padx=5, pady=5)

        #Placement dans la page choix des boutons
        self.page_boutons_ordonnancement_verif.grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        self.page_boutons_affiche_graphe.grid(row=2, column=0, sticky="nw", padx=5, pady=5)


    def choose_path(self):
        """
        Fonction permettant de choisir le repertoire contenant les graphes
        """
        self.filepath = filedialog.askdirectory(initialdir=self.cfg.graphes_path, title="Select the folder of the graphes", mustexist=True)

        if self.filepath:
            self.fichiers = os.listdir(self.filepath)
            self.page_choix_combobox.config(values=self.fichiers)
        else:
            self.fichiers = []
            self.page_choix_combobox.config(values=self.fichiers)

    def verifGrapheChoice(self):
        """
        Fonction permettant de verifier si un graphe a été choisi
        """

        if not self.fichiers and not self.filepath:
            return

        self.graphe_courant = Graphes(self.filepath + "/" + self.page_choix_combobox.get())

        if not self.graphe_courant:
            messagebox.showerror("Erreur", "Le graphe n'a pas pu être chargé")
            return

        self.page_tableau_treeview.set_data(self.graphe_courant)
        self.resetValue()
        self.page_boutons_ordonnancement_verif.configure(state="normal")
        self.page_boutons_affiche_graphe.configure(state="normal")

    def verifOrdonnancement(self):
        """
        Fonction permettant de verifier si un graphe est d'ordonnancement
        """

        self.graphe_courant.checkCircuit()
        self.graphe_courant.checkNegativeDuration()

        if self.graphe_courant.dontHaveCircuit:
            self.page_info_graphe_circuit_verif_value.config(image=self.imageMark)
        else:
            self.page_info_graphe_circuit_verif_value.config(image=self.imageCross)

        if self.graphe_courant.dontHaveNegativeDuration:
            self.page_info_graphe_arc_verif_value.config(image=self.imageMark)
        else:
            self.page_info_graphe_arc_verif_value.config(image=self.imageCross)

        if self.graphe_courant.dontHaveCircuit and self.graphe_courant.dontHaveNegativeDuration:
            self.graphe_courant.setRang()
            self.graphe_courant.setdateASAP()
            self.graphe_courant.setdateALAP()
            self.graphe_courant.setMarge()
            self.page_tableau_treeview.set_Rank(self.graphe_courant)
            self.page_tableau_treeview.set_dateASAP(self.graphe_courant)
            self.page_tableau_treeview.set_dateALAP(self.graphe_courant)
            self.page_tableau_treeview.set_marge(self.graphe_courant)




    def resetValue(self):
        """
        Fonction permettant de remettre les valeurs des labels à 0
        """
        self.page_info_graphe_circuit_verif_value.config(text="Not Verified", image="")
        self.page_info_graphe_arc_verif_value.config(text="Not Verified", image="")


    def showGraphe(self):
        """
        Fonction permettant d'afficher le graphe
        """
        graph = ToGraphviz()
        if graph.check:
            print("Graphviz est installé")
            print(graph.graphe_to_graph(self.graphe_courant, visualiser=True))











if __name__ == '__main__':
    appGraphe = AppGraphe()
    appGraphe.title("Gestion Graphes - EFREI 2023")

    appGraphe.mainloop()
