OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material(object):

#determina como se comporta la luz cuando le pega a una superficie    
     def __init__(self, diffuse=(1, 1, 1), spec=1.0, ks=0.0, ior=1.0, texture=None, matType=OPAQUE, neon_colors=None, neon_intensities=None):
        self.diffuse = diffuse
        self.spec = spec
        self.ks = ks
        self.ior = ior
        self.matType = matType
        self.texture = texture
        self.neon_colors = neon_colors if neon_colors else []
        self.neon_intensities = neon_intensities if neon_intensities else []