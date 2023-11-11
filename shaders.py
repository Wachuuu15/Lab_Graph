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
    float threshold = 0.5; // Ajusta este umbral según sea necesario
    float edgeWidth = 0.01; // Ancho de los bordes

    vec3 edgeColor = vec3(0.0, 0.0, 0.0); // Color de los bordes
    vec3 baseColor = texture(tex, outTextcoords).xyz;

    float intensity = dot(outNormals, -normalize(vec3(1.0, 1.0, 1.0))); // Luz diagonal

    // Detección de bordes
    if (intensity > threshold)
    {
        float edgeFactor = fwidth(intensity);
        float outline = smoothstep(0.5 - edgeFactor, 0.5 + edgeFactor, intensity);
        fragColor = vec4(mix(baseColor, edgeColor, outline), 1.0);
    }
    else
    {
        fragColor = vec4(baseColor, 1.0);
    }
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

    // Simulamos estrellas
    vec2 starCoords = fract(outTextcoords * 100.0); // Ajusta el valor 100.0 según sea necesario para la frecuencia de las estrellas
    float starIntensity = smoothstep(0.98, 1.0, length(starCoords - vec2(0.5))); // Ajusta el valor 0.98 según sea necesario para el brillo de las estrellas

    // Combinamos el color base con el efecto de estrellas
    vec3 finalColor = mix(baseColor, vec3(1.0), starIntensity); // Color blanco para las estrellas

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