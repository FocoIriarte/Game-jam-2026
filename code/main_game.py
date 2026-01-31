# IMPORTADORES del programa

import pygame
from pathlib import Path
import random
from pytmx.util_pygame import load_pygame
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
arial_font = pygame.font.SysFont('Trebuchet MS', 45, bold = True)


# VARIABLES globales de archivo TMX tilemap

# mapa de placita
tiled_map_placita = Active_tilemap((Path.cwd() / 'images' / 'escenarios' / 'placita2.tmx'), 6.25) 

# mapa de caminito
tiled_map_caminito = Active_tilemap(Path.cwd() / 'images' / 'escenarios' / 'caminito.tmx', 6.25) 

# mapa de cuatro gatos
tiled_map_tren = Active_tilemap(Path.cwd() / 'images' / 'assets' / 'tren.tmx', 6.25)

tiled_map_palomas = Active_tilemap(Path.cwd() / 'images' / 'escenarios' / 'palomas.tmx', 6.25)

tiled_map_estrella = Active_tilemap(Path.cwd() / 'images' / 'assets' / 'estrella.tmx', 6.25)


# VARIABLES globales de archivo de sonido 

# sonido de caminar
walk_sound1 = Conditional_sound(Path.cwd() / 'sound' / 'effects' / 'pasos.mp3', 2)

# VARIABLES de mensaje con caja DIALOGUE

# mensaje al ver gato
message_cat = Dialogue ("Qué lindo gato. \nYo también quiero un gato, loco", monospace_font, (0,0,0), (Path.cwd() / 'images' / 'cuadro de texto.png'))

# mensaje en la placita
message_placita = Dialogue ("Acá hay mucho olor a porro. \nMe dan ganas de partirme uno", monospace_font, (0,0,0), (Path.cwd() / 'images' / 'cuadro de texto.png'))

message_get_mascara = Dialogue ("En el piso de la placita encontrás algo. \nCiertamente curioso. Te lo vas a quedar", monospace_font, (0,0,0), (Path.cwd() / 'images' / 'cuadro de texto.png'))

message_white_bird = Dialogue ("¡Qué hermosa paloma! \n Creo que tiene algo en el cuello... \n ¿A ver qué es?", monospace_font, (0,0,0), (Path.cwd() / 'images' / 'cuadro de texto.png'))

message_got_item = Dialogue('¡TIENES UN NUEVO OBJETO!', arial_font, (255, 41, 0), (Path.cwd() / 'images' / 'cuadro de texto.png'))

inventory = []

inventory_open = False



# VARIABLES de clase y función
movement = 16
# usuario, pos incial y movimiento en 0
char = User_character (400, 400, False, False, False, False, inventory)




# establece un reloj para fps
clock = pygame.time.Clock()

# define el primer fondo a mostrarse
background = tiled_map_caminito
bird_got_item = False
you_got_item = False
object_got_message_boolean = False
choose_item = 0
# propone items para el juego

## LOOP DE JUEGO ##

## WHILE RUN: JUEGA
## IF RUN == FALSE: ROMPE
## NO SUMAR LOOPS O WHILES!! PELIGROSO 

