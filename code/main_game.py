# IMPORTADORES del programa

import pygame
from pathlib import Path
import random
from pytmx.util_pygame import load_pygame

# IMPORTADORES de archivos de código

from dialogue_onchar import Text
from tilemaps_scenes import Active_tilemap
from sound_effect import Conditional_sound
from user_move import User_character
from npc_class import NPC

# INICIADORES pygame

pygame.init()
pygame.mixer.init()

# CREADOR de pantalla y otras cualidades de display

width = 1600
height = 900
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Mascaritas")

# RUTAS ABSOLUTAS

BASE_DIR = Path(__file__).resolve().parent.parent
ESCENARIOS_DIR = BASE_DIR / 'images' / 'escenarios'
ASSETS_DIR = BASE_DIR / 'images' / 'assets'
SOUND_DIR = BASE_DIR / 'sound' #para sonido
TEXTBOX_IMG = ASSETS_DIR / 'cuadro de texto.png'

# VARIABLES globales booleanas

# detecta si está apretando una tecla de caminar

walking = False 

# establece que el juego se ejecuta

run = True 

# establece que el inventario no está abierto constantemente

inventory_open = False

# define que no estás agarrando o interactuando con un objeto

got_item_key = False

# define si estás interactuando con NPC

got_interaction_npc = False

# VARIABLES NONE O VACÍAS

# lista de items en inventario

inventory = []

# primer item del inventario en display es el index 0

choose_item = 0

# no hay posición de giro de palomas hasta que se setea

current_whitebird_flip, current_greybird_flip = (0 , 0 )

# la colisión con personajes no es ni CONTRA el personaje ni CERCA del personaje

result_of_collide = 0

# no chocamos con nada

collided = False

# no tenemos la máscara roja

got_mascara_roja = False

# indice de dialogo

dialogue_index = 0

# VARIABLES globales numericas

# confirma que el primer fondo será el 1

back_set = 1

# establece la velocidad del jugador en 16

movement = 16

# VARIABLES de fuente

# fuente monoespacio pequeña

monospace_font = pygame.font.SysFont('Monospace', 16, bold = True) 

# fuente arial GRANDE

arial_font = pygame.font.SysFont('Trebuchet MS', 45, bold = True)

# VARIABLES globales de archivo TMX tilemap

# mapa de caminito
tiled_map_caminito = Active_tilemap(ESCENARIOS_DIR / 'caminito.tmx', 6.25)

# mapa de tren
tiled_map_tren = Active_tilemap(ASSETS_DIR / 'tren.tmx', 6.25)

# mapa de palomas
tiled_map_palomas = Active_tilemap(ESCENARIOS_DIR / 'palomas.tmx', 6.25)

# mapa de estrella
tiled_map_estrella = Active_tilemap(ASSETS_DIR / 'estrella.tmx', 6.25)

# VARIABLES globales de archivo de sonido 

# sonido de caminar
walk_sound1 = Conditional_sound(SOUND_DIR / 'effects' / 'pasos.mp3',2)

# VARIABLES de mensaje con caja DIALOGUE

# mensaje cuando obtenés un objeto

message_got_mascara_roja = Text('Sobre tus manos reposa\nun silencio penumbroso', arial_font, (255, 41, 0), TEXTBOX_IMG)

# VARIABLES de clase y función

npc1 = NPC ((ASSETS_DIR / 'char2.png'), (ASSETS_DIR / 'char2_v2.png'), screen, 832, 256)
npc1_masked = True

# usuario, pos incial y movimiento en 0, con un inventario
char = User_character (400, 400, False, False, False, False, inventory)

# establece un reloj para fps
clock = pygame.time.Clock()

# define el primer fondo a mostrarse
background = tiled_map_caminito

# VARIABLES de lista

# lista de posiciones de palomas blancas

whitebird_choice = [(23, 1), (10, 3), (2, 4), (15, 5), (17, 5), (14, 6), (15, 6), (17, 7), (13, 7), (14, 8), (18, 8), (21, 8), (10, 8), (13, 9), (16, 9), (9, 11), (13, 11), (14, 11), (22, 13)]

# lista de posiciones de palomas grises

greybird_choice = [(26,3), (19,4), (12,6), (19,6), (11,7), (18,7), (28,7), (12,8), (17,8), (12,9), (14,9), (17,9), (18,9), (19,9), (19,9), (15,10), (16,10), (17,10), (19,10), (20,10), (12,11), (18, 11), (15,12), (10,13), (14,13), (18,13), (16,16), (20,16), (27,16)]

# lista de diálogos de NPC 1

npc1_dialogue = ['Hola, podés sentarte...', 'Mirá, no me siento muy bien', 'No sé qué decirte exactamente', 'Tomá mi máscara, así de\nfácil es la vida', 'Me encantaría tener\nun espejo...', '¡...Para que vieras tu cara!', "¡Ja, ja, ja!"]

## WHILE RUN: JUEGA
## IF RUN == FALSE: ROMPE
## NO SUMAR LOOPS O WHILES!! PELIGROSO 

