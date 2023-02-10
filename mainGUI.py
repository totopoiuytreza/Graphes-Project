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
        self.automate_courant: Automate | None = None

        # On essaie d'initialiser graphviz, une seule fois. On pourra vérifier par la suite, si on peut l'utiliser ou pas.
        self.graphe = ToGraphviz()
        if not self.graphe.check:
            print("Graphviz ne fonctionne pas sur cet ordinateur.")

        self.deja_minimise = False

        # Titre principal
        self.frmTitre: tk.Frame | None = None
        self.menu_LabelTitre: tk.Label | None = None

        # Menu des graphes
        self.frmSelection: tk.Frame | None = None
        self.menu_selection_LabelTitre: tk.Label | None = None
        self.automate_choice = tk.StringVar()
        self.menu_filter: AutocompleteEntry | None = None
        self.menu_selection: AutocompleteCombobox | None = None
        self.menu_file_chooser: tk.Button | None = None

        # Gestion des options utilisables
        self.frmOptions: tk.Frame | None = None
        self.option_choisie = tk.StringVar()
        self.option_determinisation_et_completion: tk.Radiobutton | None = None
        self.optionMinimisation: tk.Radiobutton | None = None
        self.optionComplementarisation: tk.Radiobutton | None = None
        self.optionStandardisation: tk.Radiobutton | None = None
        self.option_lire_mot: tk.Radiobutton | None = None
        self.option_ecrire_mot: tk.Entry | None = None
        self.btn_confirm: tk.Button | None = None
        self.btn_affichage_graphe: tk.Button | None = None
        self.btn_reindexer: tk.Button | None = None

        # Partie affichage des automates et de leurs status
        self.frmResultats: tk.Frame | None = None
        self.sheet: tk.Frame | None = None
        self.frameConsole: tk.Frame | None = None
        self.ConsoleTexte: Console | None = None
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
        self.widgets_grid()
        # self.MenuSelection()

    def widgets(self):
        """
        Définition des frames et widgets de la page
        """

        # Titre principal
        self.frmTitre = tk.Frame(self.page_menu, bg="black")
        self.menu_LabelTitre = tk.Label(self.frmTitre, text="Menu des sélections", bg="black", fg="white",
                                        font=('Bahnschrift SemiBold', 15, 'bold'))

        # Selection automate
        self.frmSelection = tk.Frame(self.page_menu, bg="black")
        self.menu_selection_LabelTitre = tk.Label(self.frmSelection, text="Choisir un automate : ", bg="black",
                                                  fg="white",
                                                  font=('Bahnschrift SemiBold', 14, 'bold'))
        # Gestion du filtre pour faciliter la recherche dans la combobox
        self.menu_selection = AutocompleteCombobox(self.frmSelection)
        self.menu_selection.config(textvariable=self.automate_choice, state="readonly",
                                   font=('Bahnschrift SemiBold', 12, 'bold'))
        self.menu_selection.bind("<<ComboboxSelected>>", lambda event: self.verif_choix_automate())

        self.menu_filter = AutocompleteEntry(master=self.frmSelection, cb=self.menu_selection)
        self.menu_filter.config(width=20, font=('Bahnschrift SemiBold', 10))
        # On mappe les return du clavier pour valider la saisie.
        self.menu_filter.bind("<Return>", lambda event: self.entry_validation())
        self.menu_filter.bind("<KP_Enter>", lambda event: self.entry_validation())
        self.menu_file_chooser = tk.Button(self.frmSelection, image=self.imageLoad,
                                           borderwidth=0, relief=tk.FLAT,
                                           command=self.choose_path)

        # Options utilisables sur un automate
        self.frmOptions = tk.Frame(self.page_menu, bg="black")
        self.option_determinisation_et_completion = tk.Radiobutton(self.frmOptions,
                                                                   text="Déterminisation Et Complétion", bg="black",
                                                                   fg="white", selectcolor="black",
                                                                   variable=self.option_choisie,
                                                                   value="DC",
                                                                   command=self.verifOptionChoisie)
        self.optionMinimisation = tk.Radiobutton(self.frmOptions, text="Minimisation", bg="black", fg="white",
                                                 selectcolor="black",
                                                 variable=self.option_choisie, value="Minimisation",
                                                 command=self.verifOptionChoisie)
        self.optionComplementarisation = tk.Radiobutton(self.frmOptions, text="Complémentarisation", bg="black",
                                                        fg="white", selectcolor="black",
                                                        variable=self.option_choisie, value="Complementarisation",
                                                        command=self.verifOptionChoisie)
        self.optionStandardisation = tk.Radiobutton(self.frmOptions, text="Standardisation", bg="black",
                                                    fg="white", selectcolor="black",
                                                    variable=self.option_choisie, value="Standardisation",
                                                    command=self.verifOptionChoisie)
        self.option_lire_mot = tk.Radiobutton(self.frmOptions, text="Lire Mot", bg="black",
                                              fg="white", selectcolor="black",
                                              variable=self.option_choisie, value="Lire Mot",
                                              command=self.verifOptionChoisie)
        self.option_ecrire_mot = tk.Entry(self.frmOptions, bg="white", width=20, foreground="red")
        self.option_ecrire_mot.configure(state="disabled")
        self.btn_confirm = tk.Button(self.frmOptions, text="CONFIRMER", bg="black", fg="white",
                                     font=('Bahnschrift SemiBold', 14, 'bold'), state="disabled",
                                     command=lambda: self.verifOptionExecution())
        # On affiche le bouton d'affichage des graphes que si graphviz est disponible sur le système
        if self.graphe.check:
            self.btn_affichage_graphe = tk.Button(self.frmOptions, text="Afficher Graphe",
                                                  command=lambda: self.affichegraphe())

        self.btn_reindexer = tk.Button(self.frmOptions, text="Réindexer",
                                       command=self.reindexer_automate)

        # Gestion des analyses des automates
        self.frmResultats = tk.Frame(self.page_menu, bg="black")
        # Création de la frame de la console
        self.frameConsole = tk.Frame(self.frmResultats, bg="black")
        # Création de la console
        self.ConsoleTexte = Console(self.frameConsole, self.imageCross, self.imageMark)
        self.frmSheet = tk.Frame(self.frmResultats, bg="lightgrey")
        self.sheet = Sheet(frame=self.frmSheet)
        self.sheet.colonne_initiale()

    def widgets_grid(self):
        """
        Cette fonction positionne tous les widgets et frames dans la page
        """

        # On force à prendre toute la largeur de la fenêtre
        self.page_menu.columnconfigure(index=0, minsize=self.Largeur)

        # Titre principal
        row = 0
        self.frmTitre.configure(bg="black")
        self.menu_LabelTitre.grid(row=row, column=0)
        # On place le label au milieu de l'écran...
        self.frmTitre.grid(row=row, column=0, padx=(self.Largeur / 2) - (self.menu_LabelTitre.winfo_reqwidth() / 2),
                           sticky="w")

        # Choix automate
        row += 1
        self.frmSelection.columnconfigure(index=1, minsize=150)
        self.menu_selection_LabelTitre.grid(row=0, column=0, sticky="w", pady=5)
        # On met un label pour "gagner" une colonne
        # tk.Label(self.frmSelection, text="", bg=self.frmSelection["background"]).grid(row=0, column=1)
        self.menu_filter.grid(row=0, column=2, padx=5)
        self.frmSelection.columnconfigure(index=3, minsize=300)
        self.menu_selection.grid(row=0, column=3, padx=5, sticky="we")
        self.menu_file_chooser.grid(row=0, column=4, padx=5, sticky="e")
        self.frmSelection.grid(row=row, column=0, sticky="w")

        # Options disponibles pour un automate
        row += 1
        # Options disponibles pour transformer un automate
        self.option_determinisation_et_completion.grid(row=0, column=0, padx=10)
        self.optionMinimisation.grid(row=0, column=1, padx=10)
        self.optionComplementarisation.grid(row=0, column=2, padx=10)
        self.optionStandardisation.grid(row=0, column=3, padx=10)
        self.option_lire_mot.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.option_ecrire_mot.grid(row=1, column=1, padx=0, pady=10, sticky="w")
        self.btn_confirm.grid(row=2, column=1, columnspan=2, pady=20)
        # On affiche le bouton d'affichage des graphes que si graphviz est disponible sur le système
        if self.graphe.check:
            self.btn_affichage_graphe.grid(row=3, column=0, sticky="e")
        self.btn_reindexer.grid(row=3, column=2, sticky="w")
        # On centre la frame avec padx
        self.frmOptions.update()
        self.frmOptions.grid(row=row, column=0,
                             padx=(self.Largeur / 2) - (self.frmOptions.winfo_reqwidth() / 2), pady=20,
                             sticky="w")

        # Affichages des résultats
        row += 1
        padx = 10
        padCol = 50
        rowSize = 350
        self.frmResultats.grid(row=row, column=0, padx=padx, sticky="w")
        self.frmResultats.rowconfigure(index=0, minsize=rowSize)
        # Calcul du bord droit de la frame
        frmResultatsWidth = self.Largeur - self.ConsoleTexte.width - padCol - (padx * 2)
        self.frmResultats.columnconfigure(index=0, minsize=self.ConsoleTexte.width)
        self.frmResultats.columnconfigure(index=1, minsize=padCol)
        self.frmResultats.columnconfigure(index=2, minsize=frmResultatsWidth)
        self.frameConsole.grid(row=0, column=0, sticky="nw")
        self.frameConsole.update()
        self.sheet.set_width(frmResultatsWidth)
        # Calcul empirique du nombre de lignes...
        self.sheet.set_lines(17)
        self.ConsoleTexte.set_lines(15)
        # Et on fixe les tailles des frames
        self.frmSheet.columnconfigure(0, minsize=self.sheet.width)
        self.frmSheet.rowconfigure(0, minsize=rowSize)
        self.frmSheet.grid(row=0, column=2, sticky="nw")
        self.sheet.tableau_automate.grid(row=0, column=0, sticky="nw")

    def redessine_tableau(self):
        """
        Cette fonction redessine le tableau des états et transitions de l'automate courant.
        """

        # On cache la frame du tableau, on le remplit, on force sa taille, et enfin on l'affiche à nouveau.
        # C'est le moyen pour forcer la frame à changer sa taille. Sinon, on sort de l'écran.
        self.sheet: Sheet
        self.frmSheet.grid_remove()
        self.sheet.update_tableau(self.automate_courant)
        self.frmSheet.columnconfigure(0, minsize=self.sheet.width)
        self.frmSheet.grid()

    def verif_choix_automate(self):
        """
        Vérifie si un automate a été choisi, si OUI, on donne la possibilité de choisir les options
        """

        # Met à jour l'automate
        if not self.fichiers or not self.filepath:
            # On sort si tout n'est pas encore en place
            return
        self.automate_courant = init_automate_from_file(
            os.path.join(self.filepath, self.fichiers[self.menu_selection.get()]))
        if not self.automate_courant:
            messagebox.showinfo("Erreur", "L'automate choisi n'est pas conforme")
            return

        self.deja_minimise = False
        self.redessine_tableau()
        self.ConsoleTexte.update_propriete_automate(self.automate_courant)

        if self.menu_selection.get() != "":
            # Autorise l'utilsation des options
            self.option_determinisation_et_completion.configure(state="active")
            self.optionMinimisation.configure(state="active")
            self.optionComplementarisation.configure(state="active")
            self.optionStandardisation.configure(state="active")

            # Informe l'utilisateur qu'un automate a été choisi
            self.ConsoleTexte.add_message(f"Automate choisi : {self.menu_selection.get()}")

    def verifOptionChoisie(self):
        """
            Cette fonction vérifie si une option a été choisie et active le bouton d'exécution si c'est le cas.
        """

        # Vérifie si un automate a été choisi
        if self.menu_selection.get() != "":
            # Vérifie si une option a été choisie
            if self.option_choisie.get() != "":
                # Si l'option Lire Mot est choisi, donne la possibilité d'écrire le mot à lire
                if self.option_choisie.get() == "Lire Mot":
                    self.option_ecrire_mot.configure(state="normal")
                # Qu'importe le choix, donne la possibilité d'exécuter l'option (même si le mot n'a pas encore
                # été écrit)
            self.btn_confirm.configure(state="active")

    def choose_path(self):
        """
        Cette fonction est appelée par le bouton de chargement de l'interface.
        L'utilisateur devra choisir un répertoire contenant les automates. Si le répertoire est vide, tout est remis
        à 0.
        """

        # On sauvegarde le path actuel, s'il existe. Au cas où l'utilisateur annule son choix.
        before = ""
        if self.filepath:
            before = self.filepath

        # On récupère le nouveau répertoire.
        self.filepath = filedialog.askdirectory(mustexist=True)
        if self.filepath:
            # Et la liste des automates ayant l'extension ".txt"
            self.fichiers = retourne_liste_des_fichiers(dir_path=self.filepath, extension='.txt',
                                                        remove_text=self.cfg.nom_groupe)
        elif before:
            # Si l'utilisateur n'a pas choisi de nouveau répertoire, et qu'il y en avait un existant, on revient dessus.
            self.fichiers = retourne_liste_des_fichiers(dir_path=before, extension='.txt',
                                                        remove_text=self.cfg.nom_groupe)
            self.filepath = before
        if self.fichiers:
            # Il y a des fichiers dans le répertoire, on initialise la complétion automatique.
            self.menu_selection.set_completion_list(list(self.fichiers.keys()))
            self.menu_filter.set_completion_list()
            self.menu_filter.clear_text()
            if not before:
                self.menu_selection.clear_selection()

    def affichegraphe(self):
        """
        Cette fonction permet d'afficher un graphe graphviz de l'automate actuel.
        """

        if self.graphe.check:
            if self.menu_selection.get() != "":
                self.graphe.automate_to_graph(self.automate_courant, visualiser=True)
        else:
            self.ConsoleTexte.add_message("Impossible d'initialiser Graphiz sur cet ordinateur")

    def reindexer_automate(self):
        """
        Gestion de la réindexation par l'interface.
        """

        if self.menu_selection.get() != "":
            self.automate_courant.reindexer()
            self.redessine_tableau()

    def entry_validation(self):
        """
        Validation de la boite de complétion de l'interface pour chercher rapidement dans la Combobox des automates.
        """

        if self.menu_filter.get() in self.menu_filter._completion_list:
            self.menu_filter.combo.set(self.menu_filter.get())
            self.menu_filter.combo.event_generate("<<ComboboxSelected>>")

    def verifOptionExecution(self):
        """
        Cette fonction gère les choix des transformations à appliquer à l'automate en cours.
        """

        # S'il n'y a pas d'automate à gérer, on sort
        if not self.automate_courant:
            return

        if self.option_choisie.get() != "":
            # Affiche un message informant de l'option choisi
            option_choisie = self.option_choisie.get()
            self.ConsoleTexte.add_message(f"Option choisie : {option_choisie}")




if __name__ == '__main__':
    appAutomate = AppAutomate()
    appAutomate.title("Gestion Automates - EFREI 2022")

    appAutomate.mainloop()
