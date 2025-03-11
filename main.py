# main.py
# ----------------------------------------
# Laioneall Williams
# 23-EISN-2-035
import pygame as pg
import sys
import os
import json
from settings import *
from map import Map
from player import Player
from raycasting import RayCasting
from object_renderer import ObjectRenderer
from sprite_object import *
from object_handler import ObjectHandler
from weapon import Weapon
from sound import Sound
from pathfinding import PathFinding


class Game:
    def __init__(self):
        pg.init()
        pg.joystick.init()

        self.joystick = None
        if pg.joystick.get_count() > 0:
            self.joystick = pg.joystick.Joystick(0)
            self.joystick.init()
            print("Joystick detectado:", self.joystick.get_name())
        else:
            print("No se detectó ningún joystick.")

        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)

        self.running = True
        self.playing = False
        self.font = pg.font.Font(None, 50)

        # Nombre del jugador
        self.player_name = ""

        # Ranking en memoria
        self.ephemeral_scores = []
        self.load_scoreboard()

    def load_scoreboard(self):
        """
        Intenta cargar scoreboard.json para inicializar ephemeral_scores.
        Si no existe, se crea un archivo vacío.
        """
        try:
            if os.path.exists("scoreboard.json"):
                with open("scoreboard.json", "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:  # Verificar que el archivo no esté vacío
                        data = json.loads(content)
                        if isinstance(data, list):
                            self.ephemeral_scores = data
                            print("DEBUG: Se cargaron", len(data), "puntajes desde scoreboard.json")
                    else:
                        print("DEBUG: scoreboard.json está vacío, usando lista vacía")
                        self.ephemeral_scores = []
            else:
                # Si no existe, creamos el archivo
                with open("scoreboard.json", "w", encoding="utf-8") as f:
                    f.write("[]")
                print("DEBUG: Se creó un nuevo archivo scoreboard.json")
        except Exception as e:
            print("DEBUG: Error leyendo scoreboard.json:", e)
            # Si hubo un error (ej: JSON inválido), creamos un nuevo archivo
            try:
                with open("scoreboard.json", "w", encoding="utf-8") as f:
                    f.write("[]")
                print("DEBUG: Se creó un nuevo archivo scoreboard.json debido a un error")
            except Exception as e2:
                print("DEBUG: Error creando scoreboard.json:", e2)

    def save_scoreboard(self):
        """
        Escribe self.ephemeral_scores a scoreboard.json,
        para que persista entre ejecuciones.
        """
        try:
            with open("scoreboard.json", "w", encoding="utf-8") as f:
                json.dump(self.ephemeral_scores, f, indent=4)
            print("DEBUG: scoreboard.json actualizado con", len(self.ephemeral_scores), "registros.")
        except Exception as e:
            print("DEBUG: Error guardando scoreboard.json:", e)

    def add_score(self, name, score):
        """
        Añade (name, score) a ephemeral_scores, lo ordena y guarda en disco.
        """
        if score <= 0:
            print("DEBUG: No se guarda la puntuación 0 o negativa")
            return
            
        record = {"name": name, "score": score}
        self.ephemeral_scores.append(record)
        # Orden descendente
        self.ephemeral_scores.sort(key=lambda r: r["score"], reverse=True)
        self.save_scoreboard()
        print("DEBUG: Se guardó puntaje", name, score)

    def new_game(self):
        self.show_name_input_screen()

        # Inicializar componentes del juego
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        
        # Esto debe inicializarse después del jugador
        self.object_handler = ObjectHandler(self)
        
        pg.mixer.music.play(-1)
        self.playing = True

    def show_name_input_screen(self):
        """
        Solicita el nombre en la ventana de Pygame.
        """
        input_active = True
        entered_text = ""

        while input_active:
            self.screen.fill((0, 0, 0))
            prompt = self.font.render("Escribe tu nombre y presiona ENTER:", True, (255, 255, 255))
            self.screen.blit(prompt, (RES[0] // 2 - prompt.get_width() // 2, RES[1] // 3))

            name_surf = self.font.render(entered_text, True, (255, 255, 0))
            self.screen.blit(name_surf, (RES[0] // 2 - name_surf.get_width() // 2, RES[1] // 2))

            info_surf = self.font.render("[ENTER] para confirmar", True, (100, 100, 255))
            self.screen.blit(info_surf, (RES[0] // 2 - info_surf.get_width() // 2, RES[1] // 2 + 50))

            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.player_name = entered_text.strip()
                        if not self.player_name:
                            self.player_name = "Jugador"
                        input_active = False
                    elif event.key == pg.K_BACKSPACE:
                        entered_text = entered_text[:-1]
                    else:
                        if event.unicode.isprintable():
                            entered_text += event.unicode

    def update(self):
        if self.playing:
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
            self.weapon.update()

            pg.display.flip()
            self.delta_time = self.clock.tick(FPS)
            pg.display.set_caption(f'{self.clock.get_fps():.1f}')

            # Checar si muere => registrar y volver a menú
            if self.player.is_dead():
                print(f"DEBUG: Jugador murió con score: {self.player.score}")
                self.add_score(self.player_name, self.player.score)
                self.playing = False

    def draw(self):
        if self.playing:
            self.object_renderer.draw()
            self.weapon.draw()
            
            # Dibujar puntaje en pantalla
            score_text = f"Score: {self.player.score}"
            score_surf = self.font.render(score_text, True, (255, 255, 0))
            self.screen.blit(score_surf, (RES[0] - score_surf.get_width() - 20, 80))

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.pause_menu()
                else:
                    self.player.single_fire_event(event)
            else:
                self.player.single_fire_event(event)

        if self.joystick:
            axis_left_x = self.joystick.get_axis(0)
            axis_left_y = self.joystick.get_axis(1)
            axis_right_x = self.joystick.get_axis(3)
            trigger = self.joystick.get_axis(5)
            self.player.joystick_move(axis_left_x, axis_left_y, axis_right_x, trigger)

    def pause_menu(self):
        pg.mixer.music.pause()
        paused = True
        while paused:
            self.screen.fill((0, 0, 0))
            title = self.font.render("PAUSA", True, (255, 255, 0))
            c_text = self.font.render("Continuar (C)", True, (255, 255, 255))
            r_text = self.font.render("Reiniciar (R)", True, (255, 255, 255))
            t_text = self.font.render("Ver Ranking (T)", True, (255, 255, 255))
            e_text = self.font.render("Salir (ESC)", True, (255, 255, 255))

            self.screen.blit(title, (RES[0] // 2 - title.get_width() // 2, RES[1] // 4))
            self.screen.blit(c_text, (RES[0] // 2 - c_text.get_width() // 2, RES[1] // 2))
            self.screen.blit(r_text, (RES[0] // 2 - r_text.get_width() // 2, RES[1] // 2 + 50))
            self.screen.blit(t_text, (RES[0] // 2 - t_text.get_width() // 2, RES[1] // 2 + 100))
            self.screen.blit(e_text, (RES[0] // 2 - e_text.get_width() // 2, RES[1] // 2 + 150))

            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_c:
                        pg.mixer.music.unpause()
                        paused = False
                    elif event.key == pg.K_r:
                        # Registrar puntaje actual y reiniciar
                        self.add_score(self.player_name, self.player.score)
                        self.new_game()
                        paused = False
                    elif event.key == pg.K_t:
                        self.show_rankings()
                    elif event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

    def show_rankings(self):
        """
        Muestra el ranking con los puntajes en ephemeral_scores (ya ordenados).
        """
        data = self.ephemeral_scores
        
        # Mensajes diferentes si no hay puntuaciones
        if not data:
            waiting = True
            while waiting:
                self.screen.fill((0, 0, 0))
                title = self.font.render("Ranking", True, (255, 255, 0))
                self.screen.blit(title, (RES[0] // 2 - title.get_width() // 2, 50))
                
                no_scores = self.font.render("No hay puntuaciones registradas.", True, (255, 255, 255))
                self.screen.blit(no_scores, (RES[0] // 2 - no_scores.get_width() // 2, RES[1] // 2))
                
                info = self.font.render("Presiona cualquier tecla para volver", True, (100, 100, 255))
                self.screen.blit(info, (RES[0] // 2 - info.get_width() // 2, RES[1] // 2 + 100))
                
                pg.display.flip()
                
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.KEYDOWN:
                        waiting = False
            return
            
        # Hay puntuaciones para mostrar
        self.screen.fill((0, 0, 0))
        font = pg.font.Font(None, 40)

        title = self.font.render("Ranking", True, (255, 255, 0))
        self.screen.blit(title, (RES[0] // 2 - title.get_width() // 2, 50))

        y_offset = 150
        top5 = data[:5]
        for idx, record in enumerate(top5):
            text_line = f"{idx+1}. {record['name']} - {record['score']} pts"
            line_surface = font.render(text_line, True, (255, 255, 255))
            self.screen.blit(line_surface, (RES[0] // 4, y_offset))
            y_offset += 50

        info = font.render("Presiona cualquier tecla para volver", True, (100, 100, 255))
        self.screen.blit(info, (RES[0] // 2 - info.get_width() // 2, y_offset + 50))

        pg.display.flip()
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    waiting = False

    def show_menu(self):
        menu_active = True
        while menu_active:
            self.screen.fill((0, 0, 0))
            title = self.font.render("CLON DE DOOM ", True, (255, 0, 0))
            start_text = self.font.render("Presiona ENTER para Jugar", True, (255, 255, 255))
            exit_text = self.font.render("Presiona ESC para Salir", True, (255, 255, 255))

            self.screen.blit(title, (RES[0] // 2 - title.get_width() // 2, RES[1] // 3))
            self.screen.blit(start_text, (RES[0] // 2 - start_text.get_width() // 2, RES[1] // 2))
            self.screen.blit(exit_text, (RES[0] // 2 - exit_text.get_width() // 2, RES[1] // 2 + 50))
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.new_game()
                        menu_active = False
                    elif event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

    def run(self):
        while self.running:
            if self.playing:
                self.check_events()
                self.update()
                self.draw()
            else:
                self.show_menu()


if __name__ == '__main__':
    game = Game()
    game.run()
