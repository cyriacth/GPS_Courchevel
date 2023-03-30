import tkinter as tk
from tkinter.filedialog import askopenfilename 
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk


class Noeud():
    nombre_noeuds = 1
    def __init__(self, x, y, name:str):
        Noeud.nombre_noeuds += 1
        self.x = x
        self.y = y
        self.name = name
        self.sorties = {}
        self.entrees = {}
    
    def show(self, canvas:tk.Canvas):
        self.canvas_id = []
        self.canvas_id.append(canvas.create_oval(self.x-7, self.y-7, self.x+7, self.y+7, fill="#ff00ff"))
        self.canvas_id.append(canvas.create_text(self.x, self.y-15, text=self.name, font=("Arial", 5)))

class Piste():
    nombre_pistes = 1
    def __init__(self, noeud_depart:str, noeud_fin:str, couleur:str):
        Piste.nombre_pistes += 1
        self.noeud_depart = noeud_depart
        self.noeud_fin = noeud_fin
        self.couleur = couleur
    
    def show(self, canvas:tk.Canvas):
        xy_xy = self.noeud_depart.x, self.noeud_depart.y, self.noeud_fin.x, self.noeud_fin.y
        canvas.create_line(xy_xy[0], xy_xy[1], xy_xy[2], xy_xy[3], fill=self.couleur, width= 6)


class App():
    def __init__(self, root: tk.Tk):
        self.noeuds = []
        self.pistes = []
        self.diff = "green" # attribu automatique de la difficulté de la piste (en cours)
        self.latest_action = None # utile dans le câdre de la fonction undo (en cours)

        self.root = root
        self.root.geometry("1500x1080")
        self.root.title("Createur de graph")
        self.image_path = askopenfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self.root, width=1400, height=1080, bg="black", scrollregion=(0, 0, self.image.width, self.image.height))
        self.canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        # Ajouter des barres de défilement
        self.x_scrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview, width= 40)
        self.x_scrollbar.grid(row=1, column=0, sticky=tk.E+tk.W)
        self.y_scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview, width= 40)
        self.y_scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.canvas.config(xscrollcommand=self.x_scrollbar.set, yscrollcommand=self.y_scrollbar.set)
        
        # Ajouter des boutons

        self.button_undo = tk.Button(self.root, text="Undo", command=self.undo)
        self.button_undo.grid(row=2, column= 0)

        # Ajouter l'image au canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Configurer le système de grille
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.canvas.bind("<Button-1>", self.left_clic)
        self.root.bind("<d>", self.set_diff)
        self.canvas.bind("<Motion>", self.canvas_cursor)
    
    def canvas_cursor(self, event):
        self.root.config(cursor="crosshair")
    
    def left_clic(self, event):
        """left clic sert a placer un noeud"""
        cursor = event.x + self.image.width*self.x_scrollbar.get()[0], event.y + self.image.height*self.y_scrollbar.get()[0]
        if (noeud:=self.overlapping(cursor,"left_clic")) != None:
            # Mode selection !
            print(f"Mode de selection en cours de developpement <{noeud.name}>")
            pass
        else: 
            # Mode création de noeuds !
            noms = [noeud.name for noeud in self.noeuds]
            nom_noeud = ""
            while nom_noeud in noms or nom_noeud == "":
                nom_noeud = askstring(f"Noeud nommé n°{Noeud.nombre_noeuds}", "Saisir nom")
            if nom_noeud == None:
                pass
            else:
                self.noeuds.append(Noeud(cursor[0], cursor[1], nom_noeud))
                self.noeuds[-1].show(self.canvas)
                self.latest_action = "left_clic"
    
    def overlapping(self, cursor:tuple, context:str):
        if context == "left_clic":
            for noeud in self.noeuds:
                if 0 <= abs(noeud.x-cursor[0]) <= 15 and 0 <= abs(noeud.y-cursor[1]) <= 15:
                    return noeud
        return None
    
    def set_diff(self, _=None):
        self.diff = askstring("Choisir difficulté","green/blue/red/black/yellow")
    
    def undo(self):
        """Fonction de retour arrière (à approfondir)"""
        if self.latest_action == "left_clic":
            for canvas_id in self.noeuds.pop().canvas_id:
                self.canvas.delete(canvas_id)
            Noeud.nombre_noeuds -= 1
            if len(self.noeuds) == 0:
                self.latest_action = None


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
