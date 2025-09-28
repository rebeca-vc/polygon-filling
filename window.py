from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

poligono = []
filled_segments = []

def get_edges(vertex, adjacent):
    
    if vertex[1] <= adjacent[1]:

        if vertex[1] >= adjacent[1]:
            xmax = vertex[0]
            ymax = vertex[1]
            xmin = adjacent[0]
            ymin = adjacent[1]
        else:
            xmax = adjacent[0]
            ymax = adjacent[1]
            xmin = vertex[0]
            ymin = vertex[1]

        inclination = 0 
        if (xmax - xmin) != 0 and (ymax - ymin) != 0:
            m = (ymax - ymin) / (xmax - xmin)
            inclination = 1/m

        return [ymax, xmin, inclination]
    
    return None
    

def get_edges_list(polygon, index):

    vertex = polygon[index]

    # ultimo ponto
    if index == len(polygon) - 1:
        next = polygon[0]
    else:
        next = polygon[index + 1]


    # primeiro ponto
    if index == 0:
        previous = polygon[len(polygon) - 1]
    else:
        previous = polygon[index - 1]

    edges_list = []
    if get_edges(vertex, next) != None:
        edges_list.append(get_edges(vertex, next))
    if get_edges(vertex, previous) != None:
        edges_list.append(get_edges(vertex, previous))

    return edges_list

def polygon_filling(polygon):

    if len(polygon) < 3:
        return

    ET = dict()
    for i in range(len(polygon)):

        edges = get_edges_list(polygon, i)
        
        if len(edges) != 0:
            if polygon[i][1] in ET:
                ET[polygon[i][1]] += edges
            else:
                ET[polygon[i][1]] = edges
    
    print(ET)

    if not ET:
        return

    y = min(ET.keys())      
    AET = []               

    while ET or AET:

        # remove arestas de ET e adiciona em AET 
        if y in ET:
            AET.extend(ET.pop(y))

        # mantém AET ordenada por x
        AET.sort(key=lambda e: e[1])

        # remore arestas já concluidas de AET quando o ymax passou
        AET = [edge for edge in AET if edge[0] > y]

        # desenhar linha de varredura
        for i in range(0, len(AET), 2):
            if i + 1 < len(AET):
                x1 = round(AET[i][1])
                x2 = round(AET[i + 1][1])
                
                # desenha linha
                filled_segments.append((y, x1, x2))

                print(f"Scanline y={y}: preencher de x={x1} até x={x2}")

        # 3.4 – incrementa y
        y += 1

        # 3.5 – atualiza x das arestas remanescentes
        for edge in AET:
            edge[1] += edge[2]  # x = x + 1/m

        # 3.6 – reordena AET por x
        AET.sort(key=lambda e: e[1])


def trace_scan_lines():
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    for y, x1, x2 in filled_segments:
        for x in range(x1, x2 + 1):
            glVertex2f(x, y)
    glEnd()


# Cria reta 
def trace_line(point1, point2):

    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)

    glVertex2f(point1[0], point1[1])
    glVertex2f(point2[0], point2[1])

    glEnd()

def draw_polygon(polygon):

    if len(polygon) < 2:
        return
    
    print("ENTROU AQUI")
    trace_line(polygon[0], polygon[len(polygon) - 1])
    for i in range(len(polygon) - 1):
        trace_line(polygon[i], polygon[i+1])

        
def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Cria o polígono
        height = glutGet(GLUT_WINDOW_HEIGHT)
        point = [x, height - y]
        print(point)
        poligono.append(point)
        glutPostRedisplay()

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Preenche o polígono
        print("DIREITO")
        polygon_filling(poligono)
        glutPostRedisplay()

def display():

    glClear(GL_COLOR_BUFFER_BIT)
    draw_polygon(poligono)
    trace_scan_lines()
    glFlush()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"Trabalho 1")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 600, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutMainLoop()
    return 0

main()