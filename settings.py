#Laioneall Williams
#23-EISN-2-035
import math

# -------------------------------
# Ajustes generales del juego
# -------------------------------

# RES (Resolución de la ventana): establece la anchura (WIDTH) y la altura (HEIGHT) en píxeles.
RES = WIDTH, HEIGHT = 1920, 1080
# Ejemplo alternativo para resolución completa:
# RES = WIDTH, HEIGHT = 1920, 1080

# Mitades de la resolución, útiles para centrar elementos.
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

# FPS (Frames por segundo). Cuando se coloca en 0, se suele usar vsync o limitaciones del bucle principal del juego.
# Normalmente, puedes asignar un valor (ej. 60) para limitar la velocidad de refresco.
FPS = 0

# -------------------------------
# Ajustes del jugador
# -------------------------------

# Posición inicial del jugador (x, y) dentro del mini mapa.
PLAYER_POS = 1.5, 5

# Ángulo inicial del jugador (en radianes). 0 significa mirar hacia la derecha (eje positivo de las X).
PLAYER_ANGLE = 0

# Velocidad del jugador al moverse hacia delante, atrás o en diagonal.
PLAYER_SPEED = 0.004

# Velocidad de rotación del jugador al usar el teclado (si estuviese activo).
PLAYER_ROT_SPEED = 0.002

# Escalado del tamaño del jugador para comprobar colisiones (cuanto mayor sea, más "ancho" será el jugador).
PLAYER_SIZE_SCALE = 60

# Cantidad máxima de salud que puede tener el jugador.
PLAYER_MAX_HEALTH = 100

# -------------------------------
# Ajustes del ratón
# -------------------------------

# Sensibilidad del mouse para rotar la cámara. Valores más altos = rotación más rápida.
MOUSE_SENSITIVITY = 0.0003

# Desplazamiento máximo permitido en un solo frame (previene cambios bruscos de ángulo).
MOUSE_MAX_REL = 40

# Límites en la pantalla para reposicionar el mouse si sale del área de juego.
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

# -------------------------------
# Ajustes de color
# -------------------------------

# Color de relleno para el piso (R, G, B).
FLOOR_COLOR = (30, 30, 30)

# -------------------------------
# Ajustes de la cámara y raycasting
# -------------------------------

# FOV (Field of View): campo de visión del jugador. math.pi/3 equivale a 60° (apróx).
FOV = math.pi / 3

# Mitad del campo de visión.
HALF_FOV = FOV / 2

# Cantidad de rayos que se emitirán para el raycasting. 
# Se suele asociar con la resolución horizontal para obtener suficiente detalle.
NUM_RAYS = WIDTH // 2

# Mitad de la cantidad de rayos.
HALF_NUM_RAYS = NUM_RAYS // 2

# DELTA_ANGLE: separación angular entre rayo y rayo.
DELTA_ANGLE = FOV / NUM_RAYS

# Profundidad máxima del raycasting: hasta dónde "avanzar" cada rayo antes de detenerse.
MAX_DEPTH = 20

# SCREEN_DIST: distancia de proyección en la pantalla. Se basa en la geometría de FOV y la anchura de la ventana.
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)

# SCALE: escalado horizontal para cada rayo en la representación de la pared.
SCALE = WIDTH // NUM_RAYS

# -------------------------------
# Ajustes de texturas
# -------------------------------

# Tamaño de cada textura (cuadrada) en píxeles.
TEXTURE_SIZE = 256

# Mitad del tamaño de la textura, útil para cálculos de recorte o escalado.
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
