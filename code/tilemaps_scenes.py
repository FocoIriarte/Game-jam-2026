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
        self.tile_image = self.tmxdata.get_tile_image_by_gid
        self.flipped_tile = {}


    def render_to_surface (self, screen):

        # render_to_surface ejecuta un loop        
        # donde cada layer tiene tiles
        for layer in self.tmxdata.layers:
            if isinstance (layer, pytmx.TiledTileLayer):
                
                # y cada tile tiene GIDs (IDs) con posición x e y
                for x, y, gid in layer:

                    # a cada GID de tile, se le adjudica su imagen
                    tile = self.tile_image(gid)
                    if tile:
                       
                        if (x, y) in self.flipped_tile:
                            tile = pygame.transform.flip(tile, True, False)

                        if self.scale != 1:
                            
                            # y a cada imagen de tile, se le adjudica la escala determinada previamente
                            tile = pygame.transform.scale(tile,(self.tilewidth, self.tileheight))
                        
                        # finalmente, se ejecuta cada tile en la pantalla con la posición
                        # determinada por x, tamaño y escala
                        screen.blit (tile,(x * self.tilewidth, y * self.tileheight))
    
    def certain_collision_objects(self, gidnum):
        blockers = []
        for layer in self.tmxdata.layers:
            for x, y, gid in layer:
                if gid == gidnum:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    tile_width = self.tmxdata.tilewidth
                    tile_height = self.tmxdata.tileheight
                    new_rect = pygame.Rect(
                        x * tile_width * self.scale,
                        y * tile_height * self.scale, 
                        tile_width * self.scale, 
                        tile_height * self.scale
                    )
                    blockers.append(new_rect)
        
        return blockers
    
    def flip_random_obj(self, gid, current_time, x, y):
        tile_pos = (x, y)
        
        self.flipped_tile[tile_pos] = current_time

    def update_flips(self, current_time):
        tiles_to_remove = []
        
        for tile_pos, flip_time in self.flipped_tile.items():
            time_elapsed = current_time - flip_time
            
            if time_elapsed > 500:
                tiles_to_remove.append(tile_pos)
        
        for tile_pos in tiles_to_remove:
            del self.flipped_tile[tile_pos]

        
                