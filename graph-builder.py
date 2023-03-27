import pickle
from os import remove
# utilisation de pickles pour le storage d'une liste de Nodes
path = "./data-test.pickle"

liste_noeuds = []
while (node_input:=input("\nNouveau noeud : ")) != "":
    liens = []
    while (liens_input:=input(f"{node_input} amène vers quel autre noeud ?\n")) != "":
        arcs = []
        while (arcs_input:=input(f'\nChemin pour aller de "{node_input}" à "{liens_input}" : ')) != "":
            difficulté = input(f"Nature de {arcs_input} : ")
            arcs.append((difficulté, arcs_input))
        liens.append((liens_input,arcs))
    liste_noeuds.append({"nom":node_input, "liens":liens})

for node in liste_noeuds:
    print(node)

if (push:=input("Ajouter les donnée saisie à la database existante ? (yes/any)")) == "yes":
    with open(path, "rb") as f:
        old_nodes = pickle.load(f)
    remove(path)
    old_nodes += liste_noeuds
    with open(path, "wb") as f:
        pickle.dump(old_nodes, f)
elif push == "create":
    with open(path, "wb") as f:
        pickle.dump(liste_noeuds, f)
print("end of program")