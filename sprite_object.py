#Laioneall Williams
#23-EISN-2-035
import pygame as pg
from settings import *  # Importa las constantes de configuración (WIDTH, HEIGHT, etc.)
import os
from collections import deque  # Estructura de datos para manejar animaciones (rotar imágenes)

class SpriteObject:
    """
    Representa un objeto o sprite estático en el mundo del juego.
    Puede ser cualquier elemento decorativo (por ejemplo, una vela).
    """
    def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png',
                 pos=(10.5, 3.5), scale=0.7, shift=0.27):
        # Referencia al juego principal y al jugador
        self.game = game
        self.player = game.player
        
        # Posición (x, y) en coordenadas del mundo
        self.x, self.y = pos
        
        # Carga la imagen del sprite y obtiene sus dimensiones
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.IMAGE_WIDTH // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        
        # Variables para cálculos de proyección y posición en la pantalla
        self.dx, self.dy = 0, 0        # Distancia en X e Y entre el sprite y el jugador
        self.theta = 0                # Ángulo entre el sprite y el jugador
        self.screen_x = 0             # Posición en X donde se dibuja el sprite en pantalla
        self.dist = 1                 # Distancia real al jugador
        self.norm_dist = 1            # Distancia normalizada (corregida por ángulo)
        self.sprite_half_width = 0    # Mitad del ancho proyectado del sprite

        # Parámetros de escalado y desplazamiento vertical del sprite
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        """
        Calcula y dibuja la proyección del sprite sobre la pantalla.
        Ajusta la escala y la posición en función de la distancia al jugador.
        """
        # Proyección del sprite en función de la distancia normalizada
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE

        # Ancho y alto calculados según la proporción de la imagen y la proyección
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        # Se escala la imagen original al tamaño proyectado
        image = pg.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        # Ajuste vertical del sprite (para que parezca posado en el piso o flotando)
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT

        # Cálculo de la posición donde se dibuja el sprite en la pantalla
        pos = (
            self.screen_x - self.sprite_half_width, 
            HALF_HEIGHT - proj_height // 2 + height_shift
        )

        # Se agrega la información (distancia, imagen, posición) para que el renderizador la dibuje
        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        """
        Calcula la posición relativa del sprite respecto al jugador y determina
        si es visible para posteriormente proyectarlo.
        """
        # Diferencia en X e Y entre el sprite y el jugador
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy

        # Ángulo hacia el sprite (atan2 devuelve el ángulo en radianes)
        self.theta = math.atan2(dy, dx)

        # Calcula la diferencia angular entre el sprite y la dirección del jugador
        delta = self.theta - self.player.angle

        # Ajuste para mantener el ángulo dentro de 0 a 2π y evitar saltos bruscos
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        # Convierte la diferencia angular en la posición horizontal en la "pantalla" de ray casting
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        # Distancia al jugador (hipotenusa)
        self.dist = math.hypot(dx, dy)
        
        # Ajusta la distancia con coseno del ángulo delta, para evitar el "efecto ojo de pez"
        self.norm_dist = self.dist * math.cos(delta)

        # Solo si el sprite está frente al jugador y algo cerca, se proyecta
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        """
        Se llama en cada frame para actualizar el sprite.
        Verifica su posición y, si aplica, lo proyecta en la pantalla.
        """
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    """
    Extiende SpriteObject para manejar sprites animados.
    - Usa múltiples imágenes y rota entre ellas en intervalos regulares.
    """
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120):
        # Llama al constructor de la clase base (SpriteObject)
        super().__init__(game, path, pos, scale, shift)
        
        # Tiempo entre cambios de imagen (en milisegundos)
        self.animation_time = animation_time
        
        # El path base, sin incluir el nombre de archivo final, para obtener todas las imágenes
        self.path = path.rsplit('/', 1)[0]
        
        # Carga todas las imágenes en una estructura deque para poder rotarlas
        self.images = self.get_images(self.path)
        
        # Control del tiempo transcurrido desde la última actualización de frame
        self.animation_time_prev = pg.time.get_ticks()
        
        # Indica si es momento de pasar a la siguiente imagen (se activa en check_animation_time)
        self.animation_trigger = False

    def update(self):
        """
        Sobrescribe el método update de SpriteObject:
        1. Llama al método original (para cálculos de posición y proyección).
        2. Verifica si es momento de actualizar la animación.
        3. Cambia la imagen si corresponde.
        """
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        """
        Desplaza la primera imagen del deque al final (rotación) 
        y actualiza self.image con la nueva primera posición.
        """
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        """
        Activa la bandera de animación (animation_trigger) 
        si ha transcurrido el intervalo (animation_time) desde la última vez.
        """
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        # Si pasó más del tiempo definido para cambiar de frame
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        """
        Devuelve un deque con todas las imágenes encontradas en la carpeta (path).
        Se asume que cada archivo en esa ruta es parte de la animación.
        """
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                # Carga la imagen con canal alfa (transparencia)
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
