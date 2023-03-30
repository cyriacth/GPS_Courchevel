import tkinter as tk
from tkinter.filedialog import askopenfilename 
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
from math import atan2, cos, sin, sqrt

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
    nombre_noeuds = 1
    def __init__(self, x, y, name:str):
        Noeud.nombre_noeuds += 1
        self.x = x
        self.y = y
        self.name = name
        self.sorties = []
        self.entrees = []
    
    def add_sortie(self, piste:"Piste"):
        self.sorties.append(piste)

    def add_entree(self, piste:"Piste"):
        self.entrees.append(piste)
    
    def show(self, canvas:tk.Canvas):
        self.canvas_id = []
        self.canvas_id.append(canvas.create_oval(self.x-7, self.y-7, self.x+7, self.y+7, fill="#ff00ff", activefill="yellow"))
        self.canvas_id.append(canvas.create_text(self.x, self.y-15, text=self.name, font=("Arial", 10)))
    
    def __str__(self) -> str:
        output = "\n#<"+self.name + ">#\nSorties :\n"
        for piste in self.sorties:
            output += piste.__str__()
        output += "\nEntrées :\n"
        for piste in self.entrees:
            output += piste.__str__()
        return output


class Piste():
    nombre_pistes = 0
    def __init__(self, noeud_depart:Noeud, couleur:str):
        Piste.nombre_pistes += 1
        self.noeud_depart = noeud_depart
        self.couleur = couleur
        self.noeud_fin = None
        self.piste = [(self.noeud_depart.x, self.noeud_depart.y)]
        self.canvas_id = []
        self.longueur = 0
    
    def add_chemin(self, xy:tuple, canvas:tk.Canvas):
        self.piste.append(xy)
        self.canvas_id.append(draw_arrow(canvas, self.piste[-2][0], self.piste[-2][1], self.piste[-1][0], self.piste[-1][1], self.couleur))
        self.longueur += int(sqrt((self.piste[-1][0] - self.piste[-2][0]) ** 2 + (self.piste[-1][1] - self.piste[-2][1]) ** 2))
    
    def set_noeud_fin(self, noeud_fin:Noeud, canvas:tk.Canvas):
        self.noeud_fin = noeud_fin
        self.piste.append((self.noeud_fin.x, self.noeud_fin.y))
        self.canvas_id.append(draw_arrow(canvas, self.piste[-2][0], self.piste[-2][1], self.piste[-1][0], self.piste[-1][1], self.couleur))
        self.longueur += int(sqrt((self.piste[-1][0] - self.piste[-2][0]) ** 2 + (self.piste[-1][1] - self.piste[-2][1]) ** 2))
        self.name = askstring(f"Piste n°{Piste.nombre_pistes}", "Choisir un nom")
        self.noeud_depart.add_sortie(self)
        self.noeud_fin.add_entree(self)
    
    def __str__(self) -> str:
        if self.couleur != "yellow":
            return f"'{self.noeud_depart.name}' vers '{self.noeud_fin.name}' < nom_piste : {self.name}, difficulté : {self.couleur}, longueur : {self.longueur} >\n"
        else:
            return f"'{self.noeud_depart.name}' vers '{self.noeud_fin.name}' via remontée {self.name} de longueur {self.longueur}\n"


class App():
    def __init__(self, root: tk.Tk):
        self.noeuds = []
        self.pistes = []
        self.diff = "green" # attribu automatique de la difficulté de la piste (en cours)
        self.latest_action = None # utile dans le câdre de la fonction undo (en cours)
        self.mode = "noeud" # mode d'édition par défaut

        self.root = root
        self.root.geometry("1500x1080")
        self.root.title("Createur de graph")
        self.image_path = askopenfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self.root, width=1400, height=1080, bg="black", scrollregion=(0, 0, self.image.width, self.image.height))
        self.canvas.grid(row=0, rowspan=4, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        # Ajouter des barres de défilement
        self.x_scrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview, width= 40)
        self.x_scrollbar.grid(row=5, column=0, sticky=tk.E+tk.W)
        self.y_scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview, width= 40)
        self.y_scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.canvas.config(xscrollcommand=self.x_scrollbar.set, yscrollcommand=self.y_scrollbar.set)
        
        # Ajouter des boutons

        self.button_undo = tk.Button(self.root, text="Undo", command=self.undo)
        self.button_undo.grid(row=0, column= 2)
        self.button_undo = tk.Button(self.root, text="Data", command=self.data)
        self.button_undo.grid(row=1, column= 2)

        # Ajouter l'image au canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Configurer le système de grille
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Binding de différentes actions utilisateur
        self.canvas.bind("<Button-1>", self.left_clic)
        self.root.bind("<d>", self.set_diff)
        self.canvas.bind("<Motion>", self.canvas_cursor)
    
    def canvas_cursor(self, event):
        self.root.config(cursor="crosshair")
    
    def left_clic(self, event):
        """left_clic a différent comportement selon la valeur que prend self.mode"""
        cursor = event.x + self.image.width*self.x_scrollbar.get()[0], event.y + self.image.height*self.y_scrollbar.get()[0]
        if self.mode == "noeud":
            if (noeud:=self.overlapping(cursor,"left_clic")) != None:
                # Mode piste !
                print(f"Mode de selection en cours de developpement <{noeud.name}>")
                self.canvas.itemconfigure(noeud.canvas_id[0], fill="orange")
                self.mode = "piste"
                self.pistes.append(Piste(noeud, self.diff))
            else: 
                # Création de noeuds !
                noms = [noeud.name for noeud in self.noeuds]
                nom_noeud = ""
                while nom_noeud in noms or nom_noeud == "":
                    nom_noeud = askstring(f"Noeud nommé n°{Noeud.nombre_noeuds}", "Saisir nom")
                if nom_noeud != None:
                    self.noeuds.append(Noeud(cursor[0], cursor[1], nom_noeud))
                    self.noeuds[-1].show(self.canvas)
                    self.latest_action = "left_clic"
        elif self.mode == "piste":
            if (noeud:=self.overlapping(cursor, "left_clic")) == None or noeud == self.pistes[-1].noeud_depart:
                self.pistes[-1].add_chemin(cursor, self.canvas)
            else:
                self.pistes[-1].set_noeud_fin(noeud, self.canvas)
                self.canvas.itemconfigure(self.pistes[-1].noeud_depart.canvas_id[0], fill="#ff00ff")
                self.mode = "noeud"
            
                

    def overlapping(self, xy:tuple, context:str):
        """Regarde si le curseur"""
        if context == "left_clic": # cas ou xy correspond au coordonnées du curseur utilisateur
            for noeud in self.noeuds:
                if 0 <= abs(noeud.x-xy[0]) <= 15 and 0 <= abs(noeud.y-xy[1]) <= 15:
                    return noeud
        return None
    
    def set_diff(self, _=None):
        """Permet de définir la difficulté des pistes créées"""
        self.diff = askstring("Choisir difficulté","green/blue/red/black/yellow")
    
    def undo(self):
        """Fonction de retour arrière (à approfondir)"""
        if self.mode == "noeud":
            if self.latest_action == "left_clic":
                for canvas_id in self.noeuds.pop().canvas_id:
                    self.canvas.delete(canvas_id)
                Noeud.nombre_noeuds -= 1
                if len(self.noeuds) == 0:
                    self.latest_action = None
    
    def data(self):
        """Affiche la data produite dans le terminal."""
        for noeud in self.noeuds:
            print("#"*30)
            print(noeud)
        print("#"*30)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
