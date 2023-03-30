import tkinter as tk
from tkinter.filedialog import *
from PIL import Image, ImageTk

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class App:

    def __init__(self, master):
        self.master = master
        master.title("Placer des points sur un canvas")
        master.geometry("1500x1500")

        self.frame = tk.Frame(master)
        self.frame.pack(expand=True, fill="both")

        self.canvas = tk.Canvas(self.frame, bg="white", highlightthickness=0)
        self.canvas.pack(side="left", expand=True, fill="both")

        self.scrollbar_v = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.scrollbar_v.pack(side="right", fill="y")

        self.scrollbar_h = tk.Scrollbar(master, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_h.pack(side="bottom", fill="x")

        self.canvas.config(xscrollcommand=self.scrollbar_h.set, yscrollcommand=self.scrollbar_v.set)

        self.points = []
        self.lines = []
        self.last_point = None
        self.selected_point = None
        self.image = None

        self.canvas.bind("<Button-1>", self.place_or_select_point)

        self.undo_button = tk.Button(master, text="Retour arrière", command=self.undo)
        self.undo_button.pack(side="bottom")

        self.image_button = tk.Button(master, text="Ajouter une image", command=self.add_image)
        self.image_button.pack(side="bottom")

        self.canvas.bind("<Configure>", self.on_canvas_resize)

    def on_canvas_resize(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def place_or_select_point(self, event):
        x, y = event.x, event.y
        if self.selected_point is None:
            # Place a new point
            self.points.append(Point(x, y))
            self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")
            if self.last_point is not None:
                # Draw a line to the new point
                self.lines.append(self.canvas.create_line(self.last_point.x, self.last_point.y, x, y, fill="black"))
            self.last_point = Point(x, y)
        else:
            # Add a line to the selected point
            selected_x, selected_y = self.selected_point.x, self.selected_point.y
            self.lines.append(self.canvas.create_line(selected_x, selected_y, x, y, fill="black"))
            self.selected_point = None

    def select_point(self, event):
        x, y = event.x, event.y
        for point in self.points:
            if abs(x - point.x) <= 2 and abs(y - point.y) <= 2:
                self.selected_point = point
                break

    def undo(self):
        if len(self.points) > 0:
            # Delete the last point and line
            self.canvas.delete(self.lines.pop())
            self.points.pop()
            if len(self.points) == 0:
                self.last_point = None
            else:
                self.last_point = self.points[-1]
    
            # Redraw all remaining points and lines
        self.canvas.delete("all")
        if self.image is not None:
            self.canvas.create_image(0, 0, image=self.image, anchor="nw")
        for i, point in enumerate(self.points):
            self.canvas.create_oval(point.x-2, point.y-2, point.x+2, point.y+2, fill="black")
            if i > 0:
                self.canvas.create_line(self.points[i-1].x, self.points[i-1].y, point.x, point.y, fill="black")
        self.selected_point = None

    def add_image(self):
        image_file = askopenfilename(title="Ouvrir une image", filetypes=[("JPEG files", "*.jpg"), ("all files", "*.*")])
        if image_file:
            self.image = Image.open(image_file)
            self.canvas.config(width=self.image.width, height=self.image.height)
            self.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.image, anchor="nw")

    def bind_select_point(self):
        self.canvas.bind("<Button-1>", self.select_point)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    select_button = tk.Button(root, text="Sélectionner un point", command=app.bind_select_point)
    select_button.pack(side="bottom")
    root.mainloop()
