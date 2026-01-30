# IMPORTADORES del programa

import pygame
from pathlib import Path
import random
from pytmx.util_pygame import load_pygame
import pytmx
# IMPORTADORES de archivos de código

from dialogue_onchar import Dialogue
from tilemaps_scenes import Active_tilemap
from sound_effect import Conditional_sound
from user_move import User_character

# INICIADORES pygame

pygame.init()
pygame.mixer.init()

# CREADOR de pantalla y otras cualidades de display
width = 1600
height = 900
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Mascaritas")


# VARIABLES globales booleanas

# detecta si está apretando una tecla de caminar
walking = False 

# establece que el juego se ejecuta
run = True 

# chequea que no colisionó al comienzo del juego
collided = False

# dirección de texto inicial
dir = 'midtop'


# VARIABLES globales numericas

# establece milisegundos antes de mostrar otro MSG
cooldown_wall_hit = 1000 

# establece que el primer fondo será el 1
back_set = 1


# VARIABLES globales de formato

# fuente monoespacio
monospace_font = pygame.font.SysFont('Monospace', 16, bold = True) 


# VARIABLES globales de archivo TMX tilemap

# mapa de placita
tiled_map_placita = Active_tilemap((Path.cwd() / 'images' / 'escenarios' / 'placita2.tmx'), 6.25) 

# mapa de caminito
tiled_map_caminito = Active_tilemap(Path.cwd() / 'images' / 'escenarios' / 'caminito.tmx', 6.25) 

# mapa de cuatro gatos
tiled_map_test = Active_tilemap(Path.cwd() / 'images' / 'escenarios' / 'test.tmx', 6.25)

tiled_map_palomas = Active_tilemap(Path.cwd() / 'images' / 'escenarios' / 'palomas.tmx', 6.25)


# VARIABLES globales de archivo de sonido 

# sonido de caminar
walk_sound1 = Conditional_sound(Path.cwd() / 'sound' / 'effects' / 'pasos.mp3', 2)

# VARIABLES de mensaje con caja DIALOGUE

# mensaje al ver gato
message_cat = Dialogue ("Qué lindo gato. \nYo también quiero un gato, loco", monospace_font, (0,0,0), (Path.cwd() / 'images' / 'cuadro de texto.png'))

# mensaje en la placita
message_placita = Dialogue ("Acá hay mucho olor a porro. \nMe dan ganas de partirme uno", monospace_font, (0,0,0), (Path.cwd() / 'images' / 'cuadro de texto.png'))

message_get_mascara = Dialogue ("En el piso de la placita encontrás algo. \nCiertamente curioso. Te lo vas a quedar", monospace_font, (0,0,0), (Path.cwd() / 'images' / 'cuadro de texto.png'))

# VARIABLES de clase y función

# usuario, pos incial y movimiento en 0
char = User_character (16, 400, 400, False, False, False, False)

# establece un reloj para fps
speed = pygame.time.Clock()

# define el primer fondo a mostrarse
background = tiled_map_caminito

flipped = False
# propone items para el juego
class Items:

    def __init__ (self, name, description, item_image):
        self.name = name
        self.description = description
        self.icon_image = pygame.image.load(item_image)

## LOOP DE JUEGO ##

## WHILE RUN: JUEGA
## IF RUN == FALSE: ROMPE
## NO SUMAR LOOPS O WHILES!! PELIGROSO 


while run == True:

    # Pone todo el tiempo música de fondo, la misma música
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(Path.cwd() / 'sound' / 'mascarita.mp3')
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1, 35)

    # por las dudas de que algo ande mal, tiñe capa -1 de negro.
    screen.fill((0, 0, 0))

    # current time almacena el tiempo real, speed.tick deja FPS en 8
    current_time = pygame.time.get_ticks()
    speed.tick(16)
    
    # se muestra en capa 0 MAP_SURFACE
    background.render_to_surface(screen)

    # la función UPDATE del objeto CHAR, clase User_character
    # maneja el movimiento y el sonido que hace al moverse
    # is_walking = False
    char.update_position(False, background.collision_objects())
    char.movement() 
    

    # si el personaje se mueve, suenan las pisadas en obj walk_sound1
    if char.is_walking:
       walk_sound1.playing(-1)
    else:
      walk_sound1.stop_playing()

    # una vez char puede moverse, lo mostramos en capa 1
    # (superior a capa 0)
    screen.blit(char.player_sprite, char.rect)

    # si el personaje supera X:
    # cambia de pantalla si está en background 1
    # de lo contrario, no puede seguir caminando
    if char.x >= width - 48:
        if back_set == 1:
            background = tiled_map_palomas
            char.x = 56        
            back_set = 3
        elif back_set == 2:
            background = tiled_map_caminito
            char.x = 56
            back_set = 1
        elif back_set == 3:
            char.x = width - 56
        elif back_set == 4:
            char.x = width - 56 
        elif back_set == 5:
            char.x = width - 56

    # lo mismo en posición menor a 50 en X
    # con background 3
    if char.x <= 48:
        if back_set == 1:
            background = tiled_map_test
            char.x = width - 56
            back_set = 2
        elif back_set == 2:
            char.x = 56
        elif back_set == 3:
            background = tiled_map_caminito
            char.x = width - 56
            back_set = 1
        elif back_set == 4:
            char.x = 56
        elif back_set == 5:
            char.x = 56

    
    # lo mismo en posición menor a 50 en Y
    # con background 5
    if char.y <= 48:
        if back_set == 1:
            background = tiled_map_placita
            char.y = height - 56
            back_set = 4
        elif back_set == 2:
            char.y = 56
        elif back_set == 3:
            char.y = 56
        elif back_set == 4:
            char.y = 56
        elif back_set == 5:
            background = tiled_map_caminito
            char.y = height - 56
            back_set = 1

    # lo mismo en posición mayor a 450 en Y
    # con background 4
    if char.y >= height - 48:
        if back_set == 1:
            background = tiled_map_test
            char.y = 56
            back_set = 5
        elif back_set == 2:
            char.y = height - 56
        elif back_set == 3:
            char.y = height - 56
        elif back_set == 4:
            background = tiled_map_caminito
            char.y = 56
            back_set = 1
        elif back_set == 5:
            char.y = height - 56
    if background == tiled_map_palomas:
        tiled_map_palomas.flip_random_obj(current_time)
    
    if background == tiled_map_test:
        if char.collide_with_tiles(background.collision_objects()):
            message_cat.start_dialogue_triggered(current_time)
            if char.x > 800:
                dir = 'midright'
            else:
                dir = 'midleft'
            message_cat.render(char.x, char.y, dir)

            message_cat.dialogue_display(current_time, 2000)

    if background == tiled_map_placita:
        dir = 'topright'

        if char.y < 600 and not message_placita.is_active:
            message_get_mascara.render(char.x, char.y, dir)

            message_placita.is_active = True
            message_placita.render(char.x, char.y, dir)
            screen.blit(message_placita.box_surface, message_placita.box_rect)
            screen.blit(message_placita.render_str, message_placita.str_rect)
        else:
            message_placita.is_active = False


    # ESTE ES UN IF PARA TODO EL JUEGO
    # es decir, aplica en el momento deseado
    
       
        # si hay un mensaje renderizado y que quiere ser mostrado
        # el mensaje se muestra por el tiempo indicado en el último número (1500 milis)

    # MANEJADOR DE EVENTOS
    # evento pygame.QUIT: si querés salir del juego, el código rompe.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # actualiza el código al final, y constantemente
    pygame.display.update()

pygame.quit()