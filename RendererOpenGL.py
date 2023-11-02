
import pygame
from pygame.locals import *
import glm

from gl import Renderer
from model import Model
from shaders import *

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width,height),pygame.OPENGL|pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.setShaders(vertex_shader,fragment_shader)

            # POSITIONS,    COLORS
triangleData = [-0.5,-0.5,0,    1.0,0.0,0.0,
               0,0.5,0,     0.0,1.0,0.0,
             0.5,-0.5,0,    0.0,0.0,1.0]

triangleModel = Model(triangleData)
triangleModel.position.z = -5
triangleModel.scale = glm.vec3(5,5,5)

rend.scene.append(triangleModel)

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
    
    if keys[K_RIGHT]:
        if rend.clearColor[0]<1.0:
            rend.clearColor[0]+=deltaTime
    
    rend.render()
    pygame.display.flip()
    
pygame.quit()