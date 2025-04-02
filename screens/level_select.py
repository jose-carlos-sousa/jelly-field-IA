import pygame
import os
from screens.screen import Screen
from jelly_field_state import JellyFieldState

class LevelSelect(Screen):
    def __init__(self):
        super().__init__()
        self.levels = [s.split('.')[0] for s in os.listdir(os.path.join(os.getcwd(), 'levels'))]
        self.selected = 0
        self.add_text_button("Previous", "large", (200, self.height // 2))
        self.add_text_button("Next", "large", (self.width - 200, self.height // 2))
        self.add_text_button("Select", "large", (self.width // 2, self.height - 50))

    def display(self, state):
        self.surface.fill((0, 0, 0))
        self.draw_text("Select Level", "large_bold", (self.width // 2, 50))
        
        self.draw_text("Previous", "large", (200, self.height // 2))
        self.draw_text("Next", "large", (self.width - 200, self.height // 2))

        self.draw_text("Select", "large", (self.width // 2, self.height - 50))

        self.draw_text(self.levels[self.selected], "large_bold", (self.width // 2, self.height // 2))

        pygame.display.flip()

    def handle_event(self, state, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button_text, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        if button_text == "Previous":
                            self.selected = (self.selected - 1) % len(self.levels)
                        elif button_text == "Next":
                            self.selected = (self.selected - 1) % len(self.levels)
                        elif button_text == "Select":
                            file = os.path.join('.', 'levels', '.'.join([self.levels[self.selected], 'txt']))
                            new_state = JellyFieldState(file)
                            return "player_select", new_state
        return "level_select", state
