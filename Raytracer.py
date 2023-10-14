import pygame
from pygame.locals import *
from rt import Raytracer
from figures import *   
from lights import *
from materials import *

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame. DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)


raytracer = Raytracer(screen)
raytracer.envMap = pygame.image.load("pics/sky_pink.png")
raytracer.rtClearColor(0.25,0.25,0.25)

#texture
starsTexture = pygame.image.load("pics/stars.png")
mirrorballTexture = pygame.image.load("pics/mirrorball.png")
skyTexture = pygame.image.load("pics/midnight.png")


#Materiales
brick = Material(diffuse=(1,0.4,0.4),spec=8,ks=0.01)
grass = Material(diffuse=(0.4,1,0.4),spec=32,ks=0.1)
water = Material(diffuse=(0.4,0.4,1),spec=256,ks=0.2)
concrete = Material(diffuse=(0.5,0.5,0.5),spec=256,ks=0.2)
stars = Material(texture = starsTexture,spec=64,ks=0.1)
sky = Material(texture = skyTexture,spec=64,ks=0.1)


mirror = Material(diffuse=(0.9,0.9,0.9),spec=64,ks=0.2,matType=REFLECTIVE)
blueMirror = Material(diffuse=(0.4,0.4,0.9),spec=32,ks=0.15,matType=REFLECTIVE)
mirrorball = Material(texture = mirrorballTexture,spec=64,ks=0.1,matType=OPAQUE)
glass = Material(diffuse=(0.9,0.9,0.9),spec=64,ks=0.15,ior=1.5,matType=TRANSPARENT)
diamond = Material(diffuse=(0.9,0.9,0.9),spec=128,ks=0.2,ior=2.417,matType=TRANSPARENT)
realWater = Material(diffuse=(0.4,0.4,0.9),spec=128,ks=0.2,ior=1.33,matType=TRANSPARENT)



#raytracer.scene.append(Sphere(position=(0,-1,3),radius=0.15,material=mirror))

#Cubos
raytracer.scene.append(AABB(position=(-1,1.5,-5),size=(1,1,1),material=mirrorball))
raytracer.scene.append(AABB(position=(2,-0.5,-3.2),size=(1,1,1),material=stars))


raytracer.scene.append(Triangle(vertices= [(-1, -2, -6), (0, 2, -6), (0.2, -2.5, -5.7)], material=realWater))
raytracer.scene.append(Triangle(vertices=[(1.1, -2, -6), (0, 2, -6), (0.2, -2.5, -5.7)], material=realWater))

raytracer.scene.append(Triangle(vertices=[(-1, 0, -5), (0, 2, -5), (1, 0, -5)], material=mirror))
raytracer.scene.append(Triangle(vertices=[(-1, 0, -5), (0, 2, -6), (1, 0, -5)], material=mirror))


raytracer.scene.append(Triangle(vertices= [(-2, -2, -6), (-2, 2, -6), (1, -2.5, -5.7)], material=realWater))
raytracer.scene.append(Triangle(vertices=[(2, -2, -6), (-2, 2, -6), (1, -2.5, -5.7)], material=realWater))


raytracer.lights.append(AmbientLight(intensity=2))
raytracer.lights.append(DirectionalLight(direction=(0,0,-1),intensity=0.9))

#raytracer.lights.append(PointLight(point=(1.5,0,-5),intensity=1,color=(1,0,1)))

raytracer.rtClear()
raytracer.rtRender()


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

