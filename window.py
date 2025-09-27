from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

poligono = []


# Cria reta 
def trace_line(point1, point2):

    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)

    glVertex2f(point1[0], point1[1])
    glVertex2f(point2[0], point2[1])

    glEnd()

def draw_polygon(polygon):
    if len(polygon) >= 2:
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

def display():

    glClear(GL_COLOR_BUFFER_BIT)
    draw_polygon(poligono)
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