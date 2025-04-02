import pygame
from abc import ABC, abstractmethod

class Screen(ABC):
    def __init__(self, resolution =(1280, 720), buttons={}, font=None):
        self.width, self.height = resolution
        self.buttons = buttons
        self.surface = pygame.display.set_mode(resolution)
        self.fonts = self.init_fonts(font)

    def init_fonts(self, font):
        scaling_factor = self.width / 1280

        large = pygame.font.Font(font, int(60 * scaling_factor))
        medium_large = pygame.font.Font(font, int(50 * scaling_factor))
        medium = pygame.font.Font(font, int(30 * scaling_factor))
        small = pygame.font.Font(font, int(15 * scaling_factor))

        large_bold = pygame.font.SysFont(font, int(60 * scaling_factor), bold=True)
        medium_bold = pygame.font.SysFont(font, int(30 * scaling_factor), bold=True)
        small_bold = pygame.font.SysFont(font, int(15 * scaling_factor), bold=True)

        return {'large': large, 'medium_large': medium_large, 'medium': medium, 'small': small, 'large_bold': large_bold, 'medium_bold': medium_bold, 'small_bold': small_bold}

    def draw_text(self, text, font, position, color=(255, 255, 255)):
        text = self.fonts[font].render(text, True, color)
        text_rect = text.get_rect(center=position)
        self.surface.blit(text, text_rect)

    def add_text_button(self, text, font, position, color=(255, 255, 255)):
        font_text = self.fonts[font].render(text, True, color)
        text_rect = font_text.get_rect(center=position)
            
        self.buttons[text] = text_rect
    
    @abstractmethod
    def display(self, state):
        pass

    @abstractmethod
    def handle_event(self, state, event):
        pass