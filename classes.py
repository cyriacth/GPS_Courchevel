class Piste():
    def __init__(self, id, distance, difficulte, temps, debut, fin):
        self.id = id
        self.distance = distance
        self.difficulte = difficulte
        self.temps = temps
        self.debut = debut
        self.fin = fin


class Intersection():
    def __init__(self, id):
        self.id = id
        self.pistes = {}

    def ajouter_piste(self, piste:Piste):
        self.pistes[piste.id] = piste


class Graph():
    def __init__(self):
        self.intersections = {}

    def ajouter_intersection(self, intersection:Intersection):
        self.intersections[intersection.id] = intersection

    def ajouter_piste(self, id, distance, difficulte, debut_id, fin_id):
        debut = self.intersections[debut_id]
        fin = self.intersections[fin_id]
        piste = Piste(id, distance, difficulte, debut, fin)
        debut.ajouter_piste(piste)
        fin.ajouter_piste(piste)

Courchevel = Graph()
