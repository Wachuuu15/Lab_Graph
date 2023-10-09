import pygame
from pygame.locals import *
from rt import Raytracer
from figures import *   
from lights import *
from materials import *

width = 270
height = 500

pygame.init()

screen = pygame.display.set_mode((width, height), pygame. DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)


raytracer = Raytracer(screen)
raytracer.envMap = pygame.image.load("img.jpg")
raytracer.rtClearColor(0.25,0.25,0.25)


flowTexture = pygame.image.load("img.jpg")


brick = Material(diffuse=(1,0.4,0.4), spec = 8,  ks = 0.01)
grass = Material(diffuse=(0.4,1,0.4), spec = 32,  ks = 0.1)
water = Material(diffuse=(0.4,0.4,1), spec = 256, ks = 0.2)

mirror = Material(diffuse=(0.9,0.9,0.9), spec = 64, ks = 0.2, matType = REFLECTIVE)
blueMirror = Material(diffuse=(0.4,0.4,0.9), spec = 32, ks = 0.15, matType = REFLECTIVE)
colorFlow = Material(texture = flowTexture)
reflectFlow = Material(texture = flowTexture, spec = 64, ks = 0.1, matType= REFLECTIVE)

glass = Material(diffuse=(0.9,0.9,0.9), spec = 64, ks = 0.15, ior = 1.5, matType = TRANSPARENT)
diamond = Material(diffuse=(0.9,0.9,0.9), spec = 128, ks = 0.2, ior = 2.417, matType = TRANSPARENT)
water = Material(diffuse=(0.4,0.4,1.0), spec = 128, ks = 0.2, ior = 1.33, matType = TRANSPARENT)

#Colocación de esferas
raytracer.scene.append(Sphere(position=(0,0.5,-5), radius = 1.0, material = water))
raytracer.scene.append(Plane(position=(0,-5,0), normal = (0,1,0), material = brick))
raytracer.scene.append(Disk(position=(0,-1,-5), normal = (0,1,0), radius = 1.5, material = mirror))

#iluminacion minima del ambiente
raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(direction=(-1,-1,-1), intensity=0.9))
#raytracer.lights.append(PointLight(point=(1.5,0,-5), intensity=1, color= (1,0,1)))

raytracer.rtClear()
raytracer.rtRender()

print("\nTiempo de renderizado:", pygame.time.get_ticks() / 1000, "segundos")

isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                isRunning = False

    raytracer.rtClear()
    raytracer.rtRender()
    pygame.display.flip()

pygame.quit()

