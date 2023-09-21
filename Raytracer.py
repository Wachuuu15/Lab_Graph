import pygame
from pygame.locals import *

from rt import Raytracer
from figures import *   
from lights import *
from materials import *

width = 500
height = 270

pygame.init()

screen = pygame.display.set_mode((width, height), pygame. DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)


raytracer = Raytracer(screen)
raytracer.rtClearColor(0.25,0.25,0.25)

brick = Material(diffuse=(1,0.4,0.4), spec= 8, ks=0.01)
grass = Material(diffuse=(0.4,1,0.4), spec= 32, ks=0.1)
water = Material(diffuse=(0.4,0.4,1), spec= 256, ks=0.2)



#bolas de nieve
raytracer.scene.append(Sphere(position=(0,-2,-5),radius= 2, material= brick))
raytracer.scene.append(Sphere(position=(0,0.9,-5),radius= 1.3, material= water))
raytracer.scene.append(Sphere(position=(0,2.8,-5),radius= 0.7, material= water))

#botones
raytracer.scene.append(Sphere(position=(0,0,-2),radius= 0.3, material= grass))
raytracer.scene.append(Sphere(position=(0,0,-15),radius= 0.5, material= water))

#luces
raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(direction=(-1,-1,-1), intensity= 0.7))

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

