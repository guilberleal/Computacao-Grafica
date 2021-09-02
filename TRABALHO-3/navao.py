from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
from PIL import Image
import numpy as np
import random

#fisica
GRAVIDADE = 0.1
VELOCIDADE = 0.1
PULO = 1.5
RESISTENCIA = 1.4
F_RESISTENCIA = 0.2
F_RESISTENCIA_AR = 0.05

#posicao da luz
light_position = [5.0, 10.0, -5.0, 1.0]
light_position2 = [-15.0, 10.0, 20.0, 1.0]

amb_light = [ 0.3, 0.3, 0.3, 1.0]
diffuse = [ 0.9, 0.9, 0.9, 1.0]
specular = [ 1.0, 1.0, 1.0, 1.0]
attenuation_quad = 0.01
attenuation_linear = 0.01

up = down = frente = space = 0


class Nave:
    
    vx = vy = vz = 0.0 #velocidade tiro
    px = py = pz = 0.0 #posicao do tiro
    dir_y = rx = rz = 0.0 #desaceleracao do tiro
    
    
    #texturas
    def atribui_cor(self):
        ouro_amb = [0.24725, 0.1995, 0.0745, 1.0]
        ouro_dif = [0.75164, 0.60648, 0.22648, 1.0]
        ouro_spe = [0.628281, 0.555802, 0.366065, 1.0]
        ouro_shi = 0.4*128.0
        
        nave.mesh_list[0].materials[0].ambient = ouro_amb
        nave.mesh_list[0].materials[0].diffuse = ouro_dif
        nave.mesh_list[0].materials[0].specular = ouro_spe
        nave.mesh_list[0].materials[0].shininess = ouro_shi
        
    	 
        
        
        
     #Atualiza posicao da nave   
    def atualiza_nave(self):

        self.px += self.vx
        self.py += self.vy
        self.pz += self.vz        
        visualization.draw(nave)
        

        if(not (abs(self.px)<=25.0)):
            self.px -= self.vx

        if(not (abs(self.pz)<=25.0)):
            self.pz -= self.vz
            
        if(self.py>15.0):
            self.py = 15.0

        elif(self.py<0.0):
            self.py = 0.0
            self.vy = 0.0

        print("Px: {} // Pz: {} // Py: {}\n".format(self.px, self.pz, self.py))
      

        
	
    def calcula_velocidade(self):

        global up, down, frente
        if(self.py==0.0):

            if(up):

              self.vx += np.sin(self.yaw * 3.14159/180.0)*VELOCIDADE

              self.vz += np.cos(self.yaw * 3.14159/180.0)*VELOCIDADE

              frente = 1

            elif(down):

              self.vx += - np.sin(self.yaw * 3.14159/180.0)*VELOCIDADE

              self.vz += - np.cos(self.yaw * 3.14159/180.0)*VELOCIDADE;   

              frente = 0

          

        

            self.rx = (pow(RESISTENCIA,abs(self.vx))-1.0)*F_RESISTENCIA

            self.rz = (pow(RESISTENCIA,abs(self.vz))-1.0)*F_RESISTENCIA

        else:

            self.rx = (pow(RESISTENCIA,abs(self.vx))-1.0)*F_RESISTENCIA_AR

            self.rz = (pow(RESISTENCIA,abs(self.vz))-1.0)*F_RESISTENCIA_AR

        


        if(self.vx>self.rx):

            self.vx -= self.rx

        elif(self.vx<-self.rx):

            self.vx += self.rx

        elif(abs(self.vz)<self.rx):

            if(abs(self.vx)>0):

                print("Parou\n")

                self.vx = 0.0

                self.vz = 0.0
        
        

class Tiro:

    
    vx = vy = vz = 0.0
    px = py = pz = 0.0
    yaw = pitch = roll = 0.0
    dir_y = rx = rz = 0.0
    
    cor = 1;
    
    #TAMANHO
    minX = px
    maxX = px+1;
    
    minY = 0
    maxY = 1
    
    minZ = pz
    maxZ = pz-1
    
    def atualiza_tiro(self):

        self.px += self.vx

        self.py += self.vy

        self.pz += self.vz
        
        self.minZ = self.pz
        if(self.pz <0):
            self.maxZ = self.pz-1
        else:
            self.maxZ = self.pz+1
        
        

        if(not (abs(self.px)<=25.0)):

            self.px -= self.vx

        if(not (abs(self.pz)<=25.0)):

            self.pz -= self.vz

            
        if(self.py>15.0):

            self.py = 15.0

        elif(self.py<0.0):

            self.py = 0.0

            self.vy = 0.0

        print("Px: {} // Pz: {} // Py: {}\n".format(self.px, self.pz, self.py))

        

        

    def calcula_velocidade(self):

        global up, down, frente, space, pulo

        if(self.py==0.0):

            if(up):

              self.vx += np.sin(self.yaw * 3.14159/180.0)*VELOCIDADE

              self.vz += np.cos(self.yaw * 3.14159/180.0)*VELOCIDADE

              frente = 1

            elif(down):

              self.vx += - np.sin(self.yaw * 3.14159/180.0)*VELOCIDADE

              self.vz += - np.cos(self.yaw * 3.14159/180.0)*VELOCIDADE;   

              frente = 0

          

        

            self.rx = (pow(RESISTENCIA,abs(self.vx))-1.0)*F_RESISTENCIA

            self.rz = (pow(RESISTENCIA,abs(self.vz))-1.0)*F_RESISTENCIA

        else:

            self.rx = (pow(RESISTENCIA,abs(self.vx))-1.0)*F_RESISTENCIA_AR

            self.rz = (pow(RESISTENCIA,abs(self.vz))-1.0)*F_RESISTENCIA_AR

        


        if(self.vz>self.rz):

            self.vz -= self.rz

        elif(self.vz<-self.rz):

            self.vz += self.rz

        elif(abs(self.vx)<self.rz):

            if(abs(self.vz)>0):

                print("Parou\n")

                self.vz = 0.0

                self.vx = 0.0

                
        #starta o tiro saindo da posicao inicial        
        if((space)):
            print('ATIROU \n')
            self.cor = 1
            self.vz -= PULO

            pulo = 1

            
        else:
            if(self.pz <= -23.0):
                self.cor = 0
                self.pz = 20
            pulo = 0
                        
        self.vy -= GRAVIDADE

        #tiro 'some' na posicao final -24
        print("TIRO")
        print("Vx: {} // Vz: {} // Vy: {}\n".format(self.vx, self.vz, self.vy))

        



    
        
