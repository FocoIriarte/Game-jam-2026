import pygame
import sys

pygame.init()
pygame.font.init() 

class NPC:
    def __init__(self, npc_masked_image, npc_unmasked_image, surface, x, y):
        self.npc_masked_image = npc_masked_image
        self.npc_unmasked_image = npc_unmasked_image
        self.surface = surface
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont('Monospace', 22, bold=True)
    
    def display_npc(self, boolean, surface):
        if boolean:
            self.load_sprite = pygame.image.load(self.npc_masked_image).convert_alpha()
            self.player_sprite = pygame.transform.scale(self.load_sprite, (54, 112))
            self.rect = self.player_sprite.get_rect(center = (self.x, self.y))
            self.talk_rect = self.player_sprite.get_rect(center = (self.x, self.y)).inflate(60,40)

        else:
            self.load_sprite = pygame.image.load(self.npc_unmasked_image).convert_alpha()
            self.player_sprite = pygame.transform.scale(self.load_sprite, (54, 112))
            self.rect = self.player_sprite.get_rect(center = (self.x, self.y))
            self.talk_rect = self.player_sprite.get_rect(center = (self.x, self.y)).inflate(60, 40)

        surface.blit(self.player_sprite, self.rect)

    def on_collide(self, player_rect):
        if player_rect.colliderect(self.rect):
             return 1
        if player_rect.colliderect(self.talk_rect):
             return 2
        return 0

    def dialogue_lines(self, surface, boolean, textbox, list_of_strings, dialogue_index):

        self.dialogue_index = dialogue_index

        if not boolean:
            return
        
        self.list_of_strings = list_of_strings

        if self.dialogue_index >= len(list_of_strings):
            self.dialogue_index = len(list_of_strings) - 1
        
        current_text = self.list_of_strings[self.dialogue_index]
    
        self.render_str = self.font.render(current_text, True, (0, 0, 0))
        self.rect_str = self.render_str.get_rect()
        setattr(self.rect_str, 'topleft', (self.x + 50, self.y))

        self.load_textbox = pygame.image.load(textbox).convert_alpha()
        self.textbox_increased = pygame.transform.scale(self.load_textbox,(480, self.rect_str.height + 40))
        self.textbox_surface = self.textbox_increased.get_rect()
        setattr(self.textbox_surface, 'topleft', (self.x + 30, self.y - 30))

        self.surface.blit(self.textbox_increased, self.textbox_surface)
        self.surface.blit(self.render_str, self.rect_str)