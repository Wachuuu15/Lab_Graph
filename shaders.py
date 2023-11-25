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
        outNormals = (modelMatrix * vec4(normals, 0.0)).xyz;

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

water_shader = """
#version 450 core

layout (binding=0) uniform sampler2D tex; // Textura base del agua
layout (binding=1) uniform sampler2D normalMap; // Mapa normal para el agua
uniform float time;

in vec2 outTextcoords;
in vec3 outNormals;

out vec4 fragColor;

float noise(vec2 pos) {
    return fract(sin(dot(pos, vec2(12.9898,78.233))) * 43758.5453);
}

void main() {
    // Color base azul para el agua
    vec3 baseColor = vec3(0.0, 0.5, 0.7); 

    // Coordenadas de textura distorsionadas para simular movimiento
    float waveSpeed = 0.2;
    vec2 distortedCoords = outTextcoords + vec2(noise(outTextcoords + time * waveSpeed), noise(outTextcoords - time * waveSpeed)) * 0.01;
    
    // Simular el movimiento del agua utilizando el mapa normal
    vec3 normal = texture(normalMap, distortedCoords).xyz * 2.0 - 1.0;
    vec3 lightDir = normalize(vec3(0.0, 1.0, 1.0)); // Dirección de la luz

    // Iluminación difusa
    float diff = max(dot(normal, lightDir), 0.0);

    // Iluminación especular
    float specularStrength = 0.5;
    vec3 viewDir = normalize(vec3(-outTextcoords, 1.0)); // Dirección de la vista
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * vec3(0.0, 0.5, 0.7); // Color especular azulado

    // Combinación del color de base con la iluminación
    vec3 finalColor = baseColor * diff + specular;

    fragColor = vec4(finalColor, 1.0);
}

"""

manchas_shader = """
#version 450 core

layout (binding=0) uniform sampler2D tex;

in vec2 outTextcoords;
in vec3 outNormals;

out vec4 fragColor;
uniform float time;


void main()
{
    vec3 baseColor = texture(tex, outTextcoords).xyz;
    vec2 movingCoords = outTextcoords + vec2(sin(time), cos(time)) * 0.01; // Movimiento de las manchas
    vec2 patternCoords = mod(movingCoords * 20.0, 1.0);
    
    vec3 finalColor = mix(baseColor, vec3(patternCoords, 1.0), 0.2);
    fragColor = vec4(finalColor, 1.0);
}

"""

stars_shader = """
#version 450 core

layout (binding=0) uniform sampler2D tex;
layout (binding=1) uniform sampler2D normalMap; // Mapa normal
uniform float time;
uniform vec3 lightDir; // Dirección de la luz

in vec2 outTextcoords;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    vec3 baseColor = texture(tex, outTextcoords).xyz;
    vec3 normal = texture(normalMap, outTextcoords).xyz * 2.0 - 1.0; // Normaliza el mapa normal

    vec2 radialCoords = outTextcoords - 0.5;
    float distance = length(radialCoords);

    // Iluminación difusa
    float diff = max(dot(normal, lightDir), 0.0);
    
    // Intensidad de las estrellas
    float waveIntensity = 0.5 + 0.5 * sin(distance * 20.0 + time);
    
    vec3 starColor = vec3(1.0, 1.0, 1.0);
    vec3 finalColor = mix(baseColor * diff, starColor, waveIntensity);

    fragColor = vec4(finalColor, 1.0);
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
    float intensity = dot(outNormals, -dirLight);
    vec4 color = texture(tex, outTextcoords);
    
    if (intensity > 0.95) 
        intensity = 1.0;
    else if (intensity > 0.5) 
        intensity = 0.7;
    else if (intensity > 0.25) 
        intensity = 0.4;
    else 
        intensity = 0.2;

    color.xyz *= intensity;

    fragColor = color;
}

"""

fire_shader = """
#version 450 core

layout (binding=0) uniform sampler2D tex;
uniform float time;

in vec2 outTextcoords;
in vec3 outNormals;

out vec4 fragColor;

float noise(vec2 pos) {
    // Función de ruido simple para simular la turbulencia
    return fract(sin(dot(pos, vec2(12.9898,78.233))) * 43758.5453);
}

void main() {
    vec3 baseColor = texture(tex, outTextcoords).xyz;

    // Coordenadas con "ruido" para simular el movimiento de las llamas
    vec2 noiseCoords = outTextcoords + vec2(noise(outTextcoords + time * 0.7), time * 0.4);
    float fireIntensity = noise(noiseCoords);

    // Color y brillo del fuego
    vec3 fireColor = vec3(1.0, 0.3, 0.0) + vec3(0.8, 0.2, 0.0) * fireIntensity;
    fireColor *= 1.5 - length(2.0 * outTextcoords - 1.0); // Disminuye la intensidad hacia los bordes

    // Combinación del color de fuego con el color base
    vec3 finalColor = mix(baseColor, fireColor, fireIntensity);

    fragColor = vec4(finalColor, 1.0);
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
    fragColor = texture(tex, outTextcoords) * (intensity*3);
}

"""
skybox_vertex_shader = """
#version 450 core
layout( location = 0) in vec3 inPosition;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec3 texCoords;

void main()
{
    texCoords = inPosition;
    gl_Position = projectionMatrix  * viewMatrix * vec4(inPosition,1.0);
}

"""

skybox_fragment_shader = """

#version 450

uniform samplerCube skybox;

in vec3 texCoords;
out vec4 fragColor;

void main()
{
    fragColor = texture(skybox, texCoords);
}

"""