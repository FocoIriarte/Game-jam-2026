import pygame
import pytmx
from pathlib import Path

pygame.init()
width = 1600
height = 900
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
tmxdata = pytmx.load_pygame('images/escenarios/palomas.tmx')


target_gid = 22

print(tmxdata.get_tile_gid(11, 7, 1))

for x, y, index in tmxdata.get_tile_locations_by_gid(target_gid):
   print(f"Tile found at map coordinates ({x}, {y})")


#for gid, properties in tmxdata.tile_properties.items():
#         print(f"GID: {gid}, Properties: {properties}")

