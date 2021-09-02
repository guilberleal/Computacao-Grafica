from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
import random
import decimal
from pywavefront import visualization

T = 1
T2 = 1
T3 = 1

F1 = 1
flag = 1

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    glPushMatrix()
    glTranslatef(T, T2, T3)
    glPushMatrix()
    
    #inicio nave
    glTranslatef(0.0, -10.0, 0.0)
    glColor3f(0.2, 0.3, 0.4)
    visualization.draw(carro)
    glPopMatrix()
    #fim nave

        
    glPopMatrix()
    
    

    
    glPushMatrix()
    global F1
    global flag
    if(flag == 1):
        if(F1 <=6):
            F1 = F1 + 0.125
        if(F1 == 6):
            flag = 0
    elif(flag == 0):
        if(F1 >=-6):
            F1 = F1 - 0.125
        if(F1 == -6):
            flag = 1
    glTranslatef(F1, 1.0, 1.0)
    #inicio meteoro 1
    glPushMatrix()
    
    #glPushMatrix()
    glTranslatef(0.0, 5.0, -5.0)
    glScalef(0.5,0.5,0.0)
    glColor3f(0.40, 0.24, 0.53)
    visualization.draw(meteoro)
    
    glPopMatrix()
    #fim meteoro 1
    #inicio meteoro 2
    glPushMatrix()
    
    glTranslatef(3.0, 5.0, -5.0)
    glScalef(0.5,0.5,0.0)
    glColor3f(0.4, 0.24, 0.53)
    visualization.draw(meteoro)
    
    glPopMatrix()
    #fim meteoro 2
    #inicio meteoro 3
    glPushMatrix()
    glTranslatef(-3.0, 5.0, -5.0)
    glScalef(0.5,0.5,0.0)
    glColor3f(0.4, 0.24, 0.53)
    visualization.draw(meteoro)
    
    glPopMatrix()
    #fim meteoro 3
    
    glPopMatrix()
            
    
    glutSwapBuffers()
    
def Keys(key, x, y):
    global T
    DIR = 10
    ESQ = -10
    
    if(key == GLUT_KEY_LEFT ):
        if(T >= ESQ):
            T -= 1
    elif(key == GLUT_KEY_RIGHT ): 
        if(T <= DIR):
            T += 1
    
def animacao(value):
    glutPostRedisplay()
    glutTimerFunc(30, animacao,1)
    
def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(80.0, w/h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 10.0, 10.0,
                0.0, 0.0, 0.0,
                0.0, 1.0, 0.0)

def init():
    glClearColor (0.3, 0.3, 0.3, 0.0)
    glShadeModel( GL_SMOOTH )
    glClearColor( 0.14, 0.15, 0.15, 0.5)
    glClearDepth( 1.0 )
    glEnable( GL_DEPTH_TEST )
    glDepthFunc( GL_LEQUAL )
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )

    glLightModelfv( GL_LIGHT_MODEL_AMBIENT, [0.3, 0.3, 0.3, 1.0] )
    glLightfv( GL_LIGHT0, GL_AMBIENT, [ 0.6, 0.6, 0.6, 1.0] )
    glLightfv( GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0] )
    glLightfv( GL_LIGHT0, GL_SPECULAR, [0.7, 0.7, 0.7, 1] );
    glLightfv( GL_LIGHT0, GL_POSITION, [2.0, 2.0, 1.0, 0.0])
    glEnable( GL_LIGHT0 )
    glEnable( GL_COLOR_MATERIAL )
    glShadeModel( GL_SMOOTH )
    glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE )
    glDepthFunc( GL_LEQUAL )
    glEnable( GL_DEPTH_TEST )
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Cubo")
init()
meteoro = pywavefront.Wavefront("meteoro3.obj")
carro = pywavefront.Wavefront("nave.obj")
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
glutSpecialFunc(Keys)
glutMainLoop()
