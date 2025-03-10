#Laioneall Williams
#23-EISN-2-035
import pygame as pg
import math
from settings import *

class RayCasting:
    """
    Clase encargada de implementar el algoritmo de ray casting.
    - Calcula la distancia del jugador a las paredes en cada rayo.
    - Genera los datos necesarios para renderizar la pared con la textura correspondiente.
    """
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []   # Almacena (depth, height, texture, offset) de cada rayo
        self.objects_to_render = []    # Lista de objetos (paredes) con su profundidad y superficie lista para dibujar
        self.textures = self.game.object_renderer.wall_textures  # Diccionario de texturas cargadas

    def get_objects_to_render(self):
        """
        Convierte los resultados del ray casting (self.ray_casting_result) 
        en columnas de pared escaladas para dibujarlas en la pantalla.
        """
        self.objects_to_render = []
        
        # Recorre cada rayo y sus valores (depth, height, texture, offset)
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            # Si la altura proyectada es menor que la altura total de la ventana
            # se escala la pared a proj_height y se alinea verticalmente
            if proj_height < HEIGHT:
                # Se extrae una columna de la textura, usando 'offset' para elegir la parte correcta de la imagen
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                # Se escala la columna de pared a la altura proyectada
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                # La posición en X se calcula multiplicando ray por SCALE
                # La posición en Y se centra en la mitad de la pantalla
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)

            else:
                # Si la altura proyectada supera la altura de la ventana,
                # entonces se recorta la textura para mostrar solo la parte que cabe
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 
                    HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, 
                    texture_height
                )
                # Se escala la columna a la altura completa de la ventana
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            # Se agrega a la lista un tupla con la profundidad, la imagen y la posición
            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        """
        Realiza el ray casting:
        - Genera NUM_RAYS rayos desde el ángulo actual del jugador.
        - Para cada rayo, calcula la intersección con paredes en vertical y horizontal.
        - Obtiene la distancia (depth) y la textura correspondiente, aplicando correctivo para el "efecto ojo de pez".
        - Almacena los resultados en self.ray_casting_result.
        """
        self.ray_casting_result = []
        # Variables para guardar la textura que se encuentra al chocar en vertical y horizontal
        texture_vert, texture_hor = 1, 1

        # Posición del jugador
        ox, oy = self.game.player.pos
        # Posición discreta (celda) del jugador en el mapa
        x_map, y_map = self.game.player.map_pos

        # Calculamos el ángulo inicial para el primer rayo
        # Restando HALF_FOV para que el campo de visión se extienda a los lados
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001

        # Recorre la cantidad de rayos especificados
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # --- Cálculo de intersecciones horizontales ---
            # Si el seno del ángulo es positivo, la primera intersección horizontal 
            # estará en y_map + 1 (abajo), si es negativo, en y_map - 1e-6 (arriba).
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            # Distancia en el eje Y hasta la primera intersección
            depth_hor = (y_hor - oy) / sin_a
            # X de la primera intersección horizontal
            x_hor = ox + depth_hor * cos_a
            # delta_depth indica cuánto se incrementa la profundidad al pasar de una intersección a la siguiente
            delta_depth = dy / sin_a
            # dx es el incremento en X para pasar de una intersección a la siguiente
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                # Si la celda es una pared, guardamos la textura correspondiente y salimos
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                # De lo contrario, seguimos avanzando a la siguiente intersección
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # --- Cálculo de intersecciones verticales ---
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                # Si la celda es una pared, guardamos la textura correspondiente y salimos
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # --- Determinamos la intersección más cercana (vertical u horizontal) ---
            # depth, texture, offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                # Normalizamos la posición vertical para hallar el offset de la textura
                y_vert %= 1
                # offset indica la fracción de la textura que se dibuja
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # Eliminamos el "efecto ojo de pez" corrigiendo la distancia 
            # en función de la diferencia de ángulo entre ray_angle y player.angle.
            depth *= math.cos(self.game.player.angle - ray_angle)

            # --- Calculamos la altura proyectada en la pantalla ---
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # Guardamos los resultados de este rayo en una lista
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            # Avanzamos al siguiente rayo aumentando el ángulo
            ray_angle += DELTA_ANGLE

    def update(self):
        """
        Llamado en cada frame:
        - Ejecuta el ray casting para obtener la información de profundidad y texturas.
        - Convierte esos resultados en objetos renderizables (columnas de pared) para dibujarlos.
        """
        self.ray_cast()
        self.get_objects_to_render()
