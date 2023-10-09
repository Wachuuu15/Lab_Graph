import numpi as Numpi
import numpy as np
from math import tan, pi, atan2, acos

class Intercept(object):
    def __init__(self, distance, point, texcoords, normal, obj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.obj = obj


class Shape(object):
    def __init__(self, positon, material):
        self.positon = positon
        self.material = material


    def ray_intersect(self,orig,dir):
        return None
    
class Sphere(Shape):
    def __init__(self,position,radius, material):
        self.radius = radius
        super().__init__(position, material)

    def ray_intersect(self, orig, dir):
        L = np.subtract(self.positon, orig)
        lengthL = np.linalg.norm(L)
        tca = np.dot(L, dir)
        d = (lengthL ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None
        
        thc = (self.radius * 2 -d * 2) **0.5
        
        t0 = tca - thc
        t1 = tca + thc
    
        if t0 < 0:
            t0 =t1
            
        if t0 < 0:
            return None
        # P = O + D *t0

        P = np.add(orig, t0 * np.array(dir))
        normal = np.subtract(P,self.positon)
        normal = normal/np.linalg.norm(normal)

        return Intercept(distance = t0,
                         point= P,
                         normal = normal,
                         obj = self)
    
class Plane(Shape):
    def __init__(self, position, normal, material):
        self.normal = normal/np.linalg.norm(normal)
        super().__init__(position, material)
    
    def ray_intersect(self, orig, dir):
        #Distancia = (planePos - origRay) o normal) / (dirRay o normal)
        
        denom = np.dot(dir, self.normal)
        
        if abs(denom) <= 0.0001:
            return None
        
        num = np.dot(np.subtract(self.position, orig), self.normal)
        t = num/denom
        
        if t<0:
            return None
        
        #P = O+D*t0
        p = np.add(orig, t*np.array(dir))
        
        return Intercept(distance = t,
                         point = p,
                         normal = self.normal,
                         texcoords= None,
                         obj = self)

class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        self.radius = radius
        super().__init__(position, normal, material)
    
    def ray_intersect(self, orig, dir):
        planeIntersect = super().ray_intersect(orig, dir)
        
        if planeIntersect is None:
            return None
        
        contactDistance = np.subtract(planeIntersect.point, self.position)
        contactDistance = np.linalg.norm(contactDistance)
        
        if contactDistance > self.radius:
            return None
        
        return Intercept(distance = planeIntersect.distance,
                         point = planeIntersect.point,
                         normal = self.normal,
                         texcoords= None,
                         obj = self)

class AABB(Shape):    
    #En Minecraft, los cubos solo tienen posicion; ni escala, ni rotacion.
    
    def __init__(self, position, size, material):
        self.size = size
        super().__init__(position, material)
        
        self.planes=[]
        self.lenghtX = size[0]
        self.lenghtY = size[1]
        self.lenghtZ = size[2]
    