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
raytracer.rtClearColor(0.25,0.25,0.25)

brick = Material(diffuse=(1,0.4,0.4), spec= 8, ks=0.01)
grass = Material(diffuse=(0.4,1,0.4), spec= 32, ks=0.1)
water = Material(diffuse=(0.4,0.4,1), spec= 256, ks=0.2)
button = Material(diffuse=(0,0,0),spec=32,ks=0.1)
carrot = Material(diffuse=(0.93,0.57,0.13), spec = 5, ks = 0.02)
smile = Material(diffuse=(0.60,0.60,0.60), spec = 5, ks = 0.02)
eyes = Material(diffuse=(0.86,0.88,0.85), spec = 5, ks = 0.02)
ojo = Material(diffuse=(0.15,0.15,0.15), spec = 5, ks = 0.02)




#bolas de nieve
raytracer.scene.append(Sphere(position=(0,-2,-10),radius= 2, material= brick))
raytracer.scene.append(Sphere(position=(0,0.9,-10),radius= 1.3, material= water))
raytracer.scene.append(Sphere(position=(0,2.8,-10),radius= 0.7, material= water))


#botones
raytracer.scene.append(Sphere(position=(0,-1,3),radius=0.15,material=button))
raytracer.scene.append(Sphere(position=(0,0,0),radius=0.1,material=button))
raytracer.scene.append(Sphere(position=(0,0.2,-2),radius=0.1,material=button))


#Zanahoria
raytracer.scene.append(Sphere(position=(0,1,-4), radius = 0.1, material = carrot))

#Boca
raytracer.scene.append(Sphere(position=(-0.35,1.54,-4.15), radius = 0.075, material = smile))
raytracer.scene.append(Sphere(position=(-0.13,1.49,-4.15), radius = 0.075, material = smile))
raytracer.scene.append(Sphere(position=(0.12,1.51,-4.15), radius = 0.075, material = smile))
raytracer.scene.append(Sphere(position=(0.35,1.55,-4.15), radius = 0.075, material = smile))

#Ojos
raytracer.scene.append(Sphere(position=(0.145,2.04,-4.1), radius = 0.05, material = eyes))
raytracer.scene.append(Sphere(position=(-0.145,2.04,-4.1), radius = 0.05, material = eyes))
raytracer.scene.append(Sphere(position=(-0.145,2.03,-4.05), radius = 0.025, material = ojo))
raytracer.scene.append(Sphere(position=(0.145,2.03,-4.05), radius = 0.025, material = ojo))



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

