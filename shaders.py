#En OpenGL, los shaders se escriben enn un
#nuevo lenguaje de programacion llamada GLSL
#Graphics Library Shader Language

vertex_shader = """
    #version 450 core
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec2 texCoords;
    layout (location = 2) in vec3 normals;
    
    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;

    uniform float time;
    
    out vec2 outTextcoords;
    out vec3 outNormals;
    
    void main() {
        
        vec3 pos = position;
        pos.y += sin(time + pos.x/2)/2; 
        
        gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos, 1.0);
        outTextcoords = texCoords;
    }
"""

fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    uniform vec3 dirLight;

    in vec2 outTextcoords;
    in vec3 outNormals;
    out vec4 fragColor;
    
    void main() {
        float intensity = dot(outNormals, -dirLight);
        fragColor = texture(tex, outTextcoords) * intensity;
    }
"""