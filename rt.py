from math import tan, pi, atan2, acos
import math 
import numpy as np
import numpi as Numpi
import random
import pygame
from materials import *
from lights import *

MAX_RECURSION_DEPTH = 3

class Raytracer(object):
    def __init__(self, screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect()

        self.rtViewPort(0,0,self.width,self.height)
        self.rtColor(1,1,1)
        self.rtClearColor(0,0,0)
        self.rtClear()
        self.rtProyection()
        self.camPosition = [0,0,0]
        self.scene = []
        self.lights=[]

    def rtViewPort(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height
    
    def rtProyection(self, fov = 60, n = 0.1 ):
        aspectRatio = self.vpWidth / self.vpHeight
        self.nearPlane = n
        self.topEdge = math.tan((fov*math.pi/180)/2) * self.nearPlane
        self.rightEdge = self.topEdge * aspectRatio

    def rtClearColor(self,r,g,b):
        self.clearColor = (r * 255,g * 255,b * 255)

    def rtClear(self):
        self.screen.fill(self.clearColor)
        
    def rtColor(self,r,g,b):
        self.currColor = (r * 255,g * 255,b * 255)

    def rtPoint(self, x,y,color = None):
        y=self.height - y

        if (0<=x<self.width) and (0<=y<self.height):
            if color!=None:
                color = (int(color[0]*255),
                         int(color[1]*255),
                         int(color[2]*255))
                self.screen.set_at((x,y), color)
            else:
                self.screen.set_at((x,y),self.currColor)

    def rtCastRay(self, orig, dir):
        depht = float('inf')
        intercept = None
        hit = None

        for obj in self.scene:
            intercept = obj.ray_intersect(orig, dir)
            if intercept != None:
                if intercept.distance < depht:
                    hit = intercept
                    depht= intercept.distance

        return hit

    def rtRayColor(self, intercept, rayDirection, recursion=0):
        if intercept== None:
            if self.envMap:
                x = (atan2(rayDirection[2], rayDirection[0]) / (2*pi) + 0.5) * self.envMap.get_width() 
                y = acos(rayDirection[1])/pi * self.envMap.get_height()
                
                envColor = self.envMap.get_at((int(x),int(y)))
                
                return [i/255 for i in envColor]
                return
            else:
                return None
        
        material = intercept.obj.material
        surfaceColor = material.diffuse
        
        if material.texture and intercept.texcoords:
            tx = intercept.texcoords[0]*material.texture.get_width()
            ty = intercept.texcoords[1]*material.texture.get_height()
            
            texColor = material.texture.get_at((int(tx), int(ty)))
            texColor = [i/255 for i in texColor]
            surfaceColor = [surfaceColor[i]*texColor[i] for i in range(3)]
        
        ambientColor = [0,0,0]
        reflectColor = [0,0,0]
        refractColor = [0,0,0]
        diffuseColor = [0,0,0]
        specularColor = [0,0,0]
        finalColor = [0,0,0]
        
        if material.matType == OPAQUE:
            for light in self.lights:
                if light.lightType == "Ambient":
                    ambientColor = [(ambientColor[i]+light.getLightColor()[i]) for i in range(3)]
                
                else:
                    lightDir = None
                    if light.lightType == "Directional":
                        lightDir = [(i*-1) for i in light.direction]
                    elif light.lightType == "Point":
                        lightDir = Numpi.substractV(light.point, intercept.point)
                        lightDir = Numpi.normalizeV(lightDir)
                        
                    shadowIntersect = self.rtCastRay(intercept.point, lightDir, intercept.obj)
                    
                    if shadowIntersect==None:
                        diffuseColor = [(diffuseColor[i]+light.getDiffuseColor(intercept)[i]) for i in range(3)]
                        specularColor = [(specularColor[i]+light.getSpecularColor(intercept, self.camPosition)[i]) for i in range(3)]
        
        elif material.matType == REFLECTIVE:
            reflect = Numpi.reflectVector(intercept.normal, [i*-1 for i in rayDirection])
            reflectIntercept = self.rtCastRay(intercept.point, reflect, intercept.obj, recursion + 1)
            reflectColor = self.rtRayColor(reflectIntercept, reflect, recursion + 1)
            
            for light in self.lights:
                if light.lightType != "Ambient":
                    lightDir = None
                    if light.lightType == "Directional":
                        lightDir = [(i*-1) for i in light.direction]
                    elif light.lightType == "Point":
                        lightDir = Numpi.substractV(light.point, intercept.point)
                        lightDir = Numpi.normalizeV(lightDir)
                        
                    shadowIntersect = self.rtCastRay(intercept.point, lightDir, intercept.obj)
                    
                    if shadowIntersect == None:
                        specularColor = [(specularColor[i]+light.getSpecularColor(intercept, self.camPosition)[i]) for i in range(3)]
        
        elif material.matType == TRANSPARENT:

            outside = Numpi.dotProd(rayDirection, intercept.normal) < 0

            bias = Numpi.VxE(intercept.normal, 0.001)
            

            reflect = Numpi.reflectVector(intercept.normal, [i*-1 for i in rayDirection])
            reflectOrigin =  Numpi.addV(intercept.point, bias) if outside else Numpi.substractV(intercept.point, bias)
            reflectIntercept = self.rtCastRay(reflectOrigin, reflect, None, recursion + 1)
            reflectColor = self.rtRayColor(reflectIntercept, reflect, recursion+1)
            
            for light in self.lights:
                if light.lightType != "Ambient":
                    lightDir = None
                    if light.lightType == "Directional":
                        lightDir = [(i*-1) for i in light.direction]
                    elif light.lightType == "Point":
                        lightDir = Numpi.substractV(light.point, intercept.point)
                        lightDir = Numpi.normalizeV(lightDir)
                        
                    shadowIntersect = self.rtCastRay(intercept.point, lightDir, intercept.obj)
                    
                    if shadowIntersect == None:
                        specularColor = [(specularColor[i]+light.getSpecularColor(intercept, self.camPosition)[i]) for i in range(3)]
            

            if not totalInternalReflection(intercept.normal, rayDirection, 1.0, material.ior):
                refract = reflectorVector(intercept.normal, rayDirection, 1.0, material.ior)
                refractOrigin =  Numpi.substractV(intercept.point, bias) if outside else Numpi.addV(intercept.point, bias)
                refractIntercept = self.rtCastRay(refractOrigin, refract, None, recursion + 1)
                refractColor = self.rtRayColor(refractIntercept, refract, recursion+1)

               
                kr, kt = fresnel(intercept.normal, rayDirection, 1.0, material.ior)
                reflectColor = Numpi.VxE(reflectColor, kr)
                refractColor = Numpi.VxE(refractColor, kt)
            
        lightColor = [(ambientColor[i]+diffuseColor[i]+specularColor[i]+reflectColor[i] + refractColor[i]) for i in range(3)]  
        
        finalColor = [min(1,surfaceColor[i]*lightColor[i])for i in range(3)]
        return finalColor
    
    
    def rtRender(self):
        indexes = [(i,j) for i in range(self.vpWidth) for j in range(self.vpHeight)]
        random.shuffle(indexes)
        
        for i,j in indexes:
            x = i+self.vpX
            y = j+self.vpY
            if (0<=x<self.width) and (0<=y<self.height):
              
                pX = ((x+0.5-self.vpX)/self.vpWidth)*2-1
                pY = ((y+0.5-self.vpY)/self.vpHeight)*2-1
                
                pX*=self.rightEdge
                pY*=self.topEdge
                
                direction = (pX,pY,-self.nearPlane)
                direction = Numpi.normalizeV(direction)
                
                intercept = self.rtCastRay(self.camPosition, direction)
                rayColor = self.rtRayColor(intercept, direction)
                    
                if rayColor != None: 
                    self.rtPoint(x,y,rayColor)
                    pygame.display.flip()