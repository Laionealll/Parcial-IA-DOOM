#Laioneall Williams
#23-EISN-2-035
import pygame as pg  # Importamos la librería Pygame y la renombramos como pg para abreviar

# Variable utilizada para representar un espacio vacío en el mini mapa
_ = False

# Definición del mini mapa: una lista de listas que representa la disposición de paredes (u otros elementos)
# Cada número representa un tipo de pared o elemento, mientras que False indica un espacio vacío.
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 3, 3, 3, 3, _, _, _, _, 2, 2, 2, _, _, _, _, _, _, 1],
    [1, _, _, _, _, 4, _, _, _, _, _, _, 2, _, _, _, _, _, _, 1],
    [1, _, _, _, _, 4, _, _, _, _, _, _, 2, _, _, 3, 3, 3, _, 1],
    [1, _, _, 3, 3, 3, 3, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 4, _, _, _, 4, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 3, 1, 3, 1, 1, 1, 3, _, _, 3, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 3, _, _, _, _, _, _, 1],
    [1, 1, 3, 1, 1, 1, 1, 1, 1, 3, _, _, 3, _, _, _, _, _, _, 1],
    [1, 4, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2, 2, 2, _, 1],
    [1, _, _, 2, _, _, _, _, _, 3, 4, _, 4, 3, _, 2, _, _, _, 1],
    [1, _, _, 5, _, _, _, _, _, _, 3, _, 3, _, _, 2, _, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 4, _, _, _, _, _, _, 4, _, _, 4, _, _, _, _, _, _, _, 1],
    [1, 1, 3, 3, _, _, 3, 3, 1, 3, 3, 1, 3, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 3, _, _, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 4, _, _, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, 5, _, _, _, 5, _, _, _, 5, _, _, _, 5, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]


class Map:
    def __init__(self, game):
        self.game = game  # Guarda la referencia al juego principal para acceder a la pantalla, etc.
        self.mini_map = mini_map  # Asigna el mini mapa definido anteriormente
        self.world_map = {}  # Diccionario que contendrá las coordenadas de cada elemento (pared, etc.) del mapa
        self.rows = len(self.mini_map)  # Número de filas en el mini mapa
        self.cols = len(self.mini_map[0])  # Número de columnas en el mini mapa
        self.get_map()  # Procesa el mini mapa para llenar el diccionario world_map

    def get_map(self):
        # Recorre cada fila y cada columna del mini mapa
        for j, row in enumerate(self.mini_map):  # j es el índice de la fila, row es la lista de valores
            for i, value in enumerate(row):  # i es el índice de la columna, value es el valor en esa posición
                if value:  # Si value no es False (es decir, hay un elemento en esa posición)
                    self.world_map[(i, j)] = value  # Se guarda la posición (i, j) y su valor en el diccionario

    def draw(self):
        # Dibuja un rectángulo en la pantalla del juego para cada elemento en el world_map
        # Se multiplica la posición por 100 para escalar el mini mapa a la resolución deseada
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]
