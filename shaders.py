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
        gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position,1.0);
        outTextcoords = texCoords;

    }
"""

fat_vertex_shader = """
#version 450 core
layout (location=0) in vec3 position;
layout (location=1) in vec2 texCoords;
layout (location=2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float fatness;

out vec2 outTextcoords;
out vec3 outNormals;

void main()
{
    outNormals  =(modelMatrix*vec4(normals,0.0)).xyz;
    outNormals = normalize(outNormals);
    vec3 pos = position+(fatness/4)*outNormals;
    
    gl_Position = projectionMatrix*viewMatrix*modelMatrix*vec4(pos,1.0);
    outTextcoords = texCoords;
}
"""
toon_shader = """
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 outTextcoords;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals,-dirLight);
    if (intensity<0.33)
        intensity=0.2;
    else if (intensity<0.66)
        intensity=0.6;
    else
        intensity=1.0;
    fragColor = texture(tex,outTextcoords)*intensity;
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