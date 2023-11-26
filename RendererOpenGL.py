import pygame
from pygame.locals import *
import glm

from gl import Renderer
from model import Model
from shaders import *
from obj import Obj
from math import pi,sin,cos


width = 960
height = 540    

pygame.init()

screen = pygame.display.set_mode((width,height),pygame.OPENGL|pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)
skyboxTextures = ["skybox/right.png",
                  "skybox/left.png",
                  "skybox/top.png",
                  "skybox/bottom.png",
                  "skybox/front.png",
                  "skybox/back.png"]

rend.createSkybox(skyboxTextures, skybox_vertex_shader, skybox_fragment_shader)

rend.setShaders(vertex_shader,fragment_shader)


objects_info = [
    {"obj_file": "obj/12221_Cat_v1_l3.obj", "textures": ["texture/Cat_diffuse.jpg"]},
    {"obj_file": "obj/12961_White-Tailed_Deer_v1_l2.obj", "textures": ["texture/12961_White-TailedDeer_diffuse.jpg"]},
    {"obj_file": "obj/12265_Fish_v1_L2.obj", "textures": ["texture/fish.jpg"]},
    {"obj_file": "obj/10042_Sea_Turtle_V2_iterations-2.obj", "textures": ["texture/10042_Sea_Turtle_V1_Diffuse.jpg"]},
]

# Lista para almacenar los objetos
objects = []

for obj_info in objects_info:
    obj_file = obj_info["obj_file"]
    textures = obj_info["textures"]

    obj = Obj(filename=obj_file)
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
    #Model position
    model.position.z = -2.4
    model.position.y = 3
    model.position.x = -2
    model.rotation.y = 5
    model.scale = glm.vec3(1.20, 1.20, 1.20)
    model.lookAt = glm.vec3(model.position.x + 0.4, model.position.y + 2 , model.position.z - 2.4)

    

    # Cargar texturas para el objeto actual
    for i, texture_file in enumerate(textures):
        model.loadTexture(texture_file)

    objects.append(model)
current_object_index = 0

# Configuración del primer objeto
current_object = objects[current_object_index]

rend.scene.append(current_object)
rend.target = current_object.position
rend.lightIntensity = 0.2
rend.dirLight = glm.vec3(0.0, 0.0, -1.0)

taylor_song= pygame.mixer.music.load("music/LateNightTalking.mp3")
#taylor_song.set_volume(0.3)

isRunning = True

while isRunning:
    deltaTime = clock.tick(60)/1000
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                isRunning = False
            elif event.key == pygame.K_RIGHT:
                current_object_index = (current_object_index + 1) % len(objects)
                rend.scene.remove(current_object)
                current_object = objects[current_object_index]
                rend.scene.append(current_object)
                rend.target = current_object.position
                current_object.shader = rend.activeShader

            # Manejo de cambio de shader con las teclas 1-5
            elif event.key == pygame.K_1:
                print("1")
                rend.setShaders(vertex_shader, toon_shader)
                current_object.shader = rend.activeShader
                pygame.mixer.music.play()

            elif event.key == pygame.K_2:
                print("2")
                rend.setShaders(vertex_shader, water_shader)
                current_object.shader = rend.activeShader
            elif event.key == pygame.K_3:
                print("3")
                rend.setShaders(vertex_shader, manchas_shader)
                current_object.shader = rend.activeShader
            elif event.key == pygame.K_4:
                print("4")
                rend.setShaders(vertex_shader, stars_shader)
                current_object.shader = rend.activeShader
            elif event.key == pygame.K_5:
                print("5")
                rend.setShaders(vertex_shader, fire_shader)
                current_object.shader = rend.activeShader
        
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:  # Botón izquierdo del mouse
                # Mover la cámara en función del movimiento del mouse
                rend.camPosition.x += event.rel[1] * 0.1 
                rend.camPosition.y += event.rel[0] * 0.1

            elif event.buttons[0] == 2:
                rend.camPosition.z += event.rel[1] * 0.1 
                rend.camPosition.z += event.rel[0] * 0.1

    # # Rotar cámara a la izquierda 
    # elif keys[K_LEFT]:
    #     rend.camRotation += 45 * deltaTime  # ajusta la velocidad de rotación según sea necesario


    if keys[K_d]:
        rend.camPosition.x += 20* deltaTime 

    # #left al objeto [a]

    elif keys[K_a]:
        rend.camPosition.x -=  20* deltaTime

    # #ZoomIn al objeto [w]
    if keys[K_w]:
        rend.camPosition.z += 20* deltaTime
    #ZoomOut al objeto [s]
    elif keys[K_s]:
        rend.camPosition.z -= 20* deltaTime

    #Movimiento de camara hacia arriba [q]
    if keys[K_q]:
        rend.camPosition.y += 20* deltaTime
     #Movimiento de camara hacia abajo [e]
    elif keys[K_e]:
        rend.camPosition.y -= 20* deltaTime 

    if keys[K_UP]:
        if rend.fatness<1.0:
            rend.fatness += 1 * deltaTime
    elif keys[K_DOWN]>0.0:
        rend.fatness -= 1 *deltaTime

    
    rend.update()
    rend.render()
    pygame.display.flip()
    
pygame.quit()