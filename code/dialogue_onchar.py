# NO TOCAR : inicia Pygame y las fuentes

import pygame
import sys

pygame.init()
pygame.font.init() 


# La clase Text recibe argumentos:
# STRING: un texto separado entre \n
# FONT: una fuente
# COLOR: un color
# BOXIMG: un cuadro de texto

class Text:
    def __init__(self, string, font, color, textbox):
        self.string = string
        self.font = font
        self.color = color
        self.textbox = textbox


    # la función RENDER recibe cuatro argumentos:
    # X, posición x
    # Y, posición y
    # TEXT_DIRECTION: direction desde X, Y para la que se proyecta el texto
    # PADDING: espacio de márgenes entre x e y

    def render(self, x, y, text_direction, paddingx, paddingy):

        self.text_direction = text_direction
        self.x = x
        self.y = y
        self.margin_x, self.margin_y = (paddingx, paddingy)
        
        # renderiza el texto a imagen basado en texto y color
        # luego obtiene un RECT basado en dicha imagen con padding
        # y asigna posición X e Y y dirección

        self.text_surface = self.font.render(self.string, True, self.color)       
        self.text_rect = self.text_surface.get_rect().inflate(self.margin_x + 80, self.margin_y)
        setattr(self.text_rect, self.text_direction, (self.x, self.y))

        # renderiza la imagen de textbox, vuelve al fondo transparente
        # luego obtiene un RECT basado en dicha imagen con dos paddings
        # y asigna posición X e Y y dirección

        self.load_textbox = pygame.image.load(self.textbox).convert_alpha()
        self.textbox_surface = pygame.transform.scale(self.load_textbox,(720, self.text_rect.height + paddingy * 2))
        self.textbox_rect = self.textbox_surface.get_rect()
        setattr(self.textbox_rect, self.text_direction, (self.x, self.y))
        
        # centra el texto y el textbox 
        self.text_rect.center = self.textbox_rect.center
        
        #NADA ES IMPRESO EN PANTALLA


    # dialogue_display recibe un BOOLEAN que debe ser TRUE
    # y un screen que debe ser screen
    def dialogue_display(self, boolean, screen):

        # Ejecuta la caja de texto y el texto mientras BOOLEAN sea TRUE
        # y regresa el valor text_on_display = TRUE
        # a menos que ya no esté en display. en cuyo caso regresa FALSE

        global text_on_display
        text_on_display = False
        if boolean:
            screen.blit(self.textbox_surface, self.textbox_rect)
            screen.blit(self.text_surface, self.text_rect)
            text_on_display = True
        else: 
            text_on_display = False
        return text_on_display
    