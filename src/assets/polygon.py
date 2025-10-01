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

    def draw_edges(self):
        if len(self.vertices) < 2:
            return
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
        if not self.vertices:
            return False
        
        min_x = min(v[0] for v in self.vertices)
        max_x = max(v[0] for v in self.vertices)
        min_y = min(v[1] for v in self.vertices)
        max_y = max(v[1] for v in self.vertices)

        click_x, click_y = x, y
        
        return min_x <= click_x <= max_x and min_y <= click_y <= max_y