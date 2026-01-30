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


    
    def render (self, x, y, direction):
        self.direction = direction

        self.x = x
        self.y = y
        
        self.render_str = self.font.render(self.string, True, self.color)
        self.str_rect = self.render_str.get_rect()
        self.margin_x, self.margin_y = self.render_str.get_size()
        self.str_rect = self.render_str.get_rect().inflate(30,10)
        setattr(self.str_rect, self.direction, (self.x + self.margin_x/20, self.y + self.margin_y/15))

        self.load_box = pygame.image.load(self.boximg).convert_alpha()
        self.box_surface = pygame.transform.scale(self.load_box,(self.str_rect.width, self.str_rect.height)
        )
        self.box_rect = self.box_surface.get_rect()
        setattr(self.box_rect, self.direction, (self.x, self.y))
   
    def start_dialogue_triggered(self, current_time):
        if not self.is_active:
            self.dialogue_start_time = current_time
            self.is_active = True
       
    def dialogue_display(self, current_time, duration):
        if self.is_active:
            screen.blit(self.box_surface, self.box_rect)
            screen.blit(self.render_str, self.str_rect)
            return True  
        return False
            