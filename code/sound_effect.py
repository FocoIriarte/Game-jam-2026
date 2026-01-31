import pygame
pygame.init()

# La clase Conditional_sound ejecuta:
# un efecto de sonido continuo y loopeado

# requiere un obj desde Conditional_sound con:
# ARCHIVO DE SONIDO + MULTIPLICADOR DE VOLUMEN

# requiere llamar a la función playing con:
# cantidad de veces que LOOPEA el sonido
# -1 es infinito. debe nombrarse al momento de ejecutar el sonido

# OPT - SUGERIDO:
# llamar función stop_playing donde se deba dejar de ejecutar el sonido

class Conditional_sound:

    def __init__ (self, sound, volume):

        # al adjudicar Conditional_sound a un obj, ese obj tomará:
        # un sonido con un volumen, y un valor FALSO en is_playing

        self.sound = sound
        self.condit_sound = pygame.mixer.Sound(self.sound)
        self.condit_sound.set_volume(volume)
        self.is_playing = False
    
    def playing(self, loop_times):

        # la función playing ejecuta un sonido
        # cuando is_playing es FALSO

        if not self.is_playing:
            self.condit_sound.play(-1)
            self.is_playing = True

    def stop_playing(self):

        # la función stop_playing frena abruptamente el sonido
        # is_playing se vuelve FALSO

        self.condit_sound.stop()
        self.is_playing = False