random_duration = random.randint(1000, 4000)
white_bird_choice = [(23, 1), (10, 3), (2, 4), (15, 5), (17, 5), (14, 6), (15, 6), (17, 7), (13, 7), (14, 8), (18, 8), (21, 8), (10, 8), (13, 9), (16, 9), (9, 11), (13, 11), (14, 11), (22, 13)]
grey_bird_choice= [(26,3), (19,4), (12,6), (19,6), (11,7), (18,7), (28,7), (12,8), (17,8), (12,9), (14,9), (17,9), (18,9), (19,9), (19,9), (15,10), (16,10), (17,10), (19,10), (20,10), (12,11), (18, 11), (15,12), (10,13), (14,13), (18,13), (16,16), (20,16), (27,16)]
x_y = None
variable_bandera = 0
current_white_bird_flip, current_grey_bird_flip = (0 , 0 )
got_item_key = False
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

    clock.tick(16)

   
    if background == tiled_map_palomas:

        tiled_map_palomas.update_flips(current_time)
        
        if current_time >= current_white_bird_flip:
            x_y_white = random.choice(white_bird_choice)
            x_chosen_white, y_chosen_white = x_y_white
            
            tiled_map_palomas.flip_random_obj(12, current_time, x_chosen_white, y_chosen_white)
            
            random_duration = random.randint(800, 2000)
            current_white_bird_flip = current_time + random_duration

        if current_time >= current_grey_bird_flip:
            x_y_grey = random.choice(grey_bird_choice)
            x_chosen_grey, y_chosen_grey = x_y_grey
            
            tiled_map_palomas.flip_random_obj(22, current_time, x_chosen_grey, y_chosen_grey)
            
            random_duration = random.randint(800, 2000)
            current_grey_bird_flip = current_time + random_duration
        

    background.render_to_surface(screen) 
    
    # se muestra en capa 0 MAP_SURFACE

    # la función UPDATE del objeto CHAR, clase User_character
    # maneja el movimiento y el sonido que hace al moverse
    # is_walking = False
    char.movement(movement)

    char.update_position(False)

    # si el personaje se mueve, suenan las pisadas en obj walk_sound1
    if char.is_walking:
       walk_sound1.playing(0)
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
            back_set = 2
        elif back_set == 2:
            background = tiled_map_tren
            char.x = 56
            back_set = 3
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
            char.x = 56
        elif back_set == 2:
            background = tiled_map_caminito
            char.x = width - 56
            back_set = 1
        elif back_set == 3:
            background = tiled_map_palomas
            char.x = width - 56
            back_set = 2
        elif back_set == 4:
            char.x = 56
        elif back_set == 5:
            char.x = 56

    
    # lo mismo en posición menor a 50 en Y
    # con background 5
    if char.y <= 48:
        if back_set == 1:
            char.y = 56
        elif back_set == 2:
            char.y = 56
        elif back_set == 3:
            char.y = 56
        elif back_set == 4:
            char.y = height - 56
            background = tiled_map_tren
            back_set = 3
        elif back_set == 5:
            char.y = 56

    # lo mismo en posición mayor a 450 en Y
    # con background 4
    if char.y >= height - 48:
        if back_set == 1:
            char.y = height - 56
        elif back_set == 2:
            char.y = height - 56
        elif back_set == 3:
            char.y = 56
            background = tiled_map_estrella
            back_set = 4
        elif back_set == 4:
            char.y = height - 56
        elif back_set == 5:
            char.y = height - 56

    if background == tiled_map_palomas:
        char.add_item('Máscara roja', 'El olor a tierra y la bronca acumulada\ndurante los años de los años\nyacen en esta máscara')
        char.add_item('Máscara azul', 'La avaricia y abundacia, contradictorias como\nson, debaten su poderío incesantemente\nen esta máscara')
        char.add_item('Máscara verde', 'El remoto resonar de un silbato\ny el deseo de acabarlo con todo\ndescansan pacíficamente\nen esta máscara ')

    # if background == tiled_map_palomas:
    #     grey_bird_collision = tiled_map_palomas.certain_collision_objects(22)
        
    #     if char.collide_with_tiles(grey_bird_collision) and bird_got_item == False:
    #         if not hasattr(message_white_bird, 'time_start'):
    #             message_white_bird.time_start = current_time

    #         if current_time < message_white_bird.time_start + 2000:
    #             message_white_bird.render(char.x, char.y, dir, 30)
    #             message_white_bird.dialogue_display(True)
    #         else:
    #             bird_got_item = True
    
    # if bird_got_item == True and you_got_item == False and got_item_key == True:
    #     if not hasattr(message_got_item, 'time_start'):
    #         message_got_item.time_start = current_time
    #     if current_time <= message_got_item.time_start + 2000:
    #         message_got_item.render(width/2, height/2, 'center', 20)
    #         message_got_item.dialogue_display(True)
    #     else:
    #         you_got_item = True

    #     char.list_inventory()
    
    
    if inventory_open == True:
        char.render_inventory(width/2, height/2, screen, choose_item)

    # ESTE ES UN IF PARA TODO EL JUEGO
    # es decir, aplica en el momento desedo

    # MANEJADOR DE EVENTOS
    # evento pygame.QUIT: si querés salir del juego, el código rompe.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                got_item_key = True
            if event.key == pygame.K_q:
                inventory_open = True
            if event.key == pygame.K_d and inventory_open == True and choose_item < 3:
                choose_item += 1
            if event.key == pygame.K_a and inventory_open == True and choose_item >= 1:
                    choose_item -= 1
            if event.key == pygame.K_LSHIFT:
                movement += 16
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                inventory_open = False
                choose_item = 0
            if event.key == pygame.K_LSHIFT:
                movement -=16
            if event.key == pygame.K_SPACE:
                got_item_key = False

            
    # actualiza el código al final, y constantemente
    pygame.display.update()

pygame.quit()