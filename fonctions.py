import json

def dijkstra(graph, start, end, niveau):
    # Initialisation des structures de données
    distances = {node['name']: float('inf') for node in graph['noeuds']}
    distances[start] = 0
    visited = set()
    predecessors = {}

    # Boucle principale de l'algorithme
    while len(visited) != len(graph['noeuds']):
        # Recherche du noeud non visité avec la plus petite distance
        min_distance = float('inf')
        min_node = None
        for node in graph['noeuds']:
            if node['name'] not in visited and distances[node['name']] < min_distance:
                min_distance = distances[node['name']]
                min_node = node['name']
        if min_node is None:
            break
        visited.add(min_node)

        # Mise à jour des distances pour chaque voisin du noeud courant
        for edge in get_neighbors(graph, min_node):
            neighbor = edge['noeud_fin']
            poids = edge['longueur']
            couleur = edge['couleur']

            if niveau == "débutant":
                if couleur == "blue":
                    distance = min_distance + poids*1.5
                elif couleur == "red":
                    distance = min_distance + poids*2
                elif couleur == "black":
                    distance = min_distance + poids*4
                else:
                    distance = min_distance + poids
                
            elif niveau == "moyen":
                if couleur == "red":
                    distance = min_distance + poids*1.5
                elif couleur == "black":
                    distance = min_distance + poids*2
                else:
                    distance = min_distance + poids

            else:
                distance = min_distance + poids

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = min_node

    # Construction du chemin le plus court en remontant les prédecesseurs
    path = []
    node = end
    while node != start:
        path.insert(0, node)
        node = predecessors[node]
    path.insert(0, start)

    return path, distances[end]

def get_neighbors(graph, node):
    # Retourne la liste des voisins d'un noeud dans le graphe
    neighbors = []
    for edge in graph['pistes']:
        if edge['noeud_depart'] == node:
            neighbors.append(edge)
    return neighbors

# Lecture du fichier JSON représentant le graphe
with open('data\courchevel.json') as f:
    graph = json.load(f)

# Exécution de l'algorithme de Dijkstra pour trouver le plus court chemin entre A et E
path, distance = dijkstra(graph, 'bas GRANGETTES', 'COL DE CHANROSSA', 'débutant')

# Affichage du résultat
print('Le plus court chemin est :', ' -> '.join(path))
print('La distance totale est :', distance)