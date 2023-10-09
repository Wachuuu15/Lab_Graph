import numpi as Numpi
from math import acos, asin


def reflectVector(normal,direction):
    reflect = 2*Numpi.dot_product(normal,direction)
    reflect = Numpi.multiply_scalar_array(reflect,normal)
    reflect = Numpi.subtract_arrays(reflect,direction)
    reflect = Numpi.normalizeV(reflect)
    
    return reflect

def refractVector(normal,incident,n1,n2):
    #Snell's Law
    c1 = Numpi.dot_product(normal,incident)
    if c1<0:
        c1=-c1
    else:
        normal = Numpi.deny_array(normal)
        n1,n2=n2,n1
    
    n = n1/n2
    
    T = Numpi.subtract_arrays(Numpi.multiply_scalar_array(n,(Numpi.add_arrays(incident,Numpi.multiply_scalar_array(c1,normal)))),Numpi.multiply_scalar_array((1-n**2*(1-c1**2))**0.5,normal))
    T = Numpi.normalizeV(T)
    return T


def totalInternalReflection(normal, incident, n1, n2):
    c1 = Numpi.dot_product(normal, incident)
    
    if c1 < 0:
        c1 = -c1
    else: 
        n1, n2 = n2, n1
    
    if n1 < n2:
        return False
    
    theta1 = acos(c1)
    thetaC = asin(n2/n1)
    
    return theta1 >= thetaC

def fresnel(normal, incident, n1, n2):
    c1 = Numpi.dot_product(normal, incident)
    
    if c1 < 0:
        c1 = -c1
    else: 
        n1, n2 = n2, n1
    
    s2 = (n1*(1-c1**2)**0.5)/n2
    c2 = (1-s2**2)**0.5
    
    f1 = (((n2*c1) - (n1*c2)) / ((n2*c1) + (n1*c2)))**2
    f2 = (((n1*c2) - (n2*c1)) / ((n1*c2) + (n2*c1)))**2
    
    kr = (f1+f2)/2
    kt = 1 - kr
    
    return kr, kt


class Light(object):
    def __init__(self, intensity= 1, color = (1,1,1), lightType = "None"):
        self.intensity = intensity
        self.color = color
        self.lightType = lightType 

    def getLightColor(self):
        return[self.color[0] * self.intensity,
               self.color[1] * self.intensity,
               self.color[2] * self.intensity]

    def getDiffuseColor(self,intercept):
        return self.getLightColor()
    
    def getSpecularColor(self,intercept, viewPos):
        return None

class AmbientLight(Light):
    def __init__(self, intensity = 1, color = (1,0,0)):
        super().__init__(intensity,color,"Ambient") 

class DirectionalLight(Light):
    def __init__(self, direction=(0,-1,0), intensity = 1,color=(1, 1, 1)):
        self.direction=Numpi.normalizeV(direction)
        super().__init__(intensity, color, "Directional")

    def getDiffuseColor(self, intercept):
        dir = [(i* -1) for i in self.direction]
        intensity = Numpi.dot_product(intercept.normal, dir) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks
        
        return  [(i * intensity) for i in self.color]

    def getSpecularColor(self, intercept, viewPos):
        dir =[(i*-1) for i in self.direction]
        reflect = Numpi.reflectVector(intercept.normal, dir)
        
        viewDir = Numpi.subtract_arrays(viewPos,intercept.point)
        viewDir = Numpi.normalizeV(viewDir)
        
        #Cambia dependiendo de la superficie
        specIntensity = max(0, Numpi.dot_product(viewDir, reflect))** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity
        
        specColor = [(i*specIntensity) for i in self.color]
        
        return specColor

class PointLight(Light):
    def __init__(self, point = (0,0,0), intensity = 1, color = (1,1,1)):
        self.point = point
        super().__init__(intensity, color, "Point")
        
    def getDiffuseColor(self, intercept):
        dir = Numpi.subtract_arrays(self.point, intercept.point)
        R = Numpi.magV(dir)
        dir = Numpi.divide_array_scalar(dir,R)
        
        intensity = Numpi.dot_product(intercept.normal, dir) * self.intensity
        intensity *= 1 - intercept.obj.material.ks
        
        #Ley de cuadrados inversos
        #If = intensity/R**2
        #R: distancia del punto intercepto a la luz punto.
        
        if R!=0:
            intensity /= R**2
        intensity = max(0, min(1, intensity))

        
        diffuseColor = [(i*intensity) for i in self.color]
        
        return diffuseColor
    
    def getSpecularColor(self, intercept, viewPos):
        dir = Numpi.subtract_arrays(self.point, intercept.point)
        R = Numpi.magV(dir)
        dir = Numpi.normalizeV(dir)
        
        reflect = Numpi.reflectVector(intercept.normal, dir)
        
        viewDir = Numpi.subtract_arrays(viewPos,intercept.point)
        viewDir = Numpi.normalizeV(viewDir)
        
        specIntensity = max(0, Numpi.dot_product(viewDir, reflect))** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity
        
        if R!=0:
            specIntensity /= R**2
            
        specIntensity = max(0, min(1, specIntensity))
        
        specColor = [(i*specIntensity) for i in self.color]
        
        return specColor
    