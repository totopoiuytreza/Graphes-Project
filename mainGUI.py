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
from fonction_fichiers import retourne_liste_des_fichiers
from config import Configuration


class AppAutomate(tk.Tk):
    def __init__(self):
        # Initialisation de la classe parente
        super().__init__()

        # Fenêtre
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
        # On centre la fenêtre dans l'écran, au lancement.
        largeur_ecran = self.winfo_screenwidth()
        hauteur_ecran = self.winfo_screenheight()
        self.geometry(
            f'{self.Largeur}x{self.Hauteur}+{int((largeur_ecran - self.Largeur) / 2)}+{int((hauteur_ecran - self.Hauteur) / 2)}')
        # Taille non modifiable.
        self.resizable(width=False, height=False)
        # Configuration de l'application
        self.cfg = Configuration()

        # Déclaration des variables qui vont servir dans toute la classe.
        self.filepath: str | None = None
        self.fichiers: dict | None = None

        # Automate en cours de traitement et d'affichage.
        self.graphe_courant: Graphes | None = None

        """# On essaie d'initialiser graphviz, une seule fois. On pourra vérifier par la suite, si on peut l'utiliser ou pas.
        self.graphe = ToGraphviz()
        if not self.graphe.check:
            print("Graphviz ne fonctionne pas sur cet ordinateur.")"""

        # Titre principal
        self.frmTitre: tk.Frame | None = None
        self.menu_LabelTitre: tk.Label | None = None

        # Menu des graphes
        self.frmSelection: tk.Frame | None = None
        self.menu_selection_LabelTitre: tk.Label | None = None
        self.graphe_choice = tk.StringVar()
        #self.menu_filter: AutocompleteEntry | None = None
        #self.menu_selection: AutocompleteCombobox | None = None
        self.menu_file_chooser: tk.Button | None = None

        # Gestion des options utilisables
        self.frmOptions: tk.Frame | None = None
        self.option_choisie = tk.StringVar()
        self.btn_confirm: tk.Button | None = None
        self.btn_affichage_graphe: tk.Button | None = None

        # Partie affichage des automates et de leurs status
        self.frmResultats: tk.Frame | None = None
        self.sheet: tk.Frame | None = None
        self.frameConsole: tk.Frame | None = None
        #self.ConsoleTexte: Console | None = None
        self.frmSheet: tk.Frame | None = None

        # Chargement des images que nous utilisons dans l'application
        self.imageCross = tk.PhotoImage(file=os.path.join(self.cfg.ressources_path, "crossmark.png"))
        self.imageMark = tk.PhotoImage(file=os.path.join(self.cfg.ressources_path, "checkmark.png"))
        self.imageLoad = tk.PhotoImage(file=os.path.join(self.cfg.ressources_path, "load.png"))
        self.imageLoad_size = (8, 8)
        self.imageLoad = self.imageLoad.subsample(x=8, y=8)

        # Lance l'application elle-même
        self.page_menu = tk.Frame(master=self, bg="black", width=self.Largeur, height=self.Hauteur)
        self.page_menu.grid_propagate(False)
        self.page_menu.grid()
        self.widgets()


    def widgets(self):
        """
        Cette fonction permet de créer les widgets de l'application.
        """

        # Titre principal
        self.frmTitre = tk.Frame(master=self.page_menu, bg="black", width=self.Largeur, height=50)
        self.frmTitre.grid_propagate(False)

        self.frmSelection = tk.Frame(master=self.page_menu, bg="black", width=self.Largeur, height=50)
        self.frmSelection.grid_propagate(False)
        self.menu_selection_LabelTitre = tk.Label(master=self.frmSelection, text="Selectionnez un graphe", bg="black",
                                                    fg="white", font=("Arial", 20))


    def widget_grid(self):

        pass



if __name__ == '__main__':
    appAutomate = AppAutomate()
    appAutomate.title("Gestion Automates - EFREI 2022")

    appAutomate.mainloop()
