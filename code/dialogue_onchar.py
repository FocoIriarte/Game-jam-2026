import pygame
import sys

pygame.init()
pygame.font.init() 

screen_width = 1920 // 2
screen_height = 720 // 2
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mascaritas")
clock = pygame.time.Clock
font = pygame.font.SysFont('cambria', 24)

class Dialogue:
    def __init__(self, string, font, color, boximg):
        self.string = string
        self.font = font
        self.boximg = boximg
        self.color = color
        self.dialogue_start = None
        self.dialogue_start = None 
        self.dialogue_end = None
        self.is_active = False


    
    def render(self, x, y, direction, padding):
        self.direction = direction
        self.x = x
        self.y = y
        
        self.render_str = self.font.render(self.string, True, self.color)
        self.str_rect = self.render_str.get_rect()
        self.margin_x, self.margin_y = (padding/2, padding/2)
        self.str_rect = self.render_str.get_rect().inflate(30, 10)
        setattr(self.str_rect, self.direction, (self.x, self.y))

        self.padding = padding
        self.load_box = pygame.image.load(self.boximg).convert_alpha()
        self.box_surface = pygame.transform.scale(
            self.load_box,
            (self.str_rect.width + padding * 2, self.str_rect.height + padding * 2)
        )
        self.box_rect = self.box_surface.get_rect()
        setattr(self.box_rect, self.direction, (self.x, self.y))
        
        # Center the text within the padded box
        self.str_rect.center = self.box_rect.center
            
    def dialogue_display(self, boolean):
        if boolean:
            screen.blit(self.box_surface, self.box_rect)
            screen.blit(self.render_str, self.str_rect)
    
    def dialogue_activate (self, activation, boolean):
        if activation == boolean:
            screen.blit(self.box_surface, self.box_rect)
            screen.blit(self.render_str, self.str_rect)

    