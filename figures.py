import numpi
from math import tan, pi, atan2, acos

class Intercept(object):
    def __init__(self, distance, point, texcoords, normal, obj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.obj = obj


class Shape(object):
    def __init__(self, position, material):
        self.position = position  # Cambio positon a position
        self.material = material

    def ray_intersect(self, orig, dir):
        return None


class Sphere(Shape):
    def __init__(self,position,radius, material):
        self.radius = radius
        super().__init__(position, material)

    def ray_intersect(self, orig, dir):
        L = numpi.subtract_arrays(self.positon, orig)
        lengthL = numpi.magV(L)
        tca = numpi.dot_product(L, dir)
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

        P = numpi.add_arrays(orig,numpi.multiply_scalar_array(t0,dir))
        normal = numpi.subtract_arrays(P,self.positon)
        normal = numpi.normalizeV(normal)

        u = (atan2(normal[2],normal[0])/(2*pi))+0.5
        v = acos(normal[1])/pi

        return Intercept(distance = t0,
                         point= P,
                         normal = normal,
                         texcoords=(u,v),
                         obj = self)
    
class Plane(Shape):
    def __init__(self, position, normal, material):
        self.normal = numpi.normalizeV(normal)
        super().__init__(position, material)
    
    def ray_intersect(self, orig, dir):
        #Distancia = (planePos - origRay) o normal) / (dirRay o normal)
        
        denom = numpi.dot_product(dir, self.normal)
        
        if abs(denom) <= 0.0001:
            return None
        
        num = numpi.dot_product(numpi.subtract_arrays(self.position, orig), self.normal)
        t = num/denom
        
        if t<0:
            return None
        
        #P = O+D*t0
        p = numpi.add_arrays(orig, numpi.multiply_scalar_array(t,dir))
        
        
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
        
        contactDistance = numpi.subtract_arrays(planeIntersect.point, self.position)
        contactDistance = numpi.magV(contactDistance)
        
        if contactDistance > self.radius:
            return None
        
        return Intercept(distance = planeIntersect.distance,
                         point = planeIntersect.point,
                         normal = self.normal,
                         texcoords= None,
                         obj = self)

class AABB(Shape):
    # Axis Align Boundng Box    
    #En Minecraft, los cubos solo tienen posicion; ni escala, ni rotacion.
    
    def __init__(self, position, size, material):
        self.size = size
        super().__init__(position, material)
        
        self.planes=[]

        self.lenghts= size
        # self.lenghtX = size[0]
        # self.lenghtY = size[1]
        # self.lenghtZ = size[2]

        #sides
        leftPlane = Plane(numpi.add_arrays(self.position,[-size[0]/2,0,0]),(-1,0,0),material)
        rightPlane = Plane(numpi.add_arrays(self.position,[size[0]/2,0,0]),(1,0,0),material)
        
        bottomPlane = Plane(numpi.add_arrays(self.position,[0,-size[1]/2,0]),(0,-1,0),material)
        topPlane = Plane(numpi.add_arrays(self.position,[0,size[1]/2,0]),(0,1,0),material)
    
        backPlane = Plane(numpi.add_arrays(self.position,[0,0,-size[2]/2]),(0,0,-1),material)
        frontPlane = Plane(numpi.add_arrays(self.position,[0,0,size[2]/2]),(0,0,1),material)
        
        self.planes.append(leftPlane)
        self.planes.append(rightPlane)
        self.planes.append(bottomPlane)
        self.planes.append(topPlane)
        self.planes.append(backPlane)
        self.planes.append(frontPlane)
        
        #Bounds
        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]
        
        bias = 0.001
        
        for i in range(3):
            self.boundsMin[i] = self.position[i]-(bias+size[i]/2)
            self.boundsMax[i] = self.position[i]+(bias+size[i]/2)
            
    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')
        
        u = 0
        v = 0
        
        for plane in self.planes:
            planeIntersect = plane.ray_intersect(orig,dir)
            
            if planeIntersect is not None:
                planePoint = planeIntersect.point
                if self.boundsMin[0]<planePoint[0]<self.boundsMax[0]:
                    if self.boundsMin[1]<planePoint[1]<self.boundsMax[1]:
                        if self.boundsMin[2]<planePoint[2]<self.boundsMax[2]:
                            if planeIntersect.distance<t:
                                t = planeIntersect.distance
                                intersect = planeIntersect
                                
                                #Generar las uvs
                                if abs(plane.normal[0])>0:
                                    #Estoy en X, usamos Y y Z para crear las uvs
                                    u = (planePoint[1]-self.boundsMin[1])/(self.size[1]+0.002)
                                    v = (planePoint[2]-self.boundsMin[2])/(self.size[2]+0.002)
                                elif abs(plane.normal[1])>0:
                                    #Estoy en Y, usamos X y Z para crear las uvs
                                    u = (planePoint[0]-self.boundsMin[0])/(self.size[0]+0.002)
                                    v = (planePoint[2]-self.boundsMin[2])/(self.size[2]+0.002)
                                elif abs(plane.normal[2])>0:
                                    #Estoy en Z, usamos X y Y para crear las uvs
                                    u = (planePoint[0]-self.boundsMin[0])/(self.size[0]+0.002)
                                    v = (planePoint[1]-self.boundsMin[1])/(self.size[1]+0.002)

                                    
                                
        if intersect is None:
            return None
        
        return Intercept(distance=t,
                         point=intersect.point,
                         normal=intersect.normal,
                         texcoords=(u,v),
                         obj=self)
    