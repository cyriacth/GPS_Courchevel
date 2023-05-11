import tkinter as tk
#from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
from math import atan2, cos, sin
import json


def dijkstra(graph, start, end, niveau):
    # Initialisation des structures de données
    all_temps = {node['name']: float('inf') for node in graph['noeuds']}
    all_temps[start] = 0
    visited = set()
    predecessors = {}
    edge_names = {}

    
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
                if niveau == "Débutant":
                    if couleur == "green":
                        temps = min_temps + poids
                    elif couleur == "blue":
                        temps = min_temps + poids*1.5
                    elif couleur == "red":
                        temps = min_temps + poids*2
                    elif couleur == "black":
                        temps = min_temps + poids*4
                      
                elif niveau == "Moyen":
                    if couleur == "green":
                        temps = min_temps + poids
                    elif couleur == "blue":
                        temps = min_temps + poids
                    elif couleur == "red":
                        temps = min_temps + poids*1.5
                    elif couleur == "black":
                        temps = min_temps + poids*2
                    
                elif niveau == "Avancé":
                    temps = min_temps + poids
            else:
                temps = min_temps + poids

            if temps < all_temps[neighbor]:
                all_temps[neighbor] = temps
                predecessors[neighbor] = min_node
                edge_names[(min_node, neighbor)] = edge['name']

    # Construction du chemin le plus court en remontant les prédecesseurs
    path = []
    edge_path = []
    node = end
    while node != start:
        path.insert(0, node)
        edge_path.insert(0, edge_names[(predecessors[node], node)])
        node = predecessors[node]
    path.insert(0, start)

    return path, all_temps[end], edge_path


def get_neighbors(graph, node):
    # Retourne la liste des voisins d'un noeud dans le graphe
    neighbors = []
    for edge in graph['pistes']:
        if edge['noeud_depart'] == node:
            neighbors.append(edge)
    return neighbors


def draw_arrow(canvas:tk.Canvas, x1, y1, x2, y2, couleur:str):
        # Dessiner une flèche isocèle entre les points (x1, y1) et (x2, y2)
        arrow_width = 5
        arrow_length = 10
        dx = x2 - x1
        dy = y2 - y1
        angle = atan2(dy, dx)
        x3 = x2 - arrow_length * cos(angle)
        y3 = y2 - arrow_length * sin(angle)
        x4 = x3 + arrow_width * sin(angle)
        y4 = y3 - arrow_width * cos(angle)
        x5 = x3 - arrow_width * sin(angle)
        y5 = y3 + arrow_width * cos(angle)
        id_line = canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=5, fill=couleur)
        id_poly = canvas.create_polygon(x2, y2, x4, y4, x5, y5, fill=couleur)
        return id_line, id_poly


class Noeud():
    def __init__(self, x, y, name:str):
        self.x = x
        self.y = y
        self.name = name
    
    def show(self, canvas:tk.Canvas, name:bool):
        self.canvas_id = []
        self.canvas_id.append(canvas.create_oval(self.x-7, self.y-7, self.x+7, self.y+7, fill="#ff00ff", activefill="yellow"))
        if name:
            self.canvas_id.append(canvas.create_text(self.x, self.y-15, text=self.name, font=("Arial", 10)))


class Piste():
    def __init__(self, name:str, couleur:str, coord, longueur):
        self.name = name
        if couleur not in ["green", "blue", "red", "black"]:
            self.couleur = "purple"
        else:
            self.couleur = couleur
        self.coords = coord
        self.longueur = longueur
        self.canvas_id = []
    

    def show(self, canvas:tk.Canvas):
        self.canvas_id = []
        for i in range(1, len(self.coords)):
            x1, y1 = self.coords[i-1]
            x2, y2 = self.coords[i]
            self.canvas_id.append(draw_arrow(canvas, x1, y1, x2, y2, self.couleur))



