#Laioneall Williams
#23-EISN-2-035

import math
import time
import random
from random import randint, random

from sprite_object import *  # Se asume que sprite_object define AnimatedSprite y otras funciones necesarias

###########################
# Clases para Behavior Tree
###########################

class BehaviorNode:
    def run(self, npc):
        raise NotImplementedError

class Selector(BehaviorNode):
    """
    Ejecuta a sus hijos en orden hasta que uno retorne "success".
    """
    def __init__(self, children):
        self.children = children

    def run(self, npc):
        for child in self.children:
            result = child.run(npc)
            if result == "success":
                return "success"
        return "failure"

class Sequence(BehaviorNode):
    """
    Ejecuta a sus hijos en orden; si alguno falla, retorna "failure".
    """
    def __init__(self, children):
        self.children = children

    def run(self, npc):
        for child in self.children:
            result = child.run(npc)
            if result == "failure":
                return "failure"
        return "success"

class Condition(BehaviorNode):
    """
    Nodo condicional: evalúa una función y retorna "success" o "failure".
    """
    def __init__(self, condition_func):
        self.condition_func = condition_func

    def run(self, npc):
        return "success" if self.condition_func(npc) else "failure"

class Action(BehaviorNode):
    """
    Nodo de acción: ejecuta una función y retorna "success" o "failure".
    """
    def __init__(self, action_func):
        self.action_func = action_func

    def run(self, npc):
        return self.action_func(npc)


####################################
# Clase base NPC con Árbol de Comportamiento
####################################

class NPC(AnimatedSprite):
    """
    Clase base para enemigos (NPC) que hereda de AnimatedSprite.
    Maneja animaciones, movimiento, ataques y daño.
    """
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

        # Cargar imágenes de animación
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        # Atributos de combate y movimiento
        self.attack_dist = randint(3, 6)
        self.speed = 0.02
        self.size = 20
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15

        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False

        # Construir el árbol de comportamiento
        self.build_behavior_tree()

    def build_behavior_tree(self):
        """
        Construye el árbol de comportamiento para decidir las acciones del NPC.
        """
        # Condiciones
        is_in_pain = Condition(lambda npc: npc.pain)
        can_see_player = Condition(lambda npc: npc.ray_cast_value)
        is_in_attack_range = Condition(lambda npc: npc.dist < npc.attack_dist)
        is_searching = Condition(lambda npc: npc.player_search_trigger)

        # Acciones
        def do_pain_animation(npc):
            npc.animate_pain()
            return "success"

        def do_attack(npc):
            npc.animate(npc.attack_images)
            npc.attack()
            return "success"

        def do_movement(npc):
            npc.animate(npc.walk_images)
            npc.movement()
            return "success"

        def do_search(npc):
            npc.player_search_trigger = True
            return "success"

        def do_idle(npc):
            npc.animate(npc.idle_images)
            return "success"

        # Crear nodos de acción
        pain_action = Action(do_pain_animation)
        attack_action = Action(do_attack)
        move_action = Action(do_movement)
        search_action = Action(do_search)
        idle_action = Action(do_idle)

        # Secuencias y selectores
        pain_sequence = Sequence([is_in_pain, pain_action])
        attack_sequence = Sequence([
            can_see_player,
            Selector([
                Sequence([is_in_attack_range, attack_action]),
                move_action
            ])
        ])
        search_sequence = Sequence([is_searching, move_action])
        idle_sequence = Sequence([idle_action, search_action])

        # Árbol raíz: prioriza dolor, luego ataque, búsqueda e idle.
        self.root_behavior = Selector([
            pain_sequence,
            attack_sequence,
            search_sequence,
            idle_sequence
        ])

    def update(self):
        """
        Actualiza el NPC: animación, sprite y lógica (Behavior Tree).
        """
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()

    def run_logic(self):
        """
        Lógica principal del NPC: verifica estados y ejecuta el árbol de comportamiento.
        """
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            self.check_hit_in_npc()

            if not self.alive:
                self.animate_death()
                return

            self.root_behavior.run(self)
        else:
            self.animate_death()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        """
        Mueve al NPC usando pathfinding (A* o BFS).
        """
        next_pos = self.game.pathfinding.get_path(
            self.map_pos,
            self.game.player.map_pos,
            method='astar'  # Cambia a 'bfs' si prefieres ese algoritmo
        )
        next_x, next_y = next_pos

        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def attack(self):
        """
        Ejecuta el ataque del NPC: reproduce sonido y, si acierta, daña al jugador.
        """
        if self.animation_trigger:
            self.game.sound.npc_shot.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    def animate_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
       if self.health < 1 and self.alive:
        self.alive = False
        self.game.sound.npc_death.play()
        # 🏆 SUMA PUNTOS:
        self.game.player.score += 100

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # Intersecciones horizontales
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
        depth_hor = (y_hor - oy) / sin_a if sin_a != 0 else float('inf')
        x_hor = ox + depth_hor * cos_a
        delta_depth = dy / sin_a if sin_a != 0 else float('inf')
        dx = delta_depth * cos_a

        for _ in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # Intersecciones verticales
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
        depth_vert = (x_vert - ox) / cos_a if cos_a != 0 else float('inf')
        y_vert = oy + depth_vert * sin_a
        delta_depth = dx / cos_a if cos_a != 0 else float('inf')
        dy = delta_depth * sin_a

        for _ in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_npc():
            pg.draw.line(self.game.screen, 'orange', 
                         (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)


# Ejemplos de clases derivadas con atributos específicos

class SoldierNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

class CacoDemonNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/caco_demon/0.png', pos=(10.5, 6.5),
                 scale=0.7, shift=0.27, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1.0
        self.health = 150
        self.attack_damage = 25
        self.speed = 0.02
        self.accuracy = 0.35

class CyberDemonNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/cyber_demon/0.png', pos=(11.5, 6.0),
                 scale=1.0, shift=0.04, animation_time=210):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 6
        self.health = 350
        self.attack_damage = 15
        self.speed = 0.02
        self.accuracy = 0.25


####################################
# Ejemplo de SpawnManager para control progresivo de enemigos
####################################

class SpawnManager:
    """
    Controla la aparición progresiva de enemigos.
    En lugar de spawnear todos de golpe, se instancian nuevos NPC cada cierto tiempo
    siempre que la cantidad en pantalla sea menor a un máximo definido.
    """
    def __init__(self, game, spawn_points, max_enemies=10, spawn_delay=5):
        """
        spawn_points: lista de tuplas (x, y) con posiciones posibles de aparición.
        max_enemies: cantidad máxima de NPC en pantalla.
        spawn_delay: tiempo en segundos entre spawns.
        """
        self.game = game
        self.spawn_points = spawn_points
        self.max_enemies = max_enemies
        self.spawn_delay = spawn_delay
        self.last_spawn_time = time.time()

    def update(self):
        current_time = time.time()
        # Si hay menos enemigos que el máximo y ha pasado el delay...
        if len(self.game.object_handler.npc_list) < self.max_enemies and (current_time - self.last_spawn_time) >= self.spawn_delay:
            spawn_point = random.choice(self.spawn_points)
            # Instanciar un nuevo NPC, por ejemplo un SoldierNPC.
            new_npc = SoldierNPC(self.game, pos=spawn_point)
            self.game.object_handler.add_npc(new_npc)
            self.last_spawn_time = current_time
