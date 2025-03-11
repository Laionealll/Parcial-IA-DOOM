# object_handler.py
#Laioneall Williams
#23-EISN-2-035

import time
import pygame as pg
from sprite_object import *
from npc import *
from random import choices, randrange

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []

        # Sistema de rondas
        self.wave_enemies = [5, 8, 10, 13, 18]  # 5 rondas
        self.current_wave = 0  # índice de la ronda actual
        self.total_enemies = self.wave_enemies[self.current_wave]

        self.spawned_enemies = 0
        self.max_alive = 5
        self.spawn_delay = 3  # Reducido para que aparezcan más rápido
        self.last_spawn_time = time.time()

        # Restricciones para spawn - área reducida alrededor del jugador
        player_x, player_y = int(self.game.player.x), int(self.game.player.y)
        self.restricted_area = {(i, j) for i in range(player_x - 3, player_x + 4)
                                       for j in range(player_y - 3, player_y + 4)}
        
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]
        self.weights = [70, 20, 10]

        # Spawnea un NPC inicial
        self.spawn_npc_initial()

        # Ejemplo de sprites (agrega los que necesites)
        self.add_sprite(AnimatedSprite(game))
        self.add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))

    def spawn_npc_initial(self):
        """Spawnea un NPC al inicio."""
        npc_cls = choices(self.npc_types, self.weights)[0]
        pos = x, y = randrange(1, self.game.map.cols - 1), randrange(1, self.game.map.rows - 1)
        
        # Intentar 20 veces para encontrar una posición válida
        attempts = 0
        while ((pos in self.game.map.world_map) or (pos in self.restricted_area)) and attempts < 20:
            pos = x, y = randrange(1, self.game.map.cols - 1), randrange(1, self.game.map.rows - 1)
            attempts += 1
            
        # Si después de 20 intentos no se encuentra posición, forzar una
        if attempts >= 20:
            for x in range(1, self.game.map.cols - 1):
                for y in range(1, self.game.map.rows - 1):
                    if (x, y) not in self.game.map.world_map and (x, y) not in self.restricted_area:
                        pos = x, y
                        break
        
        self.add_npc(npc_cls(self.game, pos=(x + 0.5, y + 0.5)))
        self.spawned_enemies += 1
        self.last_spawn_time = time.time()

    def spawn_npc_if_needed(self):
        """Spawnea NPC gradualmente hasta alcanzar total_enemies en la wave actual."""
        current_time = time.time()
        alive_npcs = [npc for npc in self.npc_list if npc.alive]

        if self.spawned_enemies < self.total_enemies:
            if len(alive_npcs) < self.max_alive and (current_time - self.last_spawn_time) >= self.spawn_delay:
                npc_cls = choices(self.npc_types, self.weights)[0]
                pos = x, y = randrange(1, self.game.map.cols - 1), randrange(1, self.game.map.rows - 1)
                
                # Intentar 20 veces para encontrar una posición válida
                attempts = 0
                while ((pos in self.game.map.world_map) or (pos in self.restricted_area)) and attempts < 20:
                    pos = x, y = randrange(1, self.game.map.cols - 1), randrange(1, self.game.map.rows - 1)
                    attempts += 1
                
                # Si no se encuentra posición, forzar una
                if attempts >= 20:
                    for x in range(1, self.game.map.cols - 1):
                        for y in range(1, self.game.map.rows - 1):
                            if (x, y) not in self.game.map.world_map and (x, y) not in self.restricted_area:
                                pos = x, y
                                break
                
                self.add_npc(npc_cls(self.game, pos=(x + 0.5, y + 0.5)))
                self.spawned_enemies += 1
                self.last_spawn_time = current_time

    def check_wave_cleared(self):
        """Verifica si se limpió la wave actual y avanza a la siguiente o finaliza el juego."""
        alive = any(n.alive for n in self.npc_list)
        if (self.spawned_enemies == self.total_enemies) and (not alive):
            # Wave completada: se otorga bonus de 200 puntos
            self.game.player.score += 200
            if self.current_wave < len(self.wave_enemies) - 1:
                # Preparar la siguiente wave
                self.current_wave += 1
                self.npc_list.clear()
                self.spawned_enemies = 0
                self.total_enemies = self.wave_enemies[self.current_wave]
                self.last_spawn_time = time.time()
            else:
                # Última wave completada: se otorga bonus de 500 puntos y se guarda el puntaje
                self.game.player.score += 500
                self.game.add_score(self.game.player_name, self.game.player.score)
                # Mostrar pantalla de game over en lugar de victory
                self.game.object_renderer.game_over()
                pg.display.flip()
                # Bucle de espera hasta que el usuario presione una tecla o cierre la ventana
                waiting = True
                while waiting:
                    for event in pg.event.get():
                        if event.type == pg.KEYDOWN or event.type == pg.QUIT:
                            waiting = False
                self.game.playing = False

    def update(self):
        # Actualiza la posición de los NPC vivos para el pathfinding
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        for s in self.sprite_list:
            s.update()
        for n in self.npc_list:
            # Si el NPC acaba de morir y aún no se le han sumado puntos, se agregan 100 puntos
            if not n.alive and not getattr(n, 'scored', False):
                self.game.player.add_score(100)
                n.scored = True
            n.update()
        self.spawn_npc_if_needed()
        self.check_wave_cleared()

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
