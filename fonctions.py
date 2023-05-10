import json

def dijkstra(graph, start, end, niveau):
    # Initialisation des structures de données
    all_temps = {node['name']: float('inf') for node in graph['noeuds']}
    all_temps[start] = 0
    visited = set()
    predecessors = {}

    # Boucle principale de l'algorithme
    while len(visited) != len(graph['noeuds']):
        # Recherche du noeud non visité avec le plus petite temps
        min_temps = float('inf')
        min_node = None
        for node in graph['noeuds']:
            if node['name'] not in visited and all_temps[node['name']] < min_temps:
                min_temps = all_temps[node['name']]
                min_node = node['name']
        if min_node is None:
            break
        visited.add(min_node)

        # Mise à jour de all_temps pour chaque voisin du noeud courant
        for edge in get_neighbors(graph, min_node):
            neighbor = edge['noeud_fin']
            poids = edge['temps']
            couleur = edge['couleur']

            if couleur in ["green", "blue", "red", "black"]:
                if niveau == "débutant":
                    if couleur == "green":
                        temps = min_temps + poids
                    elif couleur == "blue":
                        temps = min_temps + poids*1.5
                    elif couleur == "red":
                        temps = min_temps + poids*2
                    elif couleur == "black":
                        temps = min_temps + poids*4
                      
                elif niveau == "moyen":
                    if couleur == "green":
                        temps = min_temps + poids
                    elif couleur == "blue":
                        temps = min_temps + poids
                    elif couleur == "red":
                        temps = min_temps + poids*1.5
                    elif couleur == "black":
                        temps = min_temps + poids*2
                    
                elif niveau == "avance":
                    temps = min_temps + poids
            else:
                temps = min_temps + poids

            if temps < all_temps[neighbor]:
                all_temps[neighbor] = temps
                predecessors[neighbor] = min_node

    # Construction du chemin le plus court en remontant les prédecesseurs
    path = []
    node = end
    while node != start:
        path.insert(0, node)
        node = predecessors[node]
    path.insert(0, start)

    return path, all_temps[end]

def get_neighbors(graph, node):
    # Retourne la liste des voisins d'un noeud dans le graphe
    neighbors = []
    for edge in graph['pistes']:
        if edge['noeud_depart'] == node:
            neighbors.append(edge)
    return neighbors

# Lecture du fichier JSON représentant le graphe
with open('courchevelwithspeed.json') as f:
    graph = json.load(f)

# Exécution de l'algorithme de Dijkstra pour trouver le plus court chemin entre deux points
path, temps = dijkstra(graph, 'bas VERDONS', 'n90', 'avance')

# Affichage du résultat
print('Le plus court chemin est :', ' -> '.join(path)) #path est une liste
print('Le temps total est :', temps, "secondes") #temps correspond au temps total entre les deux noeuds