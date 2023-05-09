#notes : if novice[difficulté] < rouge il faut alors multiplié la longueur des pistes par exemple
import json
import heapq

def dijkstra(graphe, start, end, couleur):
    # Initialisation des structures de données
    distances = {node['name']: float('inf') for node in graphe['noeuds']}
    distances[start] = 0
    heap = [(0, start)]
    visited = set()
    predecessors = {}

    # Boucle principale de l'algorithme
    while heap:
        (current_distance, current_node) = heapq.heappop(heap)
        if current_node == end:
            # Si on a atteint le noeud final, on sort de la boucle
            break
        if current_node in visited:
            continue
        visited.add(current_node)

        # Mise à jour des distances pour chaque voisin du noeud courant
        for edge in get_neighbors(graphe, current_node, couleur):
            neighbor = edge['noeud_fin']
            distance = current_distance + edge['longueur']
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(heap, (distance, neighbor))

    # Construction du chemin le plus court en remontant les prédecesseurs
    path = []
    node = end
    while node != start:
        path.insert(0, node)
        node = predecessors[node]
    path.insert(0, start)

    return path, distances[end]

def get_neighbors(graphe, node, couleur):
    # Création d'un classement de couleur
    color_rank = {'yellow': 0, 'green': 1, 'blue': 2, 'red': 3, 'black': 4}

    # Retourne la liste des voisins d'un noeud dans le graphe
    neighbors = []
    for edge in graphe['pistes']:
        if edge['noeud_depart'] == node and color_rank[edge['couleur']] <= color_rank[couleur]:
            neighbors.append(edge)
    return neighbors

# Lecture du fichier JSON représentant le graphe
with open('data\courchevel.json') as f:
    graphe = json.load(f)

# Exécution de l'algorithme de Dijkstra pour trouver le plus court chemin entre A et E
path, distance = dijkstra(graphe, 'n30', 'bas Belv\u00e9d\u00e8re', 'green')

# Affichage du résultat
print('Le plus court chemin est :', ' -> '.join(path))
print('La distance totale est :', distance)