class App():
    def __init__(self, root: tk.Tk):

        with open("./data/courchevelwithspeed.json","r") as f:
            self.json = json.load(f)
        self.noeuds = [Noeud(n["x"], n["y"], n["name"]) for n in self.json["noeuds"]]
        self.pistes = [Piste(p["name"], p["couleur"], p["coords"], p["longueur"]) for p in self.json["pistes"]]
        self.noeud_depart = None

        # Gui
        self.root = root
        self.root.geometry("1500x1080")
        self.root.title("GPS - Station de Courchevel - by Aymeric & Cyriac")
        self.image = Image.open("./data/plan-pistes.jpg")
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self.root, width=1400, height=1080, bg="grey", scrollregion=(0, 0, self.image.width, self.image.height))
        self.canvas.grid(row=0, column=0, columnspan=5, sticky=tk.N+tk.S+tk.E+tk.W)
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        menu_bar.add_command(label="Github", command=self.button_github)

        # Ajouter des barres de défilement
        self.x_scrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview, width= 40)
        self.x_scrollbar.grid(row=1, column=0, columnspan=5, sticky=tk.E+tk.W)
        self.y_scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview, width= 40)
        self.y_scrollbar.grid(row=0, rowspan=1, column=5, sticky=tk.N+tk.S)
        self.canvas.config(xscrollcommand=self.x_scrollbar.set, yscrollcommand=self.y_scrollbar.set)

        # Ajouter des checkbox
        self.state_check_box_pistes = tk.BooleanVar()
        self.state_check_box_pistes.set(False)
        self.check_box_pistes = tk.Checkbutton(self.root, text="Pistes", variable=self.state_check_box_pistes, onvalue=1, offvalue=0, command= self.refresh)
        self.check_box_pistes.grid(row=2, column=1, sticky=tk.E)
        self.state_check_box_noeuds = tk.BooleanVar()
        self.state_check_box_noeuds.set(True)
        self.check_box_noeuds = tk.Checkbutton(self.root, text="Noeuds", variable=self.state_check_box_noeuds, onvalue=1, offvalue=0, command= self.refresh)
        self.check_box_noeuds.grid(row=2, column=2, sticky=tk.W)
        self.state_check_box_bg = tk.BooleanVar()
        self.state_check_box_bg.set(True)
        self.check_box_bg = tk.Checkbutton(self.root, text="Background", variable=self.state_check_box_bg, onvalue=1, offvalue=0, command= self.refresh)
        self.check_box_bg.grid(row=2, column=3, sticky=tk.W)
        self.niveaux = ["Débutant", "Moyen", "Avancé"]
        self.niveau = tk.StringVar()
        self.niveau.set(self.niveaux[0])
        self.option_menu_niveaux = tk.OptionMenu(self.root, self.niveau, *self.niveaux)
        self.option_menu_niveaux.grid(row=2, column=4, sticky=tk.W)

        # Un label affichant le temps de parcourt

        self.var_label_temps = tk.StringVar()
        self.var_label_temps.set("Temps de parcours approximatif ~ 0 minutes\nDistance approximative ~ 0.00 km\nPlus court chemin : XXX")
        self.label_temps = tk.Label(self.root, textvariable= self.var_label_temps)
        self.label_temps.grid(row=2, column=0, sticky=tk.W)

        # Configurer le système de grille
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Binding de différentes actions utilisateur
        self.canvas.bind("<Button-1>", self.left_clic)
        self.canvas.bind("<Motion>", self.canvas_cursor)
        self.refresh()
        

    def refresh(self):
        bg, p, n = self.state_check_box_bg.get() ,self.state_check_box_pistes.get(), self.state_check_box_noeuds.get()
        self.canvas.delete("all")
        name = True
        if bg:
            name = False
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        if p:
            for piste in self.pistes:
                piste.show(self.canvas)
        if n:
            for noeud in self.noeuds:
                noeud.show(self.canvas, name)


    def canvas_cursor(self, event):
        self.root.config(cursor="crosshair")


    def button_github(self):
        pass
    

    def left_clic(self, event):
        cursor = event.x + self.image.width*self.x_scrollbar.get()[0], event.y + self.image.height*self.y_scrollbar.get()[0]
        if (noeud_cliqué:=self.overlapping(cursor)) and not self.noeud_depart:
            self.state_check_box_pistes.set(False)
            self.state_check_box_noeuds.set(True)
            self.refresh()
            self.canvas.itemconfigure(noeud_cliqué.canvas_id[0], fill="orange")
            self.noeud_depart = noeud_cliqué
        elif noeud_cliqué and self.noeud_depart:
            self.state_check_box_pistes.set(False)
            self.state_check_box_noeuds.set(False)
            self.refresh()
            self.canvas.itemconfigure(noeud_cliqué.canvas_id[0], fill="orange")
            noeuds_str, temps, pistes_str = dijkstra(self.json, self.noeud_depart.name, noeud_cliqué.name, self.niveau.get()) #noeuds, temps, pistes
            longueur_totale = 0
            for string in pistes_str:
                for _piste in self.pistes:
                    if string == _piste.name:
                        _piste.show(self.canvas)
                        longueur_totale += _piste.longueur
            for string in noeuds_str:
                for _noeud in self.noeuds:
                    if string == _noeud.name:
                        _noeud.show(self.canvas, False)
            self.noeud_depart = None
            self.var_label_temps.set(f"Temps de parcours approximatif ~ {int(temps//60)} minutes\nDistance approximative ~ {round(longueur_totale/1000, 2)} km\nPlus court chemin : {'->'.join(pistes_str)}")


    def overlapping(self, xy:tuple)-> Noeud | None:
        """Renvoi un Noeud dont les coordonnées correspondent avec les coordonnées passés en arguments
        sinon None"""
        for noeud in self.noeuds:
            if 0 <= abs(noeud.x-xy[0]) <= 15 and 0 <= abs(noeud.y-xy[1]) <= 15:
                return noeud
        return None


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
