from OpenGL.GL import *
from .filling import polygon_filling


class Polygon():

    def __init__(self, color=(1.0, 1.0, 1.0)):
        self.vertices = []
        self.filled_segments = []
        self.color = color
        self.filled = False
    
    def add_vertex(self, x, y):
        self.vertices.append([x, y])

    def clear(self):
        self.vertices.clear()
        self.filled_segments.clear()

    def fill(self, color=(1.0, 1.0, 1.0)):
        self.filled_segments = polygon_filling(self.vertices)
        self.color = color

    def draw_edges(self, current_line_thickness):
        if len(self.vertices) < 2:
            return
        
        glLineWidth(current_line_thickness)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINES)
        for i in range(len(self.vertices)):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % len(self.vertices)]
            glVertex2f(x1, y1)
            glVertex2f(x2, y2)
        glEnd()
    
    def draw_fill(self):
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        for y, x1, x2 in self.filled_segments:
            for x in range(x1, x2 + 1):
                glVertex2f(x, y)
        glEnd()

    
    def check_inside_polygon(self, x, y):
        if not self.vertices or len(self.vertices) < 3:
            return False
        
        intersections = 0
        n = len(self.vertices)
        
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            
            if y1 == y2:
                continue
            # para estar no meio é um xor (sp 1 é maior)
            if (y1 > y) != (y2 > y):
                #  x em que a reta horizontal mouse intercepta a aresta
                x_intersect = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                
                # valida se a interseção foi à direita
                if x_intersect > x:
                    intersections += 1
        
        return intersections % 2 == 1