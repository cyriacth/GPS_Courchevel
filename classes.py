class Node():
    def __init__(self, nom:str, liens:list[tuple[str,list[int]]]):
        self.nom = nom
        self.liens = liens
    
    def get_liens(self):
        return self.liens
    
    def get_nom(self):
        return self.nom
    
    def get_perms(self, noeud:"Node"):
        name_noeud = noeud.get_nom()
        for (name, perms) in self.liens:
            if name == name_noeud:
                return perms
        return [0]
    
    def __str__(self):
        return f' Noeud "{self.nom}" : {self.liens}'


class Graph():
    def __init__(self, noeuds:list[Node]):
        self.nodes = noeuds
        self.matrice = []
        self.id = {}
        for i in range(len(noeuds)):
            self.id[noeuds[i].get_nom()] = i
            self.matrice.append([])
            for j in range(len(noeuds)):
                self.matrice[i].append(noeuds[i].get_perms(noeuds[j]))
    
    def __get_id(self, name:str):
        return self.id[name]
    
    def __get_name(self, id:int):
        for (name, _id) in self.id.items():
            if id == _id:
                return name
        raise ValueError
    
    def __str__(self):
        output = "\nContenu du Graph :\n"
        for node in self.nodes:
            output += node.__str__()+"\n"
        return output + "\nRAPPEL\n1 = piste verte\n2 = piste bleue\n3 = piste rouge\n4 = piste noire\n5 = remontée mecanique\n"
    
    def gps(self, depart, arrivée):
        pass


###########################
### Perms explanation : ###
# 0 = rien
# 1 = piste verte
# 2 = piste bleue
# 3 = piste rouge
# 4 = piste noire
# 5 = remontée mecanique
###########################

n1 = Node("visage", [("cou",[1,3]),("oreille",[5])])
n2 = Node("cou", [("visage",[5])])
n3 = Node("oreille", [("visage",[1]), ("cou",[4])])
graph = Graph([n1, n2, n3])
print(graph)
