class Piste():
    def __init__(self, id:str, distance:int, difficulte:str, temps:int, debut:"Intersection", fin:"Intersection"):
        self.id = id
        self.distance = distance
        self.difficulte = difficulte
        self.temps = temps
        self.debut = debut
        self.fin = fin
    
    def __str__(self) -> str:
        return f'Piste [id : "{self.id}" # distance : {self.distance}m # diff : "{self.difficulte}" # temps : {self.temps}min # debut : "{self.debut.id}" # fin : "{self.fin.id}"]'


class Intersection():
    def __init__(self, id:str):
        self.id = id
        self.entree = {}
        self.sortie = {}

    def ajouter_entree(self, piste:Piste):
        self.entree[piste.id] = piste
    
    def ajouter_sortie(self, piste:Piste):
        self.sortie[piste.id] = piste
    
    def __str__(self) -> str:
        output = self.id + "\nEntrées :\n"
        for (_, piste) in self.entree.items():
            output += piste.__str__() + "\n"
        output += "\nSorties :\n"
        for (_, piste) in self.sortie.items():
            output += piste.__str__() + "\n"
        return output


class Graph():
    def __init__(self):
        self.intersections = {}

    def ajouter_intersection(self, intersection:Intersection):
        self.intersections[intersection.id] = intersection

    def ajouter_piste(self, id, distance, difficulte, temps, debut_id, fin_id):
        debut = self.intersections[debut_id]
        fin = self.intersections[fin_id]
        piste = Piste(id, distance, difficulte, temps, debut, fin)
        debut.ajouter_sortie(piste)
        fin.ajouter_entree(piste)
    
    def print_intersection(self, id):
        print(self.intersections[id])

Courchevel = Graph()
Courchevel.ajouter_intersection(Intersection("A"))
Courchevel.ajouter_intersection(Intersection("B"))
Courchevel.ajouter_piste("rockcool",200,"rouge", 6,"A","B")
Courchevel.print_intersection("A")