while run == True:

    # Pone todo el tiempo música de fondo, la misma música

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(SOUND_DIR / 'mascarita.mp3')
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1, 35)

    # por las dudas de que algo ande mal, tiñe capa -1 de negro.

    screen.fill((0, 0, 0))

    # current time almacena el tiempo real, speed.tick deja FPS en 16

    current_time = pygame.time.get_ticks()

    clock.tick(16)

    # si el fondo es tiled_map_palomas:
    # gira las palomas cada 800ms - 2000ms
    # durante 500 ms
    # tanto grises como blancas

    if background == tiled_map_palomas:

        tiled_map_palomas.update_flips(current_time)
        
        if current_time >= current_whitebird_flip:
            position_whitebird = random.choice(whitebird_choice)
            x_chosen_whitebird, y_chosen_whitebird = position_whitebird
            
            tiled_map_palomas.flip_random_obj (12, current_time, x_chosen_whitebird, y_chosen_whitebird)
            
            random_duration = random.randint(800, 2000)
            current_whitebird_flip = current_time + random_duration

        if current_time >= current_greybird_flip:
            position_greybird = random.choice(greybird_choice)
            x_chosen_greybird, y_chosen_greybird = position_greybird
            
            tiled_map_palomas.flip_random_obj (22, current_time, x_chosen_whitebird, y_chosen_whitebird)
            
            random_duration = random.randint(800, 2000)
            current_grey_bird_flip = current_time + random_duration
    
        


    # se muestra en capa 0 MAP_SURFACE

    background.render_to_surface(screen) 
    
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
    # cambia de pantalla dos veces, en tiled_map_caminito y tiled_map_palomas

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

    # si baja X, cambiás al escenario anterior si subiste en X previamente
    # (tiled_map_caminito y tiled_map_palomas)

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

    # si Y aumenta (vas al límite de abajo)
    # en cualquier mapa no pasa nada
    # en mapa 3 (tiled_map_tren) vamos a tiled_map_estrella

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

    # Si el personaje supera Y en el escenario tiled_map_tren
    # pasa a tiled_map_estrella

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

    # FUNCIÓN CUALQUIERA: sólo sirve de ejemplo para ver que se renderizan efectivamente las imagenes y los items

    if background == tiled_map_palomas:
        if npc1_masked:
            npc1.display_npc(npc1_masked, screen)
        if npc1_masked == False:
            npc1.display_npc(npc1_masked, screen)
        result_of_collide = npc1.on_collide(char.rect)
        if result_of_collide == 2:
            if got_interaction_npc == True and dialogue_index <= len(npc1_dialogue):
                npc1.dialogue_lines(screen, got_interaction_npc, (TEXTBOX_IMG), npc1_dialogue, dialogue_index)
            elif got_item_key == True and dialogue_index > len (npc1_dialogue):
                char.add_item('Máscara roja', 'El olor a tierra y la bronca acumulada\ndurante los años de los años\nyacen en esta máscara')
                message_got_mascara_roja.render(width/2, height/2, 'center', 50)
                message_got_mascara_roja.dialogue_display(True, screen)
                npc1_masked = False
        
            
        elif result_of_collide == 1:
            collided_time = current_time
            if char.last_key == pygame.K_w: 
                char.y += 16
            if char.last_key == pygame.K_s:
                char.y -= 16
            if char.last_key == pygame.K_a: 
                char.x += 16
            if char.last_key == pygame.K_d:
                char.x -= 16
        
        
            
            

    #     message_got_item.render(char.x, char.y, 'topleft', 10)
    #     message_got_item.dialogue_display(True, screen)
    #     
    #     char.add_item('Máscara azul', 'La avaricia y abundacia, contradictorias\ncomo son, debaten su poderío\nincesantemente en esta máscara')
    #     char.add_item('Máscara verde', 'El remoto resonar de un silbato\ny el deseo de acabarlo con todo\ndescansan pacíficamente en esta máscara')
    
    # si el inventario está abierto, renderiza el inventario y lo abre

    if inventory_open == True:
        char.render_inventory(width/2, height/2, screen, 0)


    # --------------MANEJADOR DE EVENTOS--------------

    # evento pygame.QUIT: si querés salir del juego, el código rompe.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Si el evento es que se está apretando la barra espaciadora:
        # se abre el inventario, con D para un costado con A para el otro

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                

                if result_of_collide == 2:
                    if got_interaction_npc == False:
                        if dialogue_index <= len(npc1_dialogue) + 2:
                            got_interaction_npc = True 
                            dialogue_index += 1
                        else:
                            got_interaction_npc = True
                    if got_interaction_npc == True:
                        if dialogue_index <= len(npc1_dialogue):
                            got_interaction_npc = True 
                            dialogue_index += 1
                        else:
                            got_interaction_npc = False
                    
                    if got_item_key == False:
                        got_item_key = True

                    if got_item_key == True and dialogue_index == len(npc1_dialogue) + 2:
                        got_item_key = False

                    if event.key == pygame.K_q:
                        inventory_open = True
            if event.key == pygame.K_d and inventory_open == True and choose_item <= len(inventory) + 1 and inventory != []:
                choose_item += 1
            if event.key == pygame.K_a and inventory_open == True and choose_item >= 1 and inventory != []:
                choose_item -= 1

            # Si se aprieta shift, acelera el movimiento

            if event.key == pygame.K_LSHIFT:
                movement += 16

        # Si el evento es que se levanta una tecla:
        # Va para atrás el efecto que produjo previamente

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                inventory_open = False
                choose_item = 0
            if event.key == pygame.K_LSHIFT:
                movement -=16

            
    # actualiza el código al final, y constantemente
    pygame.display.update()

pygame.quit()