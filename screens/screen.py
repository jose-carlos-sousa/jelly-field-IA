import pygame, colorsys
from abc import ABC, abstractmethod

class Screen(ABC):
    def __init__(self, resolution =(1280, 720), buttons={}, font='./assets/FunBlob.ttf', bold='./assets/FunBlob.ttf'):
        self.bg = pygame.transform.scale(pygame.image.load("./assets/balala.jpg"), resolution)
        self.width, self.height = resolution
        self.buttons = buttons
        self.surface = pygame.display.set_mode(resolution)
        self.fonts = self.init_fonts(font, bold)

    def init_fonts(self, font, bold):
        scaling_factor = self.width / 1280

        large = pygame.font.Font(font, int(60 * scaling_factor))
        medium_large = pygame.font.Font(font, int(50 * scaling_factor))
        medium = pygame.font.Font(font, int(30 * scaling_factor))
        small = pygame.font.Font(font, int(15 * scaling_factor))

        large_bold = pygame.font.Font(bold, int(60 * scaling_factor))
        medium_bold = pygame.font.Font(bold, int(30 * scaling_factor))
        small_bold = pygame.font.Font(bold, int(15 * scaling_factor))

        return {'large': large, 'medium_large': medium_large, 'medium': medium, 'small': small, 'large_bold': large_bold, 'medium_bold': medium_bold, 'small_bold': small_bold}

    def get_complementary_color(self, rgb):
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)

        h = (h + 0.5) % 1.0

        r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)

        return tuple(int(x * 255) for x in (r2, g2, b2))

    def draw_text(self, text, font, position, color=(255, 255, 255), alignment="center"):
        text = self.fonts[font].render(text, True, color)
        if alignment == "center":
            text_rect = text.get_rect(center=position)
        elif alignment == "left":
            text_rect = text.get_rect(topleft=position)
        else:
            text_rect = text.get_rect(topright=position)
        self.surface.blit(text, text_rect)

    def draw_button(self, text, font, position, color=(255, 255, 255), alignment="center"):
        text = self.fonts[font].render(text, True, color)
        if alignment == "center":
            text_rect = text.get_rect(center=position)
        elif alignment == "left":
            text_rect = text.get_rect(topleft=position)
        else:
            text_rect = text.get_rect(topright=position)

        button_rect = text_rect.inflate(20, 20)
        pygame.draw.rect(self.surface, self.get_complementary_color(color), button_rect, 4, 10)
        self.surface.blit(text, text_rect)

    def add_text_button(self, text, font, position, color=(255, 255, 255), alignment="center"):
        font_text = self.fonts[font].render(text, True, color)
        if alignment == "center":
            text_rect = font_text.get_rect(center=position)
        elif alignment == "left":
            text_rect = font_text.get_rect(topleft=position)
        else:
            text_rect = font_text.get_rect(topright=position)
            
        self.buttons[text] = text_rect
    
    @abstractmethod
    def display(self, state):
        pass

    @abstractmethod
    def handle_event(self, state, event):
        pass