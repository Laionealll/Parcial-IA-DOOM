#Laioneall Williams
#23-EISN-2-035
import pygame as pg

class Sound:
    """
    Clase para la gestión de efectos de sonido y música en el juego.
    """
    def __init__(self, game):
        self.game = game
        # Inicializa el mezclador de audio de Pygame
        pg.mixer.init()
        
        # Carpeta base donde se almacenan los archivos de sonido
        self.path = 'resources/sound/'
        
        # Carga los efectos de sonido (disparo, dolor, muerte, etc.)
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav')
        # Ajusta el volumen del sonido de ataque del NPC
        self.npc_shot.set_volume(0.2)
        
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        
        # Carga un archivo de música para usar como tema principal
        self.theme = pg.mixer.music.load(self.path + 'theme.mp3')
        # Ajusta el volumen de la música
        pg.mixer.music.set_volume(0.3)
