#Laioneall Williams
#23-EISN-2-035
from sprite_object import *

class Weapon(AnimatedSprite):
    """
    Clase que representa el arma del jugador (ej. escopeta).
    Hereda de AnimatedSprite para manejar las imágenes de animación 
    (cuando dispara y vuelve a su posición inicial).
    """
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):
        # Inicializa la clase padre AnimatedSprite
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)

        # Reescalado de todas las imágenes del arma
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images]
        )

        # Posición donde se dibuja el arma en la pantalla (parte inferior, centrada horizontalmente)
        self.weapon_pos = (
            HALF_WIDTH - self.images[0].get_width() // 2,
            HEIGHT - self.images[0].get_height()
        )

        # Bandera que indica si el arma está recargando (animación de disparo en progreso)
        self.reloading = False

        # Total de cuadros (frames) en la animación de disparo
        self.num_images = len(self.images)

        # Contador para rastrear el frame actual de la animación
        self.frame_counter = 0

        # Daño que el arma ocasiona a los enemigos o al ambiente
        self.damage = 50

    def animate_shot(self):
        """
        Maneja la animación de disparo:
        - Mientras self.reloading es True, rota las imágenes para simular la acción de disparar.
        - Una vez se completan los fotogramas, se detiene la recarga (disparo).
        """
        if self.reloading:
            # Desactiva el disparo del jugador mientras dura la animación
            self.game.player.shot = False

            # Si es momento de cambiar de imagen
            if self.animation_trigger:
                # Pasa a la siguiente imagen en la cola
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1

                # Si se han reproducido todos los fotogramas de la animación
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        """
        Dibuja el arma en pantalla, usando la imagen de la parte frontal de la cola 'images'.
        Se coloca en la posición weapon_pos.
        """
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        """
        Se llama en cada frame del juego:
        - Verifica si es tiempo de cambiar de imagen (check_animation_time).
        - Ejecuta la animación del disparo si el arma está en recarga.
        """
        self.check_animation_time()
        self.animate_shot()
