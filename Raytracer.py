import pygame
from pygame.locals import *
from rt import Raytracer
from figures import *   
from lights import *
from materials import *

width = 920
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame. DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)


raytracer = Raytracer(screen)
raytracer.envMap = pygame.image.load("pics/celeste.jpg")
raytracer.rtClearColor(0.25,0.25,0.25)

#texture
starsTexture = pygame.image.load("pics/stars.png")
mirrorballTexture = pygame.image.load("pics/mirrorball.png")
skyTexture = pygame.image.load("pics/midnight.png")
sunsetTexture = pygame.image.load("pics/sunset.png")

#Materiales
brick = Material(diffuse=(1,0.4,0.4),spec=8,ks=0.01)
grass = Material(diffuse=(0.4,1,0.4),spec=32,ks=0.1)
water = Material(diffuse=(0.4,0.4,1),spec=256,ks=0.2)
concrete = Material(diffuse=(0.5,0.5,0.5),spec=256,ks=0.2)
stars = Material(texture = starsTexture,spec=64,ks=0.1)
sky = Material(texture = skyTexture,spec=30,ks=0.1)
sunset = Material(diffuse=sunsetTexture,spec=256,ks=0.2)


mirror = Material(diffuse=(0.9,0.9,0.9),spec=64,ks=0.2,matType=REFLECTIVE)
blueMirror = Material(diffuse=(0.4,0.4,0.9),spec=32,ks=0.15,matType=REFLECTIVE)
mirrorball = Material(texture = mirrorballTexture,spec=64,ks=0.1,matType=OPAQUE)
glass = Material(diffuse=(0.9,0.9,0.9),spec=64,ks=0.15,ior=1.5,matType=TRANSPARENT)
diamond = Material(diffuse=(0.9,0.9,0.9),spec=128,ks=0.2,ior=2.417,matType=TRANSPARENT)
realWater = Material(diffuse=(0.4,0.4,0.9),spec=128,ks=0.2,ior=1.33,matType=TRANSPARENT)


#figura 1
raytracer.scene.append(Triangle(vertices=[(-1,-2,-6),(0,0,-6),(0.1,-2,-5.5)],material=blueMirror))
raytracer.scene.append(Triangle(vertices=[(1.1,-2,-6),(0,0,-6),(0.1,-2,-5.5)],material=blueMirror))

#figura 2
raytracer.scene.append(Sphere(position=(-2.5,2,-7),radius=1,material=mirror))

#figura 3
raytracer.scene.append(Sphere(position=(-2,1,-7),radius=1,material=stars))

#figura 4
raytracer.scene.append(Sphere(position=(-1,-3,-7),radius=1,material=brick))

#figura 5
raytracer.scene.append(Sphere(position=(0,-1.5,-7),radius=1,material=sky))

#figura 6
raytracer.scene.append(Sphere(position=(2.5,1.5,-7),radius=1,material=water))

#figura 7
raytracer.scene.append(Sphere(position=(1,-2,-3),radius=0.5,material=diamond))

#figura 8
#raytracer.scene.append(Sphere(position=(2,-1,-2),radius=1,material=diamond))

#Cubos
raytracer.scene.append(AABB(position=(-2,1.5,-5),size=(1,1,1),material=sky))
raytracer.scene.append(AABB(position=(2,-0.5,-3.2),size=(1,1,1),material=stars))

#Discos
raytracer.scene.append(Disk(position=(2.1,0.5,-5),normal=(-1,0,0),radius=1,material=blueMirror))
raytracer.scene.append(Disk(position=(0,0.5,-10),normal=(0,0,-1),radius=1.5,material=blueMirror))
raytracer.scene.append(Disk(position=(-2.1,0.5,-5),normal=(-1,0,0),radius=1,material=blueMirror))


raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(direction=(-1,-1,-1),intensity=0.9))

#raytracer.lights.append(PointLight(point=(1.5,0,-5),intensity=1,color=(1,0,1)))


raytracer.rtClear()
raytracer.rtRender()

print("\nTiempo de renderizado:", pygame.time.get_ticks() / 1000, "segundos")

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

rect = pygame.Rect(0,0, width, height)
sub= screen.subsurface(rect)
pygame.image.save(sub, "pics/screenshot.jpg")

pygame.quit()