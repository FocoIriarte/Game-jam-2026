import pygame
from pathlib import Path
import sys


pygame.init()

# La clase User_character actualiza:
# la posición inicial y continua del jugador
# la velocidad de movimiento
# la imagen del sprite de jugador y su RECT que sirve de collider

# requiere un obj desde User_character con:
# VELOCIDAD (múltiplo de 8), posición en X inicial, posición en Y inicial...
# ...False, False, False, False (para chequear que el ninguna tecla está siendo tocada)

# el obj llama a la función update que actualiza la posición X e Y con el parámetro FALSE
# esto bloquea el sonido de caminata cuando se está quieto.

# ADICIONALMENTE, DEBERÍA:
# EJECUTAR EL INVENTARIO
  
class User_character:

    def __init__ (self, x, y, left, right, up, down, inventory):
         
         # en User_Character, las cualidades iniciales son:
         # velocidad (cuantos pixeles por movimientos)
         # x e y iniciales
         # teclas en FALSE

         self.x = x
         self.y = y
         self.left_pressed = left
         self.right_pressed = right
         self.up_pressed = up
         self.down_pressed = down
         self.inventory = inventory
         
         # imagen inicial de jugador (TIENE QUE HABER UNA MEJOR MANERA DE HACER ESTO)
         # incrementador de tamaño para el jugador
         # RECT o collider para el sprite de jugador
         self.load_sprite = pygame.image.load(Path.cwd() / 'images' / 'char.sprite.png')
         self.player_sprite = pygame.transform.scale(self.load_sprite, (54, 112))
         self.rect = self.player_sprite.get_rect(center = (self.x, self.y))

         # iniciador de movimiento vectorial, para facilitar el resto
         self.vector_pos = pygame.Vector2(0, 0)

         self.pressed_keys = []
         self.last_keys = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False, pygame.K_d: False}
         collided = False


    def movement(self, speed):

        self.speed = speed

        # key detecta cuando una tecla está siendo apretada, y da TRUE
        
        key = pygame.key.get_pressed()
        
        # por cada tecla en la lista de teclas W, A, S, D
        # si se está apretando esa tecla y no fue la última tecla en apretarse
        # y si la tecla seleccionada no está en la lista de teclas apretadas
        for key_pressed in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
            if key[key_pressed] and not self.last_keys[key_pressed]:
                if key_pressed not in self.pressed_keys:
                    # suma la tecla a la lista de teclas apretadas
                    self.pressed_keys.append(key_pressed)

            # si no está apretada pero la última tecla apretada fue ella
            # y está en la lista de teclas apretadas
            elif not key[key_pressed] and self.last_keys[key_pressed]:
                if key_pressed in self.pressed_keys:
                    # la elimina de la lista
                    self.pressed_keys.remove(key_pressed)
            
            # transforma el valor BOOLEAN de la tecla seleccionada
            # en si se apretó (TRUE) o no (FALSE)
            self.last_keys[key_pressed] = key[key_pressed]
        
        # si hay una lista de teclas apretadas:
        if self.pressed_keys:

            # last_key se vuelve la última posición de la lista de teclas apretadas

            last_key = self.pressed_keys[-1]

            # y dependiendo la tecla que sea, adjunta un valor
            self.right_pressed = last_key == pygame.K_d
            self.left_pressed = last_key == pygame.K_a
            self.up_pressed = last_key == pygame.K_w
            self.down_pressed = last_key == pygame.K_s

            # si nada fue apretado, no hay movimiento
        else:
            self.right_pressed = False
            self.left_pressed = False
            self.up_pressed = False
            self.down_pressed = False

    

    def update_position(self, is_walking):
        # variables vectoriales de posición
        self.vector_pos.x = 0
        self.vector_pos.y = 0

        # por cada tecla apretada:
        # suma 1 si suma x o y
        # resta 1 si resta x o y
        # y is_walking es TRUE para que suenen los pasos

        if self.left_pressed:
            self.vector_pos.x = -1
            self.is_walking = True

        if self.right_pressed:
            self.vector_pos.x = 1
            self.is_walking = True
        
        if self.up_pressed:
            self.vector_pos.y = -1
            self.is_walking = True
        
        if self.down_pressed:
            self.vector_pos.y = 1
            self.is_walking = True

        # si nada es apretado, is_walking vuelve a ser FALSE y no suenan los pasos
        
        if not self.down_pressed and not self.up_pressed and not self.right_pressed and not self.left_pressed:
            self.is_walking = False 
        
        # si aumentó o decreció la posición vectorial:
        # ajusta para que el movimiento sea cuadrado.

        #if self.vector_pos != (0,0):
         #   self.vector_pos.normalize_ip()

        # la posición x e y se vuelven:
        # el vector x o y (cuánto se movió) multiplicado por speed (su movimiento en pixeles)
        self.x += self.vector_pos.x * self.speed
        self.y += self.vector_pos.y * self.speed

        # finalmente, se posiciona al collider en x e y desde el centro
        self.rect.center = (self.x, self.y)

    def collide_with_tiles (self,collider_list):
    
        self.collider_list = collider_list

        collision_index = self.rect.collidelist(self.collider_list)
        
        if collision_index != -1:
            return True
        else: 
            return False

    def add_item(self, name, description):
        self.nombre = name
        self.descripcion = description
        
        self.item = {
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }

        for key, value in self.inventory:
            if value == self.nombre:
                print('Ya tienes este objeto')
        else:
            self.inventory.append(self.item)
            print(f'Nuevo objeto añadido! {self.nombre}')

    def remove_item(self, name, description):
        self.nombre = name
        self.descripcion = description
        self.item = {
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }
        for key, value in self.inventory:
            if value == self.nombre:
                self.inventory.pop(key)
                print(f'removed {self.item.nombre}!!')
            else:
                print(f"Error: {self.item.nombre} not found in inventory")

    def list_inventory(self):
        print("Current Inventory:")
        if self.inventory == []:
            print ('Inventario está vacio!!')
        else:
            for item in self.inventory:
                print(f"- {item['nombre']}: {item['descripcion']}")
            
    def render_inventory(self, x, y, surface):
        self.pos_box_x = x
        self.pos_box_y = y
        self.string = ""
        self.surface = surface
        self.box_img = (Path.cwd() / 'images' / 'cuadro de texto.png')
        self.font = pygame.font.SysFont('Monospace', 45, bold = True)

        self.load_box = pygame.image.load(self.box_img).convert_alpha()
        self.box_surface = pygame.transform.scale(self.load_box,(1200, 800))
        self.box_rect = self.box_surface.get_rect()
        setattr(self.box_rect, 'center', (self.pos_box_x, self.pos_box_y))

        for item in self.inventory:
            if item['nombre'] == 'plumita de paloma':
                self.string = "PLUMITA"
                self.render_str = self.font.render(self.string, True, (0, 0, 0))
                self.str_rect = self.render_str.get_rect()
                setattr(self.str_rect, 'center', (self.pos_box_x, self.pos_box_y))

                self.load_item = pygame.image.load(Path.cwd() / 'images' / 'personajedemonio_mascara.png').convert_alpha()
                self.item_scale = pygame.transform.scale(self.load_item, (100, 100))

                self.item_rect = self.item_scale.get_rect()
                setattr(self.item_rect, 'center', (self.pos_box_x, self.pos_box_y + 100))
            
                self.surface.blit(self.box_surface, self.box_rect)
                self.surface.blit(self.render_str, self.str_rect)
                self.surface.blit(self.item_scale, self.item_rect)
        if self.inventory == []:
            self.string = "NO HAY ITEMS EN TU INVENTARIO"
            self.render_str = self.font.render(self.string, True, (0, 0, 0))
            self.str_rect = self.render_str.get_rect().inflate(10, 10)
            setattr(self.str_rect, 'center', (self.pos_box_x, self.pos_box_y))
            self.surface.blit(self.box_surface, self.box_rect)
            self.surface.blit(self.render_str, self.str_rect)
                
