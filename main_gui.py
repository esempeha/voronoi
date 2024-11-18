import itertools
import math
import random
import tkinter as tk
from tkinter import filedialog
from point import Point
from voronoi_diagram import VoronoiDiagram

class MainGUI:
    def __init__(self, master: tk.Tk, diagram: VoronoiDiagram):
        self.master = master
        self.diagram = diagram
        self.canvas_size = diagram.get_size()

        # Set judul utama
        self.master.title("Voronoi Diagram Visualizer")

        # Buat frame utama
        self.main_frame = tk.Frame(master, bg="lightblue", padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Tambahkan judul
        self.title_label = tk.Label(self.main_frame, text="Voronoi Diagram Visualizer", font=("Helvetica", 16, "bold"), bg="lightblue")
        self.title_label.pack(pady=5)

        # Canvas untuk menggambar diagram
        self.canvas = tk.Canvas(self.main_frame, width=self.canvas_size, height=self.canvas_size, bg="white", relief=tk.SUNKEN, bd=2)
        self.canvas.pack(pady=10)

        # Frame untuk tombol
        self.button_frame = tk.Frame(self.main_frame, bg="lightblue")
        self.button_frame.pack(pady=5)

        # Tombol Clear
        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_canvas, bg="red", fg="white", font=("Helvetica", 12, "bold"))
        self.clear_button.pack(side=tk.LEFT, padx=10)

        # Tombol Load File
        self.load_button = tk.Button(self.button_frame, text="Load File", command=self.load_points_from_file, bg="green", fg="white", font=("Helvetica", 12, "bold"))
        self.load_button.pack(side=tk.LEFT, padx=10)

        # Tombol Generate Random Points
        self.random_button = tk.Button(self.button_frame, text="Generate Random Points", command=self.generate_random_points, bg="orange", fg="black", font=("Helvetica", 12, "bold"))
        self.random_button.pack(side=tk.LEFT, padx=10)

        # Input manual titik
        self.manual_input = tk.Entry(self.button_frame, font=("Helvetica", 12), width=15)
        self.manual_input.pack(side=tk.LEFT, padx=5)
        self.add_point_button = tk.Button(self.button_frame, text="Add Point", command=self.add_manual_point, bg="blue", fg="white", font=("Helvetica", 12, "bold"))
        self.add_point_button.pack(side=tk.LEFT, padx=10)

        # Informasi footer
        self.footer_label = tk.Label(self.main_frame, text="Click on the canvas to add points manually.", font=("Helvetica", 10, "italic"), bg="lightblue")
        self.footer_label.pack(pady=5)

        # Bind mouse click event to canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        """handle click pada canvas"""
        new_point = Point(event.x, event.y)
        print(f"Adding point at: {new_point}")

        # Tambahkan point ke diagram dan perbarui gambar
        if self.diagram.add_point(new_point):
            print("Point added successfully")
            self.draw_cells()
            self.find_and_draw_empty_circles()
        else:
            print("Failed to add point")

    def add_manual_point(self):
        """Add a point based on manual input."""
        try:
            coords = self.manual_input.get().strip().split(",")
            x, y = int(coords[0]), int(coords[1])
            new_point = Point(x, y)
            if self.diagram.add_point(new_point):
                print(f"Added manual point at: ({x}, {y})")
                self.draw_cells()
                self.find_and_draw_empty_circles()
            else:
                print(f"Failed to add point at: ({x}, {y})")
        except (ValueError, IndexError):
            print("Invalid input! Please enter coordinates in the format 'x, y'.")

    def generate_random_points(self):
        """Generate a set of random points."""
        self.clear_canvas()
        num_points = random.randint(5, 15)
        print(f"Generating {num_points} random points...")
        for _ in range(num_points):
            x = random.randint(0, self.canvas_size - 1)
            y = random.randint(0, self.canvas_size - 1)
            new_point = Point(x, y)
            if self.diagram.add_point(new_point):
                print(f"Random point added: ({x}, {y})")
        self.draw_cells()
        self.find_and_draw_empty_circles()

    def draw_cells(self):
        """Menggambar semua cell dan border pada canvas."""
        self.canvas.delete("all")
        for cell in self.diagram.get_cells():
            for line in cell.borders:
                self.draw_line(line)
            self.draw_point(cell.generator)

    def find_circumcircle(self, a, b, c):
        """
        Calculate the circumcircle of three points.
        Returns a dictionary with center and radius or None if points are collinear.
        """
        det = a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y)
        if abs(det) < Point.EPSILON:
            return None

        ax, ay = a.x, a.y
        bx, by = b.x, b.y
        cx, cy = c.x, c.y
        
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        ux = ((ax*ax + ay*ay) * (by - cy) + (bx*bx + by*by) * (cy - ay) + (cx*cx + cy*cy) * (ay - by)) / d
        uy = ((ax*ax + ay*ay) * (cx - bx) + (bx*bx + by*by) * (ax - cx) + (cx*cx + cy*cy) * (bx - ax)) / d

        center = Point(ux, uy)
        radius = math.sqrt((center.x - ax)**2 + (center.y - ay)**2)
        
        return {
            'center': center,
            'radius': radius,
            'points': (a, b, c)
        }

    def find_largest_empty_circles(self):
        generators = [cell.generator for cell in self.diagram.get_cells()[3:]]
        empty_circles = []

        for a, b, c in itertools.combinations(generators, 3):
            circle = self.find_circumcircle(a, b, c)
            
            if circle is None:
                continue

            is_empty = True
            for point in generators:
                if point in circle['points']:
                    continue
                dist = math.sqrt((point.x - circle['center'].x)**2 + (point.y - circle['center'].y)**2)
                if dist <= circle['radius'] + Point.EPSILON:
                    is_empty = False
                    break

            if is_empty:
                empty_circles.append(circle)
                print(circle['radius'])

        if empty_circles:
            max_radius = max(circle['radius'] for circle in empty_circles)
            return [circle for circle in empty_circles if abs(circle['radius'] - max_radius) < Point.EPSILON]
        return []

    def find_and_draw_empty_circles(self):
        if len(self.diagram.get_cells()) < 3:
            return

        self.largest_empty_circles = self.find_largest_empty_circles()

        self.draw_cells()

        for circle in self.largest_empty_circles:
            center = circle['center']
            radius = circle['radius']
            
            self.canvas.create_oval(
                center.x - radius, center.y - radius,
                center.x + radius, center.y + radius,
                outline="red", width=2
            )
            
            self.canvas.create_oval(
                center.x - 3, center.y - 3,
                center.x + 3, center.y + 3,
                fill="red"
            )
            
            for point in circle['points']:
                self.canvas.create_oval(
                    point.x - 5, point.y - 5,
                    point.x + 5, point.y + 5,
                    fill="green"
                )

    def draw_line(self, line):
        """Menggambar garis pada canvas."""
        self.canvas.create_line(line.start.x, line.start.y, line.end.x, line.end.y, fill="blue", width=2)

    def draw_point(self, point, color="black"):
        """Menggambar titik pada canvas."""
        radius = 4
        self.canvas.create_oval(point.x - radius, point.y - radius, point.x + radius, point.y + radius, fill=color)

    def clear_canvas(self):
        """Menghapus semua titik dan sel dari diagram dan canvas."""
        print("Clearing canvas and diagram")
        self.diagram.clear()
        self.canvas.delete("all")

    def load_points_from_file(self):
        """Memuat titik dari file dan menggambar diagram."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        try:
            self.clear_canvas()
            with open(file_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        x, y = map(int, line.strip("()").split(","))
                        point = Point(x, y)
                        if self.diagram.add_point(point):
                            print(f"Point loaded: {point}")
            self.draw_cells()
            self.find_and_draw_empty_circles()
        except Exception as e:
            print(f"Error loading points: {e}")

def main():
    root = tk.Tk()
    root.geometry("800x800")
    root.configure(bg="lightblue")
    diagram = VoronoiDiagram(600)
    MainGUI(root, diagram)
    root.mainloop()

if __name__ == "__main__":
    main()
