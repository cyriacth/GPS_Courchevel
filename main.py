import tkinter as tk
#from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
from math import atan2, cos, sin, sqrt
import json


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
        self.sorties = []
        self.entrees = []
    
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
    def __init__(self, noeud_depart:Noeud, couleur:str):
        self.noeud_depart = noeud_depart
        self.couleur = couleur
        self.noeud_fin = None
        self.coords = [(self.noeud_depart.x, self.noeud_depart.y)]
        self.canvas_id = []
        self.longueur = 0
        self.name = None
    

    def show(self, canvas:tk.Canvas):
        self.canvas_id = []
        for i in range(1, len(self.coords)):
            x1, y1 = self.coords[i-1]
            x2, y2 = self.coords[i]
            self.canvas_id.append(draw_arrow(canvas, x1, y1, x2, y2, self.couleur))

    
    def __str__(self) -> str:
        if self.couleur != "yellow":
            return f"'{self.noeud_depart.name}' vers '{self.noeud_fin.name}' < nom_piste : {self.name}, difficulté : {self.couleur}, longueur : {self.longueur} >\n"
        else:
            return f"'{self.noeud_depart.name}' vers '{self.noeud_fin.name}' via remontée {self.name} de longueur {self.longueur}\n"


class App():
    def __init__(self, root: tk.Tk):
        self.noeuds = []
        self.pistes = []
        self.mode = 1 # 1 = gps mode, 2 = other thing

        self.root = root
        self.root.geometry("1500x1080")
        self.root.title("GPS - Station de Courchevel - by Aymeric & Cyriac")
        self.image = Image.open("./data/plan-pistes.jpg")
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self.root, width=1400, height=1080, bg="black", scrollregion=(0, 0, self.image.width, self.image.height))
        self.canvas.grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        menu_bar.add_command(label="Aide", command=self.button_help)
        menu_bar.add_command(label="Readme", command=self.button_readme)

        # Ajouter des barres de défilement
        self.x_scrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview, width= 40)
        self.x_scrollbar.grid(row=1, column=0, columnspan=2, sticky=tk.E+tk.W)
        self.y_scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview, width= 40)
        self.y_scrollbar.grid(row=0, rowspan=1, column=2, sticky=tk.N+tk.S)
        self.canvas.config(xscrollcommand=self.x_scrollbar.set, yscrollcommand=self.y_scrollbar.set)

        # Ajouter des checkbox
        self.state_check_box_pistes = tk.BooleanVar()
        self.check_box_pistes = tk.Checkbutton(self.root, text="Pistes", variable=self.state_check_box_pistes, onvalue=1, offvalue=0, command= self.refresh)
        self.check_box_pistes.grid(row=2, column=0, sticky=tk.E)
        self.state_check_box_noeuds = tk.BooleanVar()
        self.check_box_noeuds = tk.Checkbutton(self.root, text="Noeuds", variable=self.state_check_box_noeuds, onvalue=1, offvalue=0, command= self.refresh)
        self.check_box_noeuds.grid(row=2, column=1, sticky=tk.W)

        # Configurer le système de grille
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Binding de différentes actions utilisateur
        self.canvas.bind("<Button-1>", self.left_clic)
        self.canvas.bind("<Motion>", self.canvas_cursor)
    

    def refresh(self):
        p, n = self.state_check_box_pistes.get(), self.state_check_box_noeuds.get()
        print("pistes"*p+"noeuds"*n)


    def canvas_cursor(self, event):
        self.root.config(cursor="crosshair")

    
    def button_help(self):
        pass


    def button_readme(self):
        pass
    

    def left_clic(self, event):
        """left_clic a différent comportement selon la valeur que prend self.mode"""
        cursor = event.x + self.image.width*self.x_scrollbar.get()[0], event.y + self.image.height*self.y_scrollbar.get()[0]
        noeud = self.overlapping(cursor)
        if self.mode == 1:
            pass


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