tiro = Tiro()
tiro.pz = 20

n = Nave()
n.pz=20






def display():


    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    luz()


	#definindo cor meteoro
    rubi_amb = [0.1745, 0.01175, 0.01175, 1.0]
    rubi_dif = [0.61424, 0.04136, 0.04136, 1.0]
    rubi_spe = [0.727811, 0.626959, 0.626959, 1.0]
    rubi_shi = 0.6*128.0
    	
    	
	
	
	

    glPushMatrix()
    glTranslatef(n.px, n.py, n.pz)
    n.atribui_cor()
    n.calcula_velocidade()
    n.atualiza_nave()
    #visualization.draw(nave)
    glPopMatrix()
	
    glDisable(GL_COLOR_MATERIAL)
    
    
    
        #tiro.atribui_cor()
    tiro.calcula_velocidade()
    tiro.atualiza_tiro()
    
    
    #tiro
    glPushMatrix()
    glTranslatef(n.px, tiro.py, tiro.pz)

    glColor4f(1.0,0.0,0.0,tiro.cor)
    glutSolidSphere(0.8, 8, 8)
    
    glPopMatrix()
    
    glutSwapBuffers()

    
    
    
    
    meteoro.mesh_list[0].materials[0].ambient = rubi_amb
    meteoro.mesh_list[0].materials[0].diffuse = rubi_dif
    meteoro.mesh_list[0].materials[0].specular = rubi_spe
    meteoro.mesh_list[0].materials[0].shininess = rubi_shi  
    
    #meteoro 1
    glPushMatrix()
    glTranslatef(0.0, 4.0, -4.0)
    glScalef(2,2,0.0)
    visualization.draw(meteoro)
    #glutSolidSphere(1.7, 50, 50)
    glPopMatrix()
    #m1
    
    #m2
    glPushMatrix()
    glTranslatef(10.0, 4.0, -4.0)
    glScalef(2,2,0.0)
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
    glTranslatef(-10.0, 4.0, -4.0)
    glScalef(2,2,0.0)
    glutSolidSphere(1.7, 50, 50)
    glPopMatrix()
    #m3
    
    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    glutSwapBuffers()   
    #glPopMatrix()

    

def Keys(key, x, y):

    
    
    if(key == GLUT_KEY_LEFT ):
            n.vx -= 1
            n.px -= 1
    elif(key == GLUT_KEY_RIGHT ): 
            n.px += 1
            n.vx += 1
    

def KeysUp(key, x, y):

    global up, down

    

    if(key == GLUT_KEY_UP ): 

        up = 0

    elif(key == GLUT_KEY_DOWN ): 

        down = 0

        

def Keys_letras(key, x ,y):

    global space

    

    if(key == b' ' ): #Espaço

        space = 1

        

        

def Keys_letras_Up(key, x ,y):

    global space



    if(key == b' ' ): #Espaço

        space = 0

       

def animacao(value):

    glutPostRedisplay()

    glutTimerFunc(33, animacao,1)

    

def resize(w, h):

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluPerspective(65.0, w/h, 1.0, 100.0)

    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()

    gluLookAt(0.0, 25.0, 35.0,

              0.0, 0.0, 0.0,

              0.0, 1.0, 0.0)



def init():

    glClearColor (0.0, 0.0, 0.0, 0.0)
    glEnable( GL_DEPTH_TEST )
    glDepthFunc( GL_LESS )
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )
    
    glShadeModel( GL_SMOOTH )  #Suaviza normais
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    glEnable( GL_LIGHT0 )
    glEnable( GL_LIGHT1 )
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    
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
    

    glLightfv(GL_LIGHT1, GL_POSITION, light_position2)
    glLightfv(GL_LIGHT1, GL_AMBIENT, amb_light)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, specular)
    glLightfv(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, attenuation_quad)
    glLightfv(GL_LIGHT1, GL_LINEAR_ATTENUATION, attenuation_linear)
    glEnable(GL_LIGHT1)


glutInit()

glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)

glutInitWindowSize(520, 520)

glutInitWindowPosition(100, 100)

wind = glutCreateWindow("Cubo")

init()

luz()

nave = pywavefront.Wavefront("navao.obj", create_materials=True)
meteoro = pywavefront.Wavefront("meteoro3.obj", create_materials=True)
glutDisplayFunc(display)

glutReshapeFunc(resize)

glutTimerFunc(33,animacao,1)

glutSpecialFunc(Keys)

glutSpecialUpFunc(KeysUp)

glutKeyboardFunc(Keys_letras)

glutKeyboardUpFunc(Keys_letras_Up)

glutMainLoop()
