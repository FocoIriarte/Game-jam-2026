import pygame
import sys

pygame.init()
pygame.font.init() 

class NPC:
    def __init__(self, npc_masked_image, npc_unmasked_image):
        self.npc_masked = npc_masked_image
        self.npc_unmasked = npc_unmasked_image
    
    def dialogue_lines(self, list_of_strings)
        self.list_of_string