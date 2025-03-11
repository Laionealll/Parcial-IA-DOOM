# object_renderer.py
#Laioneall Williams
#23-EISN-2-035

import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        self.wall_textures = self.load_wall_textures()
        self.win_image = self.get_texture('resources/textures/win.png', RES)
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0

        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)

        # Dígitos para salud
        self.digit_size = 90
        self.digit_images = [
            self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size]*2)
            for i in range(11)
        ]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))

        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_wave_number()

    def draw_wave_number(self):
        """
        Muestra la ronda actual, por ejemplo: "Ronda 1/5"
        """
        oh = self.game.object_handler
        wave_index = oh.current_wave  # 0-based
        total_waves = len(oh.wave_enemies)
        wave_text = f"Ronda {wave_index + 1}/{total_waves}"

        font = pg.font.Font(None, 60)
        surf = font.render(wave_text, True, (255, 0, 0))
        x_pos = WIDTH - surf.get_width() - 20
        y_pos = 20
        self.screen.blit(surf, (x_pos, y_pos))

    def show_victory_screen(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.win_image, (0, 0))
        pg.display.flip()

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health_str = str(self.game.player.health)
        for i, char in enumerate(health_str):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        # El '10' puede ser un '%' o símbolo
        self.screen.blit(self.digits['10'], ((i + 1)*self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5*self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }
