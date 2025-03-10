#Laioneall Williams
#23-EISN-2-035
import pygame as pg
from settings import *
import math

class Player:
    """
    Clase que representa al jugador en el juego.
    Maneja movimiento, disparos y colisiones.
    """
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = 700
        self.time_prev = pg.time.get_ticks()
        self.diag_move_corr = 1 / math.sqrt(2)

    def recover_health(self):
        """Recupera salud automáticamente cada cierto tiempo."""
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        """Verifica si ha transcurrido suficiente tiempo para recuperar salud."""
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def get_damage(self, damage):
        """Aplica daño al jugador y reproduce sonidos de dolor."""
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()

    def single_fire_event(self, event):
        """Detecta si el jugador dispara con el mouse."""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

    def movement(self):
        """Controla el movimiento con teclado (W, A, S, D)."""
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0

        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1
        
        if keys[pg.K_w]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            num_key_pressed += 1
            dx -= speed_cos
            dy -= speed_sin
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy -= speed_cos
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx -= speed_sin
            dy += speed_cos

        # Ajuste diagonal
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        self.check_wall_collision(dx, dy)

        # Actualiza ángulo
        self.angle %= math.tau

    def check_wall(self, x, y):
        """Verifica si (x,y) no es pared."""
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        """Evita atravesar paredes."""
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        """Opcional: dibuja información de depuración del jugador."""
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                     (self.x * 100 + WIDTH * math.cos(self.angle),
                      self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        """Control de rotación con el mouse."""
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
        self.angle %= math.tau

    def update(self):
        """Actualiza al jugador en cada frame."""
        self.movement()
        self.mouse_control()
        self.recover_health()

    def is_dead(self):
        """Retorna True si la salud del jugador es 0 o menos."""
        return self.health <= 0

    @property
    def pos(self):
        """Retorna la posición (x,y) del jugador."""
        return self.x, self.y

    @property
    def map_pos(self):
        """Retorna la posición en formato (int,int)."""
        return int(self.x), int(self.y)

    #
    # NUEVO MÉTODO: joystick_move para un estilo WASD + girar solo horizontal con stick derecho
    #
    def joystick_move(self, lx, ly, rx, trigger):
        """
        Mueve y rota al jugador con un mando de Xbox:
          - ly < -0.5 => Avanzar
          - ly >  0.5 => Retroceder
          - lx < -0.5 => Strafe izquierda
          - lx >  0.5 => Strafe derecha
          - rx < -0.2 => girar a la derecha
          - rx >  0.2 => girar a la izquierda
          - trigger > 0.7 => disparar
        """
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        speed = PLAYER_SPEED * self.game.delta_time
        dx, dy = 0, 0

        # Avanzar / Retroceder
        if ly < -0.5:
            dx += cos_a * speed
            dy += sin_a * speed
        elif ly > 0.5:
            dx -= cos_a * speed
            dy -= sin_a * speed

        # Strafe izquierda / derecha
        if lx < -0.5:
            dx += sin_a * speed
            dy -= cos_a * speed
        elif lx > 0.5:
            dx -= sin_a * speed
            dy += cos_a * speed

        self.check_wall_collision(dx, dy)

        # Rotar con stick derecho
        rotate_speed = PLAYER_ROT_SPEED * self.game.delta_time
        if rx < -0.2:
            self.angle -= rotate_speed
        elif rx > 0.2:
            self.angle += rotate_speed
        self.angle %= math.tau

        # Disparo con el gatillo
        if trigger > 0.7:
            if not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True
