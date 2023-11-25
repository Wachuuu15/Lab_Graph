from OpenGL.GL import *
import glm 
from numpy import array, float32
from obj import Obj

import pygame

class Model(object):
    def __init__(self,data):
        self.vertBuffer = array(data,dtype=float32)
        
        #Vertex Buffer Object
        self.VBO = glGenBuffers(1)
        
        #Vertex Array Object
        self.VAO = glGenVertexArrays(1)

        self.position = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0,0,0)
        self.scale    = glm.vec3(1,1,1)

        self.textureSurface = None
        self.textureData = None
        self.textureBuffer = None

    
    def loadTexture(self,textureName):
        self.textureSurface = pygame.image.load(textureName)
        self.textureData = pygame.image.tostring(self.textureSurface,"RGB",True)
        self.textureBuffer = glGenTextures(1)
        

    def getModelMatrix(self):
        identity = glm.mat4(1)

        translateMat = glm.translate(identity, self.position)

        #Rotation X - Pitch
        #Rotation Y - Yaw
        #Rotation Z - Roll

        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
        yaw   = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
        roll  = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

        rotationMat = pitch * yaw * roll

        scaleMat = glm.scale(identity, self.scale)

        return translateMat * rotationMat * scaleMat


    def render(self):
        #Atamos los buffers del object a la GPU
        glBindBuffer(GL_ARRAY_BUFFER,self.VBO)
        glBindVertexArray(self.VAO)
        
        #Especificar la informacion de vertices
        #Buffer ID, Buffer Size in Bytes, Buffer data, Usagge
        glBufferData(GL_ARRAY_BUFFER,self.vertBuffer.nbytes,self.vertBuffer,GL_STATIC_DRAW)
        
        #Atributos
        #Especificar que representa el contenido del vertice
        #Attribute Number,Size,Type,Is it normalized,Stride,Offset

        #Atributo de posiciones
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,4*8,ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        #Atributo de colores
        glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,4*8,ctypes.c_void_p(4*3))
        glEnableVertexAttribArray(1)
       
        #Atributo de normales
        glVertexAttribPointer(2,3,GL_FLOAT,GL_FALSE,4*8,ctypes.c_void_p(4*5))
        glEnableVertexAttribArray(2)
      
        #Activar la textura
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,self.textureBuffer)
        glTexImage2D(GL_TEXTURE_2D,                                 #Texture type
                               0,                                   #Positions
                               GL_RGB,                              #Interal Format
                               self.textureSurface.get_width(),     #width
                               self.textureSurface.get_height(),    #height
                               0,                                   #Border
                               GL_RGB,                              #Format
                               GL_UNSIGNED_BYTE,                    #Type
                               self.textureData)                    #Data
        
        #glGenerateMipmap(GL_TEXTURE_2D)
        glGenerateTextureMipmap(self.textureBuffer)

        #Normals
        glVertexAttribPointer(2, 
                              3, 
                              GL_FLOAT, 
                              GL_FALSE, 
                              4 * 8, 
                              ctypes.c_void_p(4 * 5))

        glDrawArrays(GL_TRIANGLES,0,int(len(self.vertBuffer)/8))
        
