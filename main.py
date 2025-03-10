#Laioneall Williams
#23-EISN-2-035
import pygame as pg
import sys
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
        if pg.joystick.get_count() > 0:
            self.joystick = pg.joystick.Joystick(0)
            self.joystick.init()
            print("Joystick detectado:", self.joystick.get_name())
        else:
            self.joystick = None
            print("No se detectó ningún joystick.")

        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)

        # Estados de ejecución
        self.running = True     # Bucle principal
        self.playing = False    # Cuando estás en partida

        self.font = pg.font.Font(None, 50)

    def new_game(self):
        """Inicia o reinicia una nueva partida."""
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)
        self.playing = True

    def update(self):
        """Actualiza el juego mientras se está jugando."""
        if self.playing:
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
            self.weapon.update()

            pg.display.flip()
            self.delta_time = self.clock.tick(FPS)
            pg.display.set_caption(f'{self.clock.get_fps():.1f}')

            # Si el jugador muere, paramos partida y volvemos al menú
            if self.player.is_dead():
                self.playing = False

    def draw(self):
        """Dibuja los elementos del juego en pantalla."""
        if self.playing:
            self.object_renderer.draw()
            self.weapon.draw()
            # Como ya hicimos un pg.display.flip() en update(), podemos omitirlo aquí
            # pero si prefieres, puedes dejarlo:
            # pg.display.flip()

    def check_events(self):
        """Procesa los eventos del teclado, ratón y joystick."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    # Se abre el menú de pausa
                    self.pause_menu()
                else:
                    self.player.single_fire_event(event)
            else:
                # Enviar eventos de disparo al jugador
                self.player.single_fire_event(event)

        # --- Lectura de ejes del joystick ---
        if self.joystick:
            axis_left_x = self.joystick.get_axis(0)
            axis_left_y = self.joystick.get_axis(1)
            axis_right_x = self.joystick.get_axis(3)
            trigger = self.joystick.get_axis(5)

            self.player.joystick_move(axis_left_x, axis_left_y, axis_right_x, trigger)

    def pause_menu(self):
        """Muestra el menú de pausa con opciones: Continuar, Reiniciar y Salir."""
        pg.mixer.music.pause()
        paused = True
        while paused:
            self.screen.fill((0, 0, 0))
            title = self.font.render("PAUSA", True, (255, 255, 0))
            continue_text = self.font.render("Continuar (C)", True, (255, 255, 255))
            restart_text = self.font.render("Reiniciar (R)", True, (255, 255, 255))
            exit_text = self.font.render("Salir (ESC)", True, (255, 255, 255))
            
            self.screen.blit(title, (RES[0] // 2 - title.get_width() // 2, RES[1] // 3))
            self.screen.blit(continue_text, (RES[0] // 2 - continue_text.get_width() // 2, RES[1] // 2))
            self.screen.blit(restart_text, (RES[0] // 2 - restart_text.get_width() // 2, RES[1] // 2 + 50))
            self.screen.blit(exit_text, (RES[0] // 2 - exit_text.get_width() // 2, RES[1] // 2 + 100))
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
                        self.new_game()  # Reinicia la partida
                        paused = False
                    elif event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

    def show_menu(self):
        """Muestra el menú principal antes de iniciar o tras perder."""
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
                    # ENTER: Inicia nueva partida
                    if event.key == pg.K_RETURN:
                        self.new_game()
                        menu_active = False
                    elif event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

    def run(self):
        """Bucle principal del juego."""
        while self.running:
            # Si estamos jugando, ejecutamos la lógica normal
            if self.playing:
                self.check_events()
                self.update()
                self.draw()
            else:
                # Si no estamos jugando (jugador murió o juego no iniciado), mostramos el menú
                self.show_menu()

if __name__ == '__main__':
    game = Game()
    game.run()
