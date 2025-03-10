#Laioneall Williams
#23-EISN-2-035
import pygame as pg              # Importamos la librería pygame como pg
from settings import *           # Importamos todas las constantes y configuraciones desde settings.py


class ObjectRenderer:
    """
    Clase que se encarga de dibujar y renderizar los elementos gráficos en pantalla:
    - Fondo (cielo y piso)
    - Paredes (texturas)
    - Objetos y sprites en la escena
    - Interfaz (barra de vida, mensajes de victoria o game over, etc.)
    """
    def __init__(self, game):
        self.game = game                      # Referencia al objeto principal del juego
        self.screen = game.screen            # Referencia a la superficie donde se dibuja todo
        self.wall_textures = self.load_wall_textures()  
        """
        Diccionario con las texturas de paredes. Cada llave (1, 2, 3, etc.) asocia 
        un número con la textura correspondiente en el mapa.
        """

        # Carga y ajusta la imagen del cielo, escalándola al ancho de la ventana y la mitad de la altura
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0  # Controla el desplazamiento del fondo para simular rotación

        # Pantalla rojiza que se muestra cuando el jugador recibe daño
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)

        # Configuración para dibujar los dígitos de la salud del jugador
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        """
        Cargamos imágenes para los dígitos del 0 al 10. 
        El 10 se suele usar como el símbolo '%' o algo parecido, dependiendo del diseño original.
        """
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        """
        Creamos un diccionario para acceder a cada dígito por su cadena de texto 
        (ej. '0': imagen, '1': imagen, ..., '10': imagen).
        """

        # Pantallas de Game Over y Victoria
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)

    def draw(self):
        """
        Método principal para dibujar todo en la pantalla: 
        - Dibuja el fondo (cielo y piso)
        - Renderiza objetos del juego (paredes, sprites, etc.)
        - Dibuja la salud del jugador
        """
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def win(self):
        """
        Muestra la imagen de victoria en pantalla completa.
        """
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        """
        Muestra la imagen de Game Over en pantalla completa.
        """
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        """
        Dibuja la salud del jugador en la esquina superior izquierda usando los dígitos cargados.
        El bucle recorre cada carácter de la salud (ej. '100') para colocar los dígitos uno tras otro.
        Después de la salud dibuja el dígito '10', que podría ser un símbolo como '%' o un icono.
        """
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        # Dibuja el dígito '10' a continuación, puede representar un símbolo de porcentaje o algo similar
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        """
        Dibuja en pantalla una capa roja que indica que el jugador ha recibido daño.
        """
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        """
        Dibuja el cielo y el piso:
        - El cielo se repite horizontalmente para simular rotación según el ángulo del jugador.
        - El piso se dibuja simplemente como un rectángulo de color sólido.
        """
        # Actualiza el desplazamiento del cielo según la rotación relativa del jugador
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH

        # Dibuja la imagen del cielo dos veces seguidas para crear el efecto de horizonte continuo
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))

        # Dibuja el piso como un rectángulo de color FLOOR_COLOR
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        """
        Renderiza los objetos en la escena:
        - La lista de objetos a renderizar se ordena por profundidad (depth) en orden descendente.
        - Se dibujan en la pantalla las imágenes en la posición calculada.
        """
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        """
        Carga una textura desde la ruta especificada y la escala al tamaño (res) indicado.
        Retorna el objeto Surface resultante.
        """
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        """
        Carga y devuelve un diccionario con las texturas de las paredes.
        Las llaves (1, 2, 3, 4, 5, ...) representan identificadores de texturas.
        """
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }
