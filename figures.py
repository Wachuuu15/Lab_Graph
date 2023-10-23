import numpi
from math import tan, pi, atan2, acos, sqrt


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
        L = numpi.subtract_arrays(self.position, orig)
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
        normal = numpi.subtract_arrays(P,self.position)
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
    
# class Donut
class Cylinder(Shape):
    def __init__(self, position, radius, height, material):
        self.radius = radius
        self.height = height
        super().__init__(position, material)
        self.top_disk = Disk(numpi.add_arrays(position, [0, height / 2, 0]), [0, 1, 0], radius, material)
        self.bottom_disk = Disk(numpi.add_arrays(position, [0, -height / 2, 0]), [0, -1, 0], radius, material)

    def ray_intersect(self, orig, dir):
        a = dir[0] ** 2 + dir[2] ** 2
        b = 2 * (orig[0] * dir[0] + orig[2] * dir[2] - self.position[0] * dir[0] - self.position[2] * dir[2])
        c = (orig[0] - self.position[0]) ** 2 + (orig[2] - self.position[2]) ** 2 - self.radius ** 2

        delta = b ** 2 - 4 * a * c

        if delta < 0:
            return None

        t0 = (-b + sqrt(delta)) / (2 * a)
        t1 = (-b - sqrt(delta)) / (2 * a)

        t = min(t0, t1)

        if t < 0:
            return None

        point = numpi.add_arrays(orig, numpi.multiply_scalar_array(t, dir))

        if point[1] < self.position[1] - self.height / 2 or point[1] > self.position[1] + self.height / 2:
            return None

        normal = list(numpi.subtract_arrays(point, self.position))
        normal[1] = 0
        normal = numpi.normalizeV(normal)


        u = (atan2(normal[2], normal[0]) / (2 * pi)) + 0.5
        v = (point[1] - self.position[1] + self.height / 2) / self.height

        return Intercept(distance=t,
                         point=point,
                         normal=normal,
                         texcoords=(u, v),
                         obj=self)


#oval
class Oval(Shape):
    def __init__(self, position, radius, material):
        self.radius = radius
        super().__init__(position, material)

    def ray_intersect(self, orig, dir):
        l = numpi.vecResta(orig,self.position)
        l = numpi.vecDiv(l,self.radius)

        a = numpi.doti(dir,dir)
        b = 2.0 * numpi.doti(dir,l)
        c = numpi.doti(l, l) - 1.0

        dis = (b**2) - (4*a*c)

        if dis < 0:
            return None
        
        t1 = (-b + sqrt(dis)) / (2 * a)
        t2 = (-b - sqrt(dis)) / (2 * a)
        
        if t1 < 0 and t2 <0:
            return None
        
        if t1 < t2:
            t = t1
        else:
            t = t2
            
        p = numpi.vecAdd(orig, numpi.VxE(dir, t))
        
        normal = numpi.vecResta(p, self.position)
        normal = numpi.vecDiv(normal, self.radius)
        normal = numpi.normalizeV(normal)
        
        u = 1-((atan2(normal[2], normal[0])+pi)/(2*pi))
        v = ((acos(normal[1])+pi)/2)/pi
        
        return Intercept(distance = t,
                         point = p,
                         normal = normal,
                         texcoords= (u,v),
                         obj = self)


#triangle 3d
class Triangle(Shape):
    def __init__(self, vertices, material):
        self.vertices = vertices
        #super().__init__(position, material)
        v0 = numpi.subtract_arrays(self.vertices[1], self.vertices[0])
        v1 = numpi.subtract_arrays(self.vertices[2],self.vertices[0])
        self.normal = numpi.normalizeV(numpi.crossProduct(v0,v1))

        #
        x = (vertices[0][0] + vertices[1][0]+vertices[2][0])/3
        y = (vertices[0][1] + vertices[1][1]+vertices[2][1])/3
        z = (vertices[0][2] + vertices[1][2]+vertices[2][2])/3

        super().__init__((x,y,z), material)

    def ray_intersect(self, orig, dir):
        #The Ray And The Triangle Are Parallel
        denom = numpi.dot_product(dir, self.normal)
                
        if abs(denom)<=0.0001:
            return None
        
        d = -1*numpi.dot_product(self.normal,self.vertices[0])
        num = -1*(numpi.dot_product(self.normal,orig)+d)
        t = num/denom

        if t<0:
            return None
        
        P = numpi.add_arrays(orig,numpi.multiply_scalar_array(t,dir))

        #test if the dot product of the vector along the edge and the vector defined by the first vertex of the tested edge
        #edge 0
        edge0 = numpi.subtract_arrays(self.vertices[1],self.vertices[0]) #v1 - v0; 
        vp0 = numpi.subtract_arrays(P,self.vertices[0]) #Vec3f vp0 = P - v0;
        C = numpi.crossProduct(edge0,vp0);
        if numpi.dot_product(self.normal,C)<0: #if (N.dotProduct(C) < 0) return false; P is on the right side
            return None
        
        #edge 1
        edge1 = numpi.subtract_arrays(self.vertices[2], self.vertices[1])    #Vec3f edge1 = v2 - v1; 
        vp1 = numpi.subtract_arrays(P, self.vertices[1])    #Vec3f vp1 = P - v1;
        C = numpi.crossProduct(edge1,vp1);
        if numpi.dot_product(self.normal, C)<0:    #if (N.dotProduct(C) < 0)  return false; // P is on the right side
            return None
    
        #edge 2
        edge2 = numpi.subtract_arrays(self.vertices[0],self.vertices[2]) #v0 - v2; 
        vp2 = numpi.subtract_arrays(P,self.vertices[2]) #Vec3f vp2 = P - v2;
        C = numpi.crossProduct(edge2,vp2);
        if numpi.dot_product(self.normal, C)<0:   #if (N.dotProduct(C) < 0) return false; // P is on the right side;
            return None 
        
        u,v,w = numpi.barycentricCoords(self.vertices[0],self.vertices[1],self.vertices[2],P)

        
        return Intercept(distance=t,
                         point=P,
                         normal=self.normal,
                         texcoords=(u,v),
                         obj=self)  