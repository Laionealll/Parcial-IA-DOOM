#Laioneall Williams
#23-EISN-2-035
import time
from sprite_object import *
from npc import *
from random import choices, randrange

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc

        # Config para spawns
        self.total_enemies = 20
        self.spawned_enemies = 0
        self.max_alive = 5
        self.spawn_delay = 5
        self.last_spawn_time = time.time()
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]
        self.weights = [70, 20, 10]

        # Spawnea un NPC inicial (opcional)
        self.spawn_npc_initial()

        # Spawneo de sprites estáticos y animados
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 5.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(12.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 12.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(10.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 14.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 18.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 24.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 24.5)))

    def spawn_npc_initial(self):
        """Spawnea un NPC al inicio de la partida (opcional)."""
        npc = choices(self.npc_types, self.weights)[0]
        pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
        while (pos in self.game.map.world_map) or (pos in self.restricted_area):
            pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
        self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))
        self.spawned_enemies += 1
        self.last_spawn_time = time.time()

    def spawn_npc_if_needed(self):
        """Spawnea NPC de forma gradual."""
        current_time = time.time()
        alive_npcs = [npc for npc in self.npc_list if npc.alive]
        if self.spawned_enemies < self.total_enemies:
            if len(alive_npcs) < self.max_alive and (current_time - self.last_spawn_time) >= self.spawn_delay:
                npc = choices(self.npc_types, self.weights)[0]
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                    pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))
                self.spawned_enemies += 1
                self.last_spawn_time = current_time

    def check_win(self):
        """
        Verifica la condición de victoria:
         - Se han spawneado todos los enemigos (total_enemies)
         - Y no queda ningún NPC vivo.
        """
        alive = any(npc.alive for npc in self.npc_list)
        if self.spawned_enemies == self.total_enemies and not alive:
            # Muestra la pantalla de victoria
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(1500)
            # En lugar de new_game, paramos la partida y volvemos al menú
            self.game.playing = False

    def update(self):
        """Actualiza el estado de todos los objetos."""
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        self.spawn_npc_if_needed()
        self.check_win()

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
