# player.py
#Laioneall Williams
#23-EISN-2-035

import pygame as pg
from settings import *
import math
import os
from datetime import datetime

class Player:
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

        # Puntaje
        self.score = 0
        # Se elimina el uso de scores.json para evitar duplicidad con scoreboard.json

    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def get_damage(self, damage):
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        # No se guarda el score aquí; se actualiza al matar enemigos y al finalizar la partida.

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time

        keys = pg.key.get_pressed()
        num_key_pressed = -1

        if keys[pg.K_w]:
            num_key_pressed += 1
            dx += cos_a * speed
            dy += sin_a * speed
        if keys[pg.K_s]:
            num_key_pressed += 1
            dx -= cos_a * speed
            dy -= sin_a * speed
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx += sin_a * speed
            dy -= cos_a * speed
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx -= sin_a * speed
            dy += cos_a * speed

        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        self.check_wall_collision(dx, dy)
        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        pg.draw.line(
            self.game.screen, 
            'yellow', 
            (self.x * 100, self.y * 100),
            (self.x * 100 + WIDTH * math.cos(self.angle), self.y * 100 + WIDTH * math.sin(self.angle)), 2
        )
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
        self.angle %= math.tau

    def update(self):
        self.movement()
        self.mouse_control()
        self.recover_health()

    def is_dead(self):
        return self.health <= 0

    def add_score(self, points):
        """Añade puntos al jugador y muestra un mensaje de debug"""
        self.score += points
        print(f"DEBUG: +{points} puntos. Score total: {self.score}")

    def joystick_move(self, lx, ly, rx, trigger):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        speed = PLAYER_SPEED * self.game.delta_time
        dx, dy = 0, 0

        if ly < -0.5:
            dx += cos_a * speed
            dy += sin_a * speed
        elif ly > 0.5:
            dx -= cos_a * speed
            dy -= sin_a * speed

        if lx < -0.5:
            dx += sin_a * speed
            dy -= cos_a * speed
        elif lx > 0.5:
            dx -= sin_a * speed
            dy += cos_a * speed

        self.check_wall_collision(dx, dy)

        rotate_speed = PLAYER_ROT_SPEED * self.game.delta_time
        if rx < -0.2:
            self.angle -= rotate_speed
        elif rx > 0.2:
            self.angle += rotate_speed
        self.angle %= math.tau

        if trigger > 0.7:
            if not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

    @property
    def pos(self):
        """Devuelve la posición actual del jugador."""
        return self.x, self.y

    @property
    def map_pos(self):
        """Devuelve la posición entera (mapa) del jugador."""
        return int(self.x), int(self.y)
