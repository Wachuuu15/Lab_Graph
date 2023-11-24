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

resalt_shader = """
#version 450 core

layout (binding=0) uniform sampler2D tex;

in vec2 outTextcoords;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    // Obtenemos el color base de la textura
    vec3 baseColor = texture(tex, outTextcoords).xyz;

    // Simulamos un efecto de fractales
    float scale = 10.0; // Ajusta la escala de los fractales según sea necesario
    vec2 fractalCoords = outTextcoords * scale;
    float fractalIntensity = sin(fractalCoords.x) * cos(fractalCoords.y);

    // Aplicamos el efecto de fractales al color base
    vec3 finalColor = baseColor + vec3(fractalIntensity);

    fragColor = vec4(finalColor, 1.0);
}


"""

manchas_shader = """
#version 450 core

layout (binding=0) uniform sampler2D tex;

in vec2 outTextcoords;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    // Obtenemos el color base de la textura
    vec3 baseColor = texture(tex, outTextcoords).xyz;

    // Añadimos un patrón de manchas de colores
    vec2 patternCoords = mod(outTextcoords * 20.0, 1.0); // Ajusta el valor de 20.0 según sea necesario para la frecuencia del patrón
    vec3 patternColor = vec3(patternCoords, 1.0);

    // Combinamos el color base con el patrón
    vec3 finalColor = baseColor + 0.2 * patternColor; // Ajusta el valor 0.2 para controlar la intensidad de las manchas

    fragColor = vec4(finalColor, 1.0);
}

"""

stars_shader = """
#version 450 core

layout (binding=0) uniform sampler2D tex;

in vec2 outTextcoords;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    // Obtenemos el color base de la textura
    vec3 baseColor = texture(tex, outTextcoords).xyz;

    // Calculamos las coordenadas radiales
    vec2 radialCoords = outTextcoords - 0.5;
    float distance = length(radialCoords);

    // Creamos un patrón de ondas concéntricas
    float waveIntensity = 0.5 + 0.5 * sin(distance * 20.0); // Ajusta la frecuencia de las ondas según sea necesario

    // Combinamos el color base con el patrón de ondas
    vec3 finalColor = baseColor + waveIntensity;

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

fire_shader = """
#version 450 core

layout (binding=0) uniform sampler2D tex;

in vec2 outTextcoords;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    // Obtenemos el color base de la textura
    vec3 baseColor = texture(tex, outTextcoords).xyz;

    // Simulamos un efecto de fuego o calor
    float fireIntensity = 0.5 + 0.5 * sin(outTextcoords.y * 20.0); // Ajusta la frecuencia del efecto de fuego

    // Aplicamos el efecto de fuego al color base
    vec3 finalColor = baseColor + vec3(1.0, 0.5, 0.0) * fireIntensity; // Color naranja para el fuego

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

void main()
{
    gl_Position = projectionMatrix  * viewMatrix * vec4(inPosition,1.0);
}

"""

skybox_fragment_shader = """

#version 450

out vec4 fragColor;

void main()
{
    fragColor = vec4(1,1,1,1);
}

"""