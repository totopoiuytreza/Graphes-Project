import os
from graphes import Graphes
def get_all_files_in_dir(dir_path: str) -> list:
    """
    Récupère tous les fichiers dans un répertoire sans le repertoire, et les renvoie sous forme de liste.
    :param dir_path: Le chemin vers le répertoire
    :return: Une liste de fichiers
    """
    return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

def create_file_with_name(file_path: str):
    """
    Crée un fichier vide
    :param file_path: Le chemin vers le fichier
    """
    with open(os.path.join("execution_trace" + "/" + file_path), "w") as file:
        pass

def write_in_file(file_path: str, content: str):
    """
    Ecrit dans un fichier
    :param file_path: Le chemin vers le fichier
    :param content: Le contenu à écrire dans le fichier
    """
    with open("execution_trace" + "/" + file_path, "w") as file:
        file.write(content)

def get_content(file_path: str):
    """
    Rend le contenu du ficher en appliquant les fonctions du graphes
    """
    content = ""
    graphe = Graphes(file_path)
    graphe.checkCircuit()
    graphe.checkNegativeDuration()

    if graphe.dontHaveCircuit and graphe.dontHaveNegativeDuration:
        content += "Ce graphe n'a pas de circuit et n'a pas de durée négative\n\n"
        graphe.setRang()
        graphe.setdateASAP()
        graphe.setdateALAP()
        graphe.setMargeTotale()
        graphe.setMargeLibre()
        critical_path = graphe.getCriticalPath()
        content += graphe.getMatrix_withAllData().__str__() + "\n"

        content += "Le chemin critique est : " + critical_path.__str__()

    else:
        if not graphe.dontHaveCircuit:
            content += "Ce graphe a un circuit\n"
        if not graphe.dontHaveNegativeDuration:
            content += "Ce graphe a une durée négative\n"

    return content



def execution_trace():


    graphe_files = get_all_files_in_dir("graphes")
    exectution_files = get_all_files_in_dir("execution_trace")
    for graphe_file in graphe_files:
        if graphe_file not in exectution_files:
            create_file_with_name(graphe_file)
            write_in_file(graphe_file, get_content(graphe_file))

if __name__ == '__main__':
    execution_trace()

