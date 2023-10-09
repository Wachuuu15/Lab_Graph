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
raytracer.envMap = pygame.image.load("pics/wal.png")
raytracer.rtClearColor(0.25,0.25,0.25)


#texture
starsTexture = pygame.image.load("pics/stars.png")
mirrorballTexture = pygame.image.load("pics/mirrorball.png")


#Materiales
brick = Material(diffuse=(1,0.4,0.4),spec=8,Ks=0.01)
grass = Material(diffuse=(0.4,1,0.4),spec=32,Ks=0.1)
water = Material(diffuse=(0.4,0.4,1),spec=256,Ks=0.2)
concrete = Material(diffuse=(0.5,0.5,0.5),spec=256,Ks=0.2)
stars = Material(texture = starsTexture,spec=64,Ks=0.1)

mirror = Material(diffuse=(0.9,0.9,0.9),spec=64,Ks=0.2,matType=REFLECTIVE)
blueMirror = Material(diffuse=(0.4,0.4,0.9),spec=32,Ks=0.15,matType=REFLECTIVE)
mirrorball = Material(texture = mirrorballTexture,spec=64,Ks=0.1,matType=OPAQUE)
glass = Material(diffuse=(0.9,0.9,0.9),spec=64,Ks=0.15,ior=1.5,matType=TRANSPARENT)
diamond = Material(diffuse=(0.9,0.9,0.9),spec=128,Ks=0.2,ior=2.417,matType=TRANSPARENT)
realWater = Material(diffuse=(0.4,0.4,0.9),spec=128,Ks=0.2,ior=1.33,matType=TRANSPARENT)

width = 100
height = 100
depth = 600

#Pared izquierda
raytracer.scene.append(Plane(position=(-width,height/2,0),normal=(1,0,0),material=brick))
#Pared derecha
raytracer.scene.append(Plane(position=(width,height/2,0),normal=(-1,0,0),material=grass))
#Fondo
raytracer.scene.append(Plane(position=(0,height/2,-depth/2),normal=(0,0,1),material=water))
#Techo
raytracer.scene.append(Plane(position=(0,height,0),normal=(0,-1,0),material=concrete))
#Suelo
raytracer.scene.append(Plane(position=(0,-height/2,0),normal=(0,1,0),material=concrete))

#Cubos
raytracer.scene.append(AABB(position=(1,1.5,-5),size=(1,1,1),material=mirrorball))
raytracer.scene.append(AABB(position=(-1,-0.5,-3.2),size=(1,1,1),material=stars))

#Discos
raytracer.scene.append(Disk(position=(2.1,0.5,-5),normal=(-1,0,0),radius=1,material=blueMirror))
raytracer.scene.append(Disk(position=(0,0.5,-10),normal=(0,0,-1),radius=1.5,material=blueMirror))
raytracer.scene.append(Disk(position=(-2.1,0.5,-5),normal=(-1,0,0),radius=1,material=blueMirror))

raytracer.lights.append(AmbientLight(intensity=1))
raytracer.lights.append(DirectionalLight(direction=(0,0,-1),intensity=0.9))
raytracer.lights.append(PointLight(point=(1.5,0,-5),intensity=1,color=(1,0,1)))

raytracer.rtClear()
raytracer.rtRender()

print("\nRender Time:",pygame.time.get_ticks()/1000,"secs")


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

