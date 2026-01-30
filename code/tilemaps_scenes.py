import pygame
import pytmx
from pytmx.util_pygame import load_pygame
import random

# La clase Active_tilemaps nombra:
# un tilemap activo con un archivo TMX para ser ejecutado
# + otras funciones de tiles que todavía no tiene

# requiere un obj desde Active_tilemap con:
# un archivo TMX y un número multiplicador para escalar ese archivo
# generalmente el número será 6.25

# la función render_to_surface toma como argumento un surface
# generalmente screen
# para ejecutar el TMX en la pantalla

pygame.init()

class Active_tilemap:

    def __init__(self, filename_TMX, scale_multiplier):
        
        # Active_tilemap llama al archivo y lo carga al programa
        # luego, nombra diferentes características como:
        # alto, ancho, alto de tile, ancho de tile, escala, etc.

        self.tmxdata = pytmx.load_pygame(filename_TMX, pixelalpha=True)
        self.scale = scale_multiplier
        self.tilewidth = self.tmxdata.tilewidth * self.scale
        self.tileheight = self.tmxdata.tileheight * self.scale

    def render_to_surface (self, surface):

        tile_image = self.tmxdata.get_tile_image_by_gid

        # render_to_surface ejecuta un loop        
        # donde cada layer tiene tiles
        for layer in self.tmxdata.layers:
            if isinstance (layer, pytmx.TiledTileLayer):
                
                # y cada tile tiene GIDs (IDs) con posición x e y
                for x, y, gid in layer:

                    # a cada GID de tile, se le adjudica su imagen
                    tile = tile_image(gid)
                    if tile:
                        if self.scale != 1:
                            
                            # y a cada imagen de tile, se le adjudica la escala determinada previamente
                            tile = pygame.transform.scale(tile,(self.tilewidth, self.tileheight))
                        
                        # finalmente, se ejecuta cada tile en la pantalla con la posición
                        # determinada por x, tamaño y escala
                        surface.blit(tile,(x * self.tilewidth, y * self.tileheight))
    
    def collision_objects (self):
        blockers = []
        for layer in self.tmxdata.layers:
            for x, y, gid in layer:
                if gid != 0:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    tile_width = self.tmxdata.tilewidth
                    tile_height = self.tmxdata.tileheight
                    new_rect = pygame.Rect(x * tile_width * self.scale,y * tile_height * self.scale, tile_width * self.scale, tile_height * self.scale)
                    blockers.append(new_rect)
            return blockers
    
    def flip_random_obj (self, current_time):
        self.random_duration = random.randint(1000, 4000)
        self.current_bird_flip = current_time + self.random_duration
        flipped = True  
        
        if current_time <= self.current_bird_flip:
            self.x_y_choice = [(23, 1), (10, 3), (2, 4), (15, 5), (17, 5), (14, 6), (15, 6), (17, 7), (13, 7), (14, 8), (18, 8), (21, 8), (10, 8), (13, 9), (16, 9), (9, 11), (13, 11), (14, 11), (22, 13)]
            self.x_y = random.choice(self.x_y_choice)
            self.x_chosen, self.y_chosen = self.x_y
            self.palomita_random = self.tmxdata.get_tile_image(self.x_chosen, self.y_chosen, 0)

            if self.palomita_random is not None:
                print(f'{self.x_chosen}, {self.y_chosen}')
                self.palomita_random = pygame.transform.flip(self.palomita_random, True, False)
            else:
                print(f"No se encontró tile en ({self.x_chosen}, {self.y_chosen}, capa 0)")
        else: 
            print('Something went wrong')
    



