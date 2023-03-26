from classes import *
# utilisation de pickles pour le storage d'une liste de Nodes

liste_noeuds = []
while (node_input:=input("Nouveau noeud : ")) != "":
    liens = []
    while (liens_input:=input(f"{node_input} amène vers quel autre noeud ? ")) != "":
        arcs = []
        while (arcs_input:=input(f"Chemin pour aller de {node_input} à {liens_input} : ")) != "":
            difficulté = int(input(f"Difficulté de {arcs_input} : "))
            arcs.append((difficulté, arcs_input))
        liens.append((liens_input,arcs))
    liste_noeuds.append(Node(node_input, liens))

for node in liste_noeuds:
    print(node)