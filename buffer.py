from OpenGL.GL import *
from numpy import array, float32

class Model(object):
    def __init__(self,data):
        self.vertBuffer = array(data,dtype=float32)
        
        #Vertex Buffer Object
        self.VBO = glGenBuffers(1)
        
        #Vertex Array Object
        self.VAO = glGenVertexArrays(1)
        
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
        glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,4*6,ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        #Atributo de colores
        glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,4*6,ctypes.c_void_p(4*3))
        glEnableVertexAttribArray(1)
        
        glDrawArrays(GL_TRIANGLES,0,int(len(self.vertBuffer)/6))
        
        