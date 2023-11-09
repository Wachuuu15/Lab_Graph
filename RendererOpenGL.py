
import pygame
from pygame.locals import *
import glm

from gl import Renderer
from model import Model
from shaders import *
from obj import Obj

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width,height),pygame.OPENGL|pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.setShaders(vertex_shader,fragment_shader)


obj = Obj(filename="obj/12221_Cat_v1_l3.obj")
objData = []

for face in obj.faces:

    if len(face) == 3:

        for vertexInfo in face:

            vertexID, texcoordID, normalID = vertexInfo
            vertex = obj.vertices[vertexID - 1]
            normals = obj.normals[normalID - 1]
            uv = obj.textcoords[texcoordID - 1]
            uv = [uv[0], uv[1]]

            objData.extend(vertex + uv + normals)

    elif len(face) == 4:

        for i in [0, 1, 2]:

            vertexInfo = face[i]
            vertexID, texcoordID, normalID = vertexInfo
            vertex = obj.vertices[vertexID - 1]
            normals = obj.normals[normalID - 1]
            uv = obj.textcoords[texcoordID - 1]

            uv = [uv[0], uv[1]]

            objData.extend(vertex + uv + normals)

        for i in [0, 2, 3]:

            vertexInfo = face[i]

            vertexID, texcoordID, normalID = vertexInfo
            vertex = obj.vertices[vertexID - 1]
            normals = obj.normals[normalID - 1]
            uv = obj.textcoords[texcoordID - 1]
            uv = [uv[0], uv[1]]

            objData.extend(vertex + uv + normals)


model = Model(objData)

model.loadTexture("texture/Cat_diffuse.jpg")


# El modelo inicialmente mira hacia abajo en el eje Y (-90 grados en Y)
initial_rotation = glm.vec3(20, 0, 0)

desired_rotation = glm.vec3(2, 2, -2)  # Rotación que hace que el modelo mire hacia la cámara
model.rotation = desired_rotation

# Configurar la posición y escala según sea necesario
model.position.z = -6
model.position.y = 0
model.scale = glm.vec3(0.05, 0.05, 0.05)


rend.scene.append(model)
rend.target = model.position



#                 # POSITIONS,    COLORS
# triangleData = [-0.5,-0.5,0,    1.0,0.0,0.0,
#                 0,0.5,0,        0.0,1.0,0.0,
#                 0.5,-0.5,0,     0.0,0.0,1.0]

# triangleModel = Model(triangleData)
# triangleModel.position.z = -10
# triangleModel.scale = glm.vec3(5,5,5)

# rend.scene.append(triangleModel)

isRunning = True

while isRunning:
    deltaTime = clock.tick(60)/1000
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            isRunning = False
            
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                isRunning = False

            if event.key == pygame.K_ESCAPE:
                rend.toogleFiledMode()
    
    if keys[K_d]:
        rend.camPosition.x += 5 * deltaTime 

    elif keys[K_a]:
        rend.camPosition.x -= 5 * deltaTime

    if keys[K_w]:
        rend.camPosition.z += 5* deltaTime

    elif keys[K_s]:
        rend.camPosition.z -= 5 * deltaTime

        
    if keys[K_q]:
        rend.camPosition.y += 5 * deltaTime

    elif keys[K_e]:
        rend.camPosition.y -= 5 * deltaTime 

    
    rend.update()
    rend.render()
    pygame.display.flip()
    
pygame.quit()