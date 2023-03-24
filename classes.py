class Node():
    def __init__(self, nom:str, liens:list[tuple[str,list[tuple[int,str]]]], pos_canvas:tuple[int,int]=(0,0)):
        """liens prend en argument une liste de tuples contenant le
        nom du noeuds d'arrivée en [0] puis en [1] il s'agit d'une
        liste de tuple permettant l'existance de plusieurs chemins
        entre deux noeuds ( difficultée : int, nom_piste : str ).
        xy sert pour l'affichage du noeud sur un canvas"""
        self.nom = nom
        self.liens = liens
        self.pos_canvas = pos_canvas
    
    def get_liens(self):
        return self.liens
    
    def get_nom(self):
        return self.nom
    
    def get_issues(self, noeud:"Node"):
        issues = []
        name_noeud = noeud.get_nom()
        for (name, issue) in self.liens:
            if name == name_noeud:
                issues.append(issue)
        return issues
    
    def __str__(self):
        return f' Noeud "{self.nom}" : {self.liens}'
    
    def get_pos_canvas(self):
        return self.pos_canvas


class Graph():
    def __init__(self, noeuds:list[Node]):
        self.nodes = noeuds
        self.matrice = []
        self.id = {}
        for i in range(len(noeuds)):
            self.id[noeuds[i].get_nom()] = i
            self.matrice.append([])
            for j in range(len(noeuds)):
                self.matrice[i].append(noeuds[i].get_issues(noeuds[j]))
    
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
    
    def gps(self, depart:str, arrivée:str):
        id_depart = self.__get_id(depart)
        id_arrivée = self.__get_id(arrivée)
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

n1 = Node("visage", [("cou",[(1,"doux"),(3,"galère")]),("oreille",[(5,"remontée du pic")])])
n2 = Node("cou", [("visage",[(5,"tire fesses")])])
n3 = Node("oreille", [("visage",[(1,"tartiflette")]), ("cou",[(4,"le chemin du fou")])])
graph = Graph([n1, n2, n3])
print(graph)
