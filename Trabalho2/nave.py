from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
import random
import decimal
from pywavefront import visualization
from PIL import Image

T = 1
T2 = 1
T3 = 1

lim = 1
flag = 1

#PROPRIEDADES DA LUZ
light_position = [0.0, -5.0, 0.0, 1.0]
light_position_2 = [0.0, 10.0, 0.0, 1.0]

amb_light = [ 0.3, 0.3, 0.3, 1.0]
diffuse = [ 0.9, 0.9, 0.9, 1.0]
specular = [ 1.0, 1.0, 1.0, 1.0]
attenuation_quad = 0.01
attenuation_linear = 0.01

def display():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    luz()
   
    #DEFINICAO DAS CORES
    #ouro pra nave
    rubi_amb = [0.1745, 0.01175, 0.01175, 1.0]
    rubi_dif = [0.61424, 0.04136, 0.04136, 1.0]
    rubi_spe = [0.727811, 0.626959, 0.626959, 1.0]
    rubi_shi = 0.6*128.0
    #rubi
    ouro_amb = [0.24725, 0.1995, 0.0745, 1.0]
    ouro_dif = [0.75164, 0.60648, 0.22648, 1.0]
    ouro_spe = [0.628281, 0.555802, 0.366065, 1.0]
    ouro_shi = 0.4*128.0


    glPushMatrix()
    glTranslatef(T, T2, T3)
    
    nave.mesh_list[0].materials[0].ambient = ouro_amb
    nave.mesh_list[0].materials[0].diffuse = ouro_dif
    nave.mesh_list[0].materials[0].specular = ouro_spe
    nave.mesh_list[0].materials[0].shininess = ouro_shi

    glPushMatrix()
    glTranslatef(0.0, -10.0, 0.0)
    visualization.draw(nave)
    glPopMatrix()
    glPopMatrix()

    glEnable(GL_COLOR_MATERIAL)
    
    glPushMatrix()
    global lim
    global flag
    if(flag == 1):
        if(lim <=4):
            lim = lim + 0.125
        if(lim == 4):
            flag = 0
    elif(flag == 0):
        if(lim >=-4):
            lim = lim - 0.125
        if(lim == -4):
            flag = 1
    glTranslatef(lim, 1.0, 1.0)
    glDisable(GL_COLOR_MATERIAL)
    
    #Material dos meteoros
    meteoro.mesh_list[0].materials[0].ambient = rubi_amb
    meteoro.mesh_list[0].materials[0].diffuse = rubi_dif
    meteoro.mesh_list[0].materials[0].specular = rubi_spe
    meteoro.mesh_list[0].materials[0].shininess = rubi_shi    
   
    #m1
    glPushMatrix()
    glTranslatef(0.0, 4.0, -4.0)
    glScalef(0.8,0.8,0.0)
    visualization.draw(meteoro)
    #glutSolidSphere(1.7, 50, 50)
    glPopMatrix()
    #m1
    
    #m2
    glPushMatrix()
    glTranslatef(3.0, 4.0, -4.0)
    glScalef(0.8,0.8,0.0)
    visualization.draw(meteoro)
    #glutSolidSphere(1.7, 50, 50)
    glPopMatrix()
    #m2

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)

    glBindTexture(GL_TEXTURE_2D, lua_ID)
    
    #m3
    glPushMatrix()
    glTranslatef(-3.0, 4.0, -4.0)
    glScalef(0.8,0.8,0.0)
    glutSolidSphere(1.7, 50, 50)
    glPopMatrix()
    #m3
    
    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    glutSwapBuffers()   

    glPopMatrix()
    
def Keys(key, x, y):
    global T
    DIR = 8
    ESQ = -8
    
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
    gluPerspective(65.0, w/h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 10.0, 10.0,
                0.0, 0.0, 0.0,
                0.0, 1.0, 0.0)

def init():
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glEnable( GL_DEPTH_TEST )
    glDepthFunc( GL_LESS )
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )
    
    glShadeModel( GL_SMOOTH )  #Suaviza normais
    glEnable(GL_NORMALIZE)
    
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_BLEND)
    
    global lua_ID
    lua_img = Image.open('rock.jpg')
    lua_img = lua_img.resize((512,512), resample=Image.LANCZOS)
    w, h, lua_img = lua_img.size[0], lua_img.size[1], lua_img.tobytes("raw", "RGB", 0, -1)
    lua_ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, lua_ID)
    
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, w, h, GL_RGB, GL_UNSIGNED_BYTE, lua_img)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
   

def luz():
    glEnable(GL_LIGHTING)
    
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, amb_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, attenuation_quad)
    glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, attenuation_linear)
    glEnable(GL_LIGHT0)
    
    glLightfv(GL_LIGHT1, GL_POSITION, light_position_2)
    glLightfv(GL_LIGHT1, GL_AMBIENT, amb_light)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, attenuation_quad)
    glLightfv(GL_LIGHT1, GL_LINEAR_ATTENUATION, attenuation_linear)
    glEnable(GL_LIGHT1)

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Cubo")
init()
luz()
meteoro = pywavefront.Wavefront("meteoro3.obj", create_materials=True)
nave = pywavefront.Wavefront("navechaveLOW.obj", create_materials=True)
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
glutSpecialFunc(Keys)
glutMainLoop()
