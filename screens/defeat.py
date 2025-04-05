import pygame
from screens.screen import Screen

class Defeat(Screen):
    def __init__(self):
        super().__init__()

    def display(self, state):
        self.draw_text("YOU LOST!", "large_bold", (self.width // 2, self.height // 2))

        pygame.display.flip()

    def handle_event(self, state, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button_text, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        if button_text == "Main Menu":
                            return "main_menu", state

        return "defeat", state