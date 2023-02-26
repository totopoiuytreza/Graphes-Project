"""
Projet Théorie des graphes L3 EFREI
    -
    -
    - Nathan RICARDO
    - Thomas SONG
    -

Cette classe de générer un graphique du graphe avec graphviz
"""

import os
import tempfile

from graphes import Graphes
from config import Configuration

class ToGraphviz:
    """
    Classe qui permet de convertir un graphe en graphique.
    L'installation de graphviz est nécessaire, mais elle n'est pas triviale en fonction des systèmes d'exploitations.
    La classe doit donc être vérifiée (check) afin de savoir si l'interface pourra gérer les images ou pas.
    """

    def __init__(self):
        self.check = False
        try:
            import graphviz
        except ModuleNotFoundError:
            return
        try:
            graphviz.version()
            self.check = True
        except graphviz.backend.execute.ExecutableNotFound:
            return

    def graphe_to_graph(self, graphes: Graphes, nom_fichier: str | None = None, visualiser: bool = True) -> str | None:
        """
        Cette fonction transforme le graphe passé en paramètre en image.

        :param graphes: Le graphe à dessiner
        :return: Le path vers le fichier PNG que l'on peut afficher ailleur. None si graphviz ne fonctionne pas.
        """

        # self.check sera True si l'installation de graphviz sur l'ordinateur est complète
        if self.check:
            import graphviz
        else:
            return None

        # On crée un graphe, avec une orientation horizontale (LR) et en essayant de ne pas trop mettre de liaisons les
        # unes sur les autres (overlap)
        gra = graphviz.Digraph(graph_attr={'rankdir': 'LR', "overlap": "false"})

        # On parcourt tous les états du graphe et on crée les nodes graphviz correspondants.
        for sommet in graphes.grapheDict:
            if sommet["marge"] == 0:
                gra.attr('node', color='red')
            else:
                gra.attr('node', color='black')
            nom_sommet = sommet["tache"]
            gra.attr('node', shape='circle')
            gra.node(nom_sommet, nom_sommet)

        # On parcourt tous les sommets du graphe pour créer les arcs
        for sommet in graphes.grapheDict:
            nom_sommet = sommet["tache"]
            for successeur in sommet["contraintes"]:
                for element in graphes.grapheDict:
                    if element["tache"] == successeur:
                        if element["marge"] == 0 and sommet["marge"] == 0:
                            gra.attr('edge', color='red')
                        else:
                            gra.attr('edge', color='black')
                        gra.edge(successeur, nom_sommet, label=str(element["duree"]))



        # On génère une image de type png
        file_ext = 'png'
        # Si le nom du fichier destination n'a pas été donné, on le génère aléatoirement
        if not nom_fichier:
            tmp = tempfile.NamedTemporaryFile()
            nom_fichier = tmp.name
            tmp.close()
        # On crée le nom du fichier graphviz
        temp_img = os.path.join(tempfile.gettempdir(), nom_fichier)
        # On génère le fichier graphviz grâce à sa source (dot file)
        my_graph = graphviz.Source(gra.source)
        # Et enfin, on crée l'image finale, l'image est affichée par le système si visualiser=True
        my_graph.render(temp_img, format=file_ext, view=visualiser)
        # Et on renvoie le path complet vers le fichier image
        return f"{temp_img}.{file_ext}"


if __name__ == '__main__':
    graph = ToGraphviz()
    if graph.check:
        print("Graphviz est installé")
        cfg = Configuration()
        graphe = Graphes("test6.txt")
        print(graph.graphe_to_graph(graphe, visualiser=True))