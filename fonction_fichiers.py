"""
Projet Théorie des graphes L3 EFREI
    - Yann SCARDIGLI
    - Pierre THAITE
    - Nathan RICARDO
    - Thomas SONG
    -

Gestion des fichiers dans le répertoire des graphes
"""
import os


def cpt_nbr_fichier(dir_path: str) -> int:
    """
    Cette fonction compte le nombre de fichiers graphes dans la base de données

    :param: dir_path: path vers le repertoire
    :return: Nombre de fichiers graphes dans la base de données (int)
    """
    count = 0

    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1

    return count


def retourne_liste_des_fichiers(dir_path: str, extension: str, remove_text: str | None = None) -> dict:
    """
    Cette fonction renvoie sous forme de dictionnaire tous les fichiers du path dir_path possédants
    l'extention passée en paramètre. On peut supprimer une partie du texte avec remove_texte (vide par défaut).
    Le format du dictionnaire est le suivant : {"nom court": "nom_complet"}

    :param: dir_path: path vers le répertoire
    :param: extension: L'extension de fichier à chercher
    :param: remove_text: Texte à supprimer de la liste affichée. Cela permet de masquer des parties du nom de fichier
    :return: Dictionnaire des noms des fichiers du répertoire automates.
    """

    proprietes = {}
    # On cherche tous les fichiers dans le path dir_path, possédant l'extension "extension"
    list_files_name = os.listdir(dir_path)
    files = [i for i in list_files_name if i.endswith(extension)]

    for file in files:
        # On ajoute les noms des fichiers, sans extension, comme clé du dictionnaire
        file_without_extension = os.path.splitext(file)[0]
        # Si une partie du texte doit être supprimé, notamment pour les groupes EFREI
        if remove_text:
            file_without_extension = file_without_extension.replace(remove_text, "")
        # Et on conserve le nom complet du fichier
        proprietes[file_without_extension] = file

    return proprietes